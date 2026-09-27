import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "http://localhost:8793/index.html"
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

    # dashboard dropdown open/select/close, cross-filter
    page.click("#m-dashboard")
    page.wait_for_timeout(150)
    page.click("#dd-dist .dd-btn")
    page.wait_for_timeout(100)
    opts = page.query_selector_all("#dd-dist .chk")
    check("dropdown distancia abre com 2 opcoes", len(opts)==2)
    opts[1].click()  # "Mais longe"
    page.wait_for_timeout(150)
    chip = page.query_selector(".achip")
    check("filtro aplicado gera chip", chip is not None)
    fcount = page.inner_text("#fcount")
    check("contador atualizado", "de 733" in fcount)
    # remove filter via chip
    if chip: chip.click()
    page.wait_for_timeout(150)
    check("filtro removido", page.query_selector(".achip") is None)

    # matrix click-to-filter
    rect = page.query_selector("#d-heat svg rect[data-flt]")
    if rect:
        rect.click()
        page.wait_for_timeout(150)
        sel_stroke = page.eval_on_selector("#d-heat svg rect[stroke]", "el=>!!el") if page.query_selector("#d-heat svg rect[stroke]") else False
        check("matriz seleciona celula (stroke aplicado)", sel_stroke)
        again = page.query_selector("#d-heat svg rect[stroke]")
        if again: again.click()
        page.wait_for_timeout(150)

    # table sort
    th = page.query_selector("#d-tab th[data-k='it']")
    th.click(); page.wait_for_timeout(100)
    sort_attr = page.get_attribute("#d-tab th[data-k='it']", "aria-sort")
    check("coluna ordenavel aplica aria-sort", sort_attr in ("ascending","descending"))

    # xlsx download
    with page.expect_download(timeout=8000) as dl_info:
        page.click("#t-xlsx")
    dl = dl_info.value
    path = dl.path()
    import os
    size = os.path.getsize(path) if path else 0
    check("xlsx baixa e tem tamanho > 1KB", size > 1000)

    # slides nav to 9/9
    page.click("#m-slides")
    page.wait_for_timeout(150)
    for _ in range(10):
        nxt = page.query_selector("#next")
        if not nxt: break
        disabled = page.eval_on_selector("#next", "el=>el.disabled")
        if disabled: break
        nxt.click(); page.wait_for_timeout(80)
    frame_txt = page.inner_text(".framenum >> visible=true") if page.query_selector(".framenum") else ""
    check("slides chegam a 9/9", "9" in frame_txt)

    # pptx download
    pptx_btn = page.query_selector("#dl-pptx")
    with page.expect_download(timeout=8000) as dl_info2:
        pptx_btn.click()
    dl2 = dl_info2.value
    size2 = os.path.getsize(dl2.path()) if dl2.path() else 0
    check("pptx baixa e tem tamanho > 1KB", size2 > 1000)

    check("zero console/page errors", len(errs)==0)
    if errs: print("ERROS:", errs)

    b.close()

print()
print("RESUMO:", sum(1 for _,v in ok if v), "/", len(ok), "OK")
