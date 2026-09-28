import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = "C:/Users/Augusto/AppData/Local/Temp/claude/c--Users-Augusto-Desktop-Projetos-hr-absenteeism-dmaic/a644b0a9-03d7-4f22-8620-9bdd173194c9/scratchpad"
URL = "http://localhost:8799/index.html"
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
    page = b.new_page(viewport={"width": 1600, "height": 1000}, color_scheme="dark")
    page.on("console", on_console); page.on("pageerror", on_pageerror)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(500)

    # I5: recommendation block + link navigates to relatorio s2
    check("I5 bloco de recomendacao presente", page.query_selector(".reco") is not None)
    page.click("#reco-link"); page.wait_for_timeout(400)
    check("I5 link leva ao modo relatorio", page.is_hidden("#pane-dashboard"))
    s2_visible = page.eval_on_selector("#s2", "el => { const r = el.getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; }")
    check("I5 rola ate a secao 2", s2_visible)
    page.click("#m-dashboard"); page.wait_for_timeout(200)

    # I6: matrix shows n=
    check("I6 matriz mostra n=", "n=" in page.inner_text("#d-heat"))

    # I7: badges + charts present in Dashboard
    check("I7 badge testado (dashboard)", page.query_selector(".badge-testado") is not None)
    check("I7 badge exploratorio (dashboard)", page.query_selector(".badge-exploratorio") is not None)
    check("I7 grafico dia-tipo renderizou", page.eval_on_selector("#d-dia-tipo", "el=>el.querySelectorAll('rect').length>0"))
    check("I7 grafico mes-tipo renderizou", page.eval_on_selector("#d-mes-tipo", "el=>el.querySelectorAll('rect').length>0"))
    check("I7 tabela bruta esta dentro de details", page.query_selector("details table#d-tab") is not None)

    # I4: autor placeholder present, all 3 modes
    check("I4 autor no dashboard", "preencha" in page.inner_text(".autor"))
    page.click("#m-relatorio"); page.wait_for_timeout(200)
    check("I4 autor visivel no modo relatorio", page.is_visible(".autor"))
    check("I7 badges espelhados no relatorio", page.query_selector("#pane-relatorio .badge-testado") is not None and page.query_selector("#pane-relatorio .badge-exploratorio") is not None)
    check("I7 graficos espelhados no relatorio renderizaram", page.eval_on_selector("#rep-dia-tipo", "el=>el.querySelectorAll('rect').length>0") and page.eval_on_selector("#rep-mes-tipo", "el=>el.querySelectorAll('rect').length>0"))
    page.click("#m-slides"); page.wait_for_timeout(200)
    check("I4 autor visivel no modo slides", page.is_visible(".autor"))
    page.click("#m-dashboard"); page.wait_for_timeout(200)

    # regression: existing mechanics
    page.click("#dd-dist .dd-btn"); page.wait_for_timeout(100)
    opts = page.query_selector_all("#dd-dist .chk")
    opts[1].click(); page.wait_for_timeout(150)
    check("regressao: filtro cruzado ainda funciona", page.query_selector(".achip") is not None)
    page.query_selector(".achip").click(); page.wait_for_timeout(100)

    rect = page.query_selector("#d-heat svg rect[data-flt]")
    rect.click(); page.wait_for_timeout(150)
    check("regressao: matriz seleciona", page.query_selector("#d-heat svg rect[stroke]") is not None)
    page.query_selector("#d-heat svg rect[stroke]").click(); page.wait_for_timeout(150)

    # open details to reveal table, then test sort/xlsx
    page.click("details summary"); page.wait_for_timeout(150)
    th = page.query_selector("#d-tab th[data-k='mo']")
    th.click(); page.wait_for_timeout(100)
    check("regressao: ordenacao de tabela", page.get_attribute("#d-tab th[data-k='mo']", "aria-sort") is not None)
    with page.expect_download(timeout=8000) as dlx:
        page.click("#t-xlsx")
    check("regressao: xlsx > 1KB", os.path.getsize(dlx.value.path()) > 1000)

    page.click("#f-reset"); page.wait_for_timeout(150)

    page.click("#m-slides"); page.wait_for_timeout(200)
    for _ in range(10):
        nxt = page.query_selector("#next")
        if page.eval_on_selector("#next", "el=>el.disabled"): break
        nxt.click(); page.wait_for_timeout(60)
    check("regressao: slides chegam a 9/9", "9" in page.inner_text(".framenum >> visible=true"))
    with page.expect_download(timeout=8000) as dlp:
        page.click("#dl-pptx")
    check("regressao: pptx > 1KB", os.path.getsize(dlp.value.path()) > 1000)

    # B1/B2/CID scan
    html = page.content()
    b1 = len(re.findall(r'\bB1\b', html)); b2 = len(re.findall(r'\bB2\b', html)); cid = len(re.findall(r'\bCID\b', html))
    check("nenhuma ocorrencia de B1/B2/CID fora do gloss.", b1==0 and b2==0 and cid<=1)

    # numeric consistency: headline
    page.click("#m-dashboard"); page.wait_for_timeout(200)
    dash_num = page.inner_text(".bignum")
    check("manchete 64,3% intacta", "64,3" in dash_num)

    check("zero console/page errors", len(errs) == 0)
    if errs: print("ERROS:", errs)

    # screenshots for record
    page.screenshot(path=f"{OUT}/banca_final_dashboard.png", full_page=True)
    page.emulate_media(color_scheme="light"); page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/banca_final_dashboard_light.png", full_page=True)
    page.emulate_media(color_scheme="dark")
    page.set_viewport_size({"width":390,"height":844}); page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/banca_final_dashboard_mobile.png", full_page=True)
    page.set_viewport_size({"width":1600,"height":1000})
    page.click("#m-relatorio"); page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/banca_final_relatorio.png", full_page=True)

    b.close()

print()
print("RESUMO:", sum(1 for _, v in ok if v), "/", len(ok), "OK")
