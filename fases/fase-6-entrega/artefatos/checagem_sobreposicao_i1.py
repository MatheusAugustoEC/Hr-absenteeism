import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = "C:/Users/Augusto/AppData/Local/Temp/claude/c--Users-Augusto-Desktop-Projetos-hr-absenteeism-dmaic/a644b0a9-03d7-4f22-8620-9bdd173194c9/scratchpad"
URL = "http://localhost:8800/index.html"

def rects_overlap(a, b):
    return not (a['right'] <= b['left'] or b['right'] <= a['left'] or a['bottom'] <= b['top'] or b['bottom'] <= a['top'])

def check_pareto_labels(page, label):
    # the x-axis category labels in #rep-pareto are the <text> elements with a data-tip
    # attribute holding the full motivo name (distinguishes them from the axis-scale labels)
    boxes = page.eval_on_selector_all(
        "#rep-pareto svg text[data-tip]",
        "els => els.map(e => { const r = e.getBoundingClientRect(); return {left:r.left, right:r.right, top:r.top, bottom:r.bottom, text: e.textContent}; })"
    )
    collisions = []
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            if rects_overlap(boxes[i], boxes[j]):
                collisions.append((boxes[i]['text'], boxes[j]['text']))
    print(f"[{label}] rotulos: {[b['text'] for b in boxes]}")
    print(f"[{label}] colisoes: {len(collisions)} -> {collisions}")
    return len(collisions)

total_collisions = 0
with sync_playwright() as p:
    b = p.chromium.launch()

    page = b.new_page(viewport={"width": 1400, "height": 1000}, color_scheme="dark")
    page.goto(URL, wait_until="networkidle")
    page.click("#m-relatorio")
    page.wait_for_timeout(400)
    el = page.query_selector("#rep-pareto")
    el.scroll_into_view_if_needed()
    page.wait_for_timeout(150)
    total_collisions += check_pareto_labels(page, "desktop-escuro")
    el.screenshot(path=f"{OUT}/i1r2_dark.png")

    page.emulate_media(color_scheme="light")
    page.wait_for_timeout(200)
    total_collisions += check_pareto_labels(page, "desktop-claro")
    el.screenshot(path=f"{OUT}/i1r2_light.png")

    page.emulate_media(color_scheme="dark")
    page.set_viewport_size({"width": 390, "height": 900})
    page.wait_for_timeout(200)
    el2 = page.query_selector("#rep-pareto")
    el2.scroll_into_view_if_needed()
    page.wait_for_timeout(150)
    total_collisions += check_pareto_labels(page, "mobile")
    el2.screenshot(path=f"{OUT}/i1r2_mobile.png")

    b.close()

print()
print("TOTAL DE COLISOES NOS 3 CENARIOS:", total_collisions)
