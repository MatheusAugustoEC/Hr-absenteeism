import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = "C:/Users/Augusto/AppData/Local/Temp/claude/c--Users-Augusto-Desktop-Projetos-hr-absenteeism-dmaic/a644b0a9-03d7-4f22-8620-9bdd173194c9/scratchpad"
URL = "http://localhost:8794/index.html"

errs = []
def on_console(msg):
    if msg.type == "error": errs.append(msg.text)
def on_pageerror(e): errs.append("pageerror: "+str(e))

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("OK  " if cond else "FAIL"), name)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width":1400,"height":1000}, color_scheme="dark")
    page.on("console", on_console); page.on("pageerror", on_pageerror)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(200)

    # PAINEL
    page.screenshot(path=f"{OUT}/v3_painel_dark.png", full_page=True)

    # DASHBOARD
    page.click("#m-dashboard"); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v3_dashboard_dark.png", full_page=True)
    check("dashboard usa grade12", page.eval_on_selector("#dash-body", "el=>el.classList.contains('grade12')"))

    # dropdown/filter still works
    page.click("#dd-dist .dd-btn"); page.wait_for_timeout(100)
    opts = page.query_selector_all("#dd-dist .chk")
    opts[1].click(); page.wait_for_timeout(150)
    check("filtro cross ok", page.query_selector(".achip") is not None)
    page.query_selector(".achip").click(); page.wait_for_timeout(100)

    # RELATORIO
    page.click("#m-relatorio"); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v3_relatorio_dark.png", full_page=True)
    check("relatorio tem faixa de kpis nova", page.query_selector("#pane-relatorio .kpis") is not None)
    check("fmea usa pill de severidade", page.query_selector(".sevpill") is not None)

    # SLIDES
    page.click("#m-slides"); page.wait_for_timeout(250)
    page.screenshot(path=f"{OUT}/v3_slide1_dark.png")
    check("slide 1 tem fpill", page.query_selector(".frame.on .fpill") is not None)

    for _ in range(10):
        nxt = page.query_selector("#next")
        disabled = page.eval_on_selector("#next", "el=>el.disabled")
        if disabled: break
        nxt.click(); page.wait_for_timeout(60)
    frame_txt = page.inner_text(".framenum >> visible=true")
    check("slides chegam a 9/9", "9" in frame_txt)
    page.screenshot(path=f"{OUT}/v3_slide9_dark.png")

    # downloads still work
    page.click("#m-dashboard"); page.wait_for_timeout(150)
    with page.expect_download(timeout=8000) as dlx:
        page.click("#t-xlsx")
    check("xlsx > 1KB", os.path.getsize(dlx.value.path()) > 1000)

    page.click("#m-slides"); page.wait_for_timeout(150)
    with page.expect_download(timeout=8000) as dlp:
        page.click("#dl-pptx")
    check("pptx > 1KB", os.path.getsize(dlp.value.path()) > 1000)

    # light theme + mobile
    page.emulate_media(color_scheme="light")
    page.click("#m-painel"); page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v3_painel_light.png", full_page=True)
    page.click("#m-dashboard"); page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v3_dashboard_light.png", full_page=True)

    page.emulate_media(color_scheme="dark")
    page.set_viewport_size({"width":390,"height":844})
    page.click("#m-painel"); page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v3_painel_mobile.png", full_page=True)
    page.click("#m-dashboard"); page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v3_dashboard_mobile.png", full_page=True)
    page.click("#m-relatorio"); page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v3_relatorio_mobile.png", full_page=True)

    check("zero console/page errors", len(errs)==0)
    if errs: print("ERROS:", errs)

    b.close()

print()
print("RESUMO:", sum(1 for _,v in ok if v), "/", len(ok), "OK")
