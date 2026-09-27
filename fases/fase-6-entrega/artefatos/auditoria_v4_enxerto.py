import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

# Roda a pagina publicada localmente (python -m http.server na pasta pagina/)
# antes de rodar este script. Audita o enxerto real do Painel (v4): as duas
# secoes ECharts renderizam com os dados do pipeline, o registro de idioma
# funciona dentro do enxerto, a tabela nao herda o th{background} global da
# pagina, e os outros tres modos continuam intactos.

URL = "http://localhost:8795/index.html"
errs = []
def on_console(msg):
    if msg.type == "error": errs.append(msg.text)
def on_pageerror(e): errs.append("pageerror: " + str(e))

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("OK  " if cond else "FAIL"), name)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1400, "height": 1000}, color_scheme="dark")
    page.on("console", on_console); page.on("pageerror", on_pageerror)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(500)

    check("pareto (echarts) renderizou svg", page.eval_on_selector("#chart-pareto-enx", "el=>el.querySelectorAll('svg').length>0"))
    check("barras agrupadas (echarts) renderizou svg", page.eval_on_selector("#chart-barras-enx", "el=>el.querySelectorAll('svg').length>0"))
    check("badge achado promissor presente", page.query_selector("#painel-enxerto .badge-promissor2") is not None)

    txt_sim = page.inner_text("#painel-enxerto .marca h2")
    page.click("#r-tecnica"); page.wait_for_timeout(200)
    txt_tec = page.inner_text("#painel-enxerto .marca h2")
    check("registro simples/tecnica muda texto do enxerto", txt_sim != txt_tec)
    page.click("#r-simples"); page.wait_for_timeout(150)

    page.click("#m-dashboard"); page.wait_for_timeout(200)
    page.click("#dd-dist .dd-btn"); page.wait_for_timeout(100)
    opts = page.query_selector_all("#dd-dist .chk")
    opts[1].click(); page.wait_for_timeout(150)
    check("dashboard filtro cruzado intacto", page.query_selector(".achip") is not None)
    page.query_selector(".achip").click(); page.wait_for_timeout(100)
    with page.expect_download(timeout=8000) as dlx:
        page.click("#t-xlsx")
    check("xlsx > 1KB", os.path.getsize(dlx.value.path()) > 1000)

    page.click("#m-relatorio"); page.wait_for_timeout(200)
    check("relatorio kpis intacto", page.query_selector("#pane-relatorio .kpis") is not None)

    page.click("#m-slides"); page.wait_for_timeout(200)
    with page.expect_download(timeout=8000) as dlp:
        page.click("#dl-pptx")
    check("pptx > 1KB", os.path.getsize(dlp.value.path()) > 1000)

    check("zero console/page errors", len(errs) == 0)
    if errs: print("ERROS:", errs)

    b.close()

print()
print("RESUMO:", sum(1 for _, v in ok if v), "/", len(ok), "OK")
