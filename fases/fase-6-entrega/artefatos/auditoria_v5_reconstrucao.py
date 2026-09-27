import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = "C:/Users/Augusto/AppData/Local/Temp/claude/c--Users-Augusto-Desktop-Projetos-hr-absenteeism-dmaic/a644b0a9-03d7-4f22-8620-9bdd173194c9/scratchpad"
URL = "http://localhost:8796/index.html"
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
    page.wait_for_timeout(400)

    # dropdown open/select/stay-open
    page.click("#dd-dist .dd-btn"); page.wait_for_timeout(100)
    opts = page.query_selector_all("#dd-dist .chk")
    check("dropdown distancia abre com 2 opcoes", len(opts) == 2)
    opts[1].click(); page.wait_for_timeout(150)
    check("menu continua aberto apos marcar", page.is_visible("#dd-dist .dd-panel"))
    chip = page.query_selector(".achip")
    check("filtro aplicado gera chip", chip is not None)
    fcount = page.inner_text("#fcount")
    check("contador atualizado", "de 733" in fcount)
    page.click("body")
    page.wait_for_timeout(100)
    page.query_selector(".achip").click(); page.wait_for_timeout(150)
    check("filtro removido via chip", page.query_selector(".achip") is None)

    # matrix double click
    rect = page.query_selector("#d-heat svg rect[data-flt]")
    rect.click(); page.wait_for_timeout(150)
    check("matriz seleciona", page.query_selector("#d-heat svg rect[stroke]") is not None)
    page.query_selector("#d-heat svg rect[stroke]").click(); page.wait_for_timeout(150)
    check("matriz desmarca", page.query_selector("#d-heat svg rect[stroke]") is None)

    # table sort
    th = page.query_selector("#d-tab th[data-k='mo']")
    th.click(); page.wait_for_timeout(100)
    check("coluna ordenavel aplica aria-sort", page.get_attribute("#d-tab th[data-k='mo']", "aria-sort") is not None)

    # mostrar todas
    btn_all = page.query_selector("#t-all")
    if btn_all and btn_all.is_visible():
        btn_all.click(); page.wait_for_timeout(100)
        check("mostrar todas expande tabela", "Mostrar só" in page.inner_text("#t-all"))
        btn_all.click()

    # xlsx download
    with page.expect_download(timeout=8000) as dlx:
        page.click("#t-xlsx")
    check("xlsx > 1KB", os.path.getsize(dlx.value.path()) > 1000)

    # reset filters
    page.click("#f-reset"); page.wait_for_timeout(150)
    check("limpar filtros zera selecao", "Nenhum filtro" in page.inner_text("#active"))

    # relatorio mode
    page.click("#m-relatorio"); page.wait_for_timeout(300)
    check("relatorio kpis presentes", page.query_selector("#pane-relatorio .kpis") is not None)
    check("side-filtros escondido fora do dashboard", page.is_hidden("#side-filtros"))
    check("relatorio tem 16 secoes h2", len(page.query_selector_all("#pane-relatorio h2")) == 16)

    # print PDF button opens glossary (won't actually print in headless, just check handler runs)
    # slides mode
    page.click("#m-slides"); page.wait_for_timeout(300)
    check("side-filtros escondido em slides", page.is_hidden("#side-filtros"))
    for _ in range(10):
        nxt = page.query_selector("#next")
        if page.eval_on_selector("#next", "el=>el.disabled"): break
        nxt.click(); page.wait_for_timeout(60)
    frame_txt = page.inner_text(".framenum >> visible=true")
    check("slides chegam a 9/9", "9" in frame_txt)

    with page.expect_download(timeout=8000) as dlp:
        page.click("#dl-pptx")
    check("pptx > 1KB", os.path.getsize(dlp.value.path()) > 1000)

    # numeric consistency: headline 64,3 in dashboard and slide1
    page.click("#m-dashboard"); page.wait_for_timeout(200)
    dash_num = page.inner_text(".bignum")
    page.click("#m-slides"); page.wait_for_timeout(200)
    page.evaluate("document.querySelectorAll('.frame')[0].classList.add('on')")
    slide1_txt = page.inner_text(".frame:nth-child(1)")
    check("manchete identica dashboard/slide1", "64,3" in dash_num and "64,3" in slide1_txt)

    # B1/B2/CID search
    html = page.content()
    b1 = len(re.findall(r'\bB1\b', html)); b2 = len(re.findall(r'\bB2\b', html)); cid = len(re.findall(r'\bCID\b', html))
    check("nenhuma ocorrencia de B1/B2 fora do glossario (so CID no gloss.)", b1==0 and b2==0 and cid<=1)

    # theme + mobile screenshots
    page.click("#m-dashboard"); page.wait_for_timeout(200)
    page.emulate_media(color_scheme="light"); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v5_dashboard_light.png", full_page=True)
    page.emulate_media(color_scheme="dark")
    page.set_viewport_size({"width":390,"height":844}); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v5_dashboard_mobile.png", full_page=True)
    page.click("#m-relatorio"); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v5_relatorio_mobile.png", full_page=True)
    page.click("#m-slides"); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v5_slides_mobile.png", full_page=True)

    check("zero console/page errors", len(errs) == 0)
    if errs: print("ERROS:", errs)

    b.close()

print()
print("RESUMO:", sum(1 for _, v in ok if v), "/", len(ok), "OK")
