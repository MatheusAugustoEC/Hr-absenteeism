import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = "C:/Users/Augusto/AppData/Local/Temp/claude/c--Users-Augusto-Desktop-Projetos-hr-absenteeism-dmaic/a644b0a9-03d7-4f22-8620-9bdd173194c9/scratchpad"
URL = "http://localhost:8793/index.html"

errs = []

def on_console(msg):
    if msg.type == "error":
        errs.append(msg.text)

def on_pageerror(e):
    errs.append("pageerror: " + str(e))

with sync_playwright() as p:
    b = p.chromium.launch()

    # 1) dark theme, painel, simples
    page = b.new_page(viewport={"width": 1400, "height": 1000}, color_scheme="dark")
    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(300)
    page.screenshot(path=f"{OUT}/v2_painel_dark_simples.png", full_page=True)

    # check for badge, guardrail
    badge = page.query_selector(".badge-promissor")
    print("badge presente:", badge is not None)
    guard = page.query_selector(".kpi-guard")
    print("kpi guard presente:", guard is not None)

    # switch to tecnica
    page.click("#r-tecnica")
    page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v2_painel_dark_tecnica.png", full_page=True)

    # check svg rendered (bars exist)
    n_pareto_rects = page.eval_on_selector("#chart-pareto svg", "el => el.querySelectorAll('rect').length") if page.query_selector("#chart-pareto svg") else 0
    n_h1_rects = page.eval_on_selector("#chart-h1 svg", "el => el.querySelectorAll('rect').length") if page.query_selector("#chart-h1 svg") else 0
    print("pareto rects:", n_pareto_rects, "h1 rects:", n_h1_rects)

    # legend for h1
    leg = page.inner_text("#legend-h1")
    print("legend-h1:", leg.replace("\n"," | "))

    # dashboard mode
    page.click("#m-dashboard")
    page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v2_dashboard_dark.png", full_page=True)

    # relatorio mode
    page.click("#m-relatorio")
    page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v2_relatorio_dark.png", full_page=True)

    # slides mode
    page.click("#m-slides")
    page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v2_slide1_dark.png")

    # back to painel, light theme
    page.click("#m-painel")
    page.wait_for_timeout(150)
    page.emulate_media(color_scheme="light")
    page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v2_painel_light.png", full_page=True)

    # mobile width, dark
    page.emulate_media(color_scheme="dark")
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(200)
    page.screenshot(path=f"{OUT}/v2_painel_mobile.png", full_page=True)

    print("console/page errors:", errs)
    b.close()
print("done")
