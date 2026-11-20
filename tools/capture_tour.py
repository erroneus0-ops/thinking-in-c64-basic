"""Capture the screenshots for the C64 tour (docs/tour/). Development tool: needs the course
site running on 127.0.0.1:8064 with runtime/ in place, plus Playwright and Pillow.
Writes tools/tour_shots/*.webp. Then run tools/build_tour.py."""
import asyncio, io, pathlib, sys
from PIL import Image
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "tour_shots"
URL = "http://127.0.0.1:8064"
CHROME = sys.argv[1] if len(sys.argv) > 1 else None

def save(png, name, width=None):
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(OUT / f"{name}.webp", "WEBP", quality=82)
    print("saved", name, im.size)

async def typing(page, text, wait=0):
    await page.evaluate("document.getElementById('c64').contentWindow.wasm_auto_type(%r)" % text)
    await page.wait_for_timeout(wait or 600 + 110 * len(text))

async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME) if CHROME else await p.chromium.launch()
        page = await b.new_page(viewport={"width": 1280, "height": 860})
        await page.goto(URL + "/login?next=/c64"); await page.fill("#name", "Ace"); await page.click("button[type=submit]"); await page.wait_for_url(URL + "/c64")
        await page.wait_for_function("document.getElementById('status').textContent.startsWith('Ready')", timeout=90000)
        await page.wait_for_timeout(800)
        screen = page.locator(".screen")
        save(await screen.screenshot(), "ready", 900)
        # Caps Lock: same word typed in small letters and in capitals
        await typing(page, 'print "hi"\nPRINT "HI"\n')
        save(await screen.screenshot(), "capslock", 900)
        await page.click("button[data-keys='ShiftLeft home']"); await page.wait_for_timeout(700)
        # RETURN: direct mode, then a stored line, then RUN
        await typing(page, 'print "level up"\n10 print "stored for later"\nrun\n')
        save(await screen.screenshot(), "return", 900)
        await page.click("button[data-keys='ShiftLeft home']"); await page.wait_for_timeout(700)
        # An error, and its fix
        await typing(page, 'gold = 100\ngld = 100\n? gld\n')
        save(await screen.screenshot(), "error", 900)
        # The controls under the screen, and the special keys panel
        save(await page.locator(".under-screen").screenshot(), "under", 900)
        aside = page.locator("aside")
        box = await aside.bounding_box()
        keys = await page.locator("button[data-keys='runStop']").bounding_box()
        save(await page.screenshot(clip={"x": box["x"], "y": keys["y"] - 48, "width": box["width"], "height": 100}), "keys", 700)
        # Shift-click: a listed program, cursor placed mid-line
        await page.click("button[data-keys='ShiftLeft home']"); await page.wait_for_timeout(700)
        await typing(page, 'new\n10 print "my best score"\n20 pirnt "9000 points"\nlist\n')
        canvas = await page.evaluate("""(()=>{const f=document.getElementById('c64'); const c=f.contentWindow.document.getElementById('canvas').getBoundingClientRect(); const fr=f.getBoundingClientRect(); return {x:fr.left+c.left, y:fr.top+c.top, w:c.width, h:c.height}})()""")
        row, col = 4, 4      # the I of PIRNT on the listed line 20
        x = canvas["x"] + (32 + col * 8 + 4) / 384 * canvas["w"]; y = canvas["y"] + (35 + row * 8 + 4) / 270 * canvas["h"]
        await page.keyboard.down("Shift"); await page.mouse.click(x, y); await page.keyboard.up("Shift")
        await page.wait_for_timeout(1200)
        for _ in range(40):   # the cursor blinks by reversing the character under it; catch it "on"
            if await page.evaluate(f"document.getElementById('c64').contentWindow.wasm_peek({0x400 + row * 40 + col}) & 128"): break
            await page.wait_for_timeout(50)
        save(await screen.screenshot(), "shiftclick", 900)
        # Submit, versions, listing
        await typing(page, 'ri\n20 print "9000 points"\n')
        await page.select_option("#exercise", "ch02-ex3")
        await page.click("#submit"); await page.wait_for_timeout(1200)
        await page.click("#submit"); await page.wait_for_timeout(1200)
        top = await page.locator("aside").bounding_box()
        hint = await page.locator("#message").bounding_box()
        save(await page.screenshot(clip={"x": top["x"], "y": top["y"], "width": top["width"], "height": hint["y"] + hint["height"] - top["y"] + 8}), "picker", 700)
        vh = await page.locator("#versions").bounding_box(); lb = await page.locator("#listing-box").bounding_box()
        save(await page.screenshot(clip={"x": top["x"], "y": vh["y"] - 6, "width": top["width"], "height": lb["y"] + lb["height"] - vh["y"] + 14}), "submit", 700)
        # Load: put version 1 back into the C64, which then LISTs it
        await page.click("#versions li:last-child button:has-text('Load')"); await page.wait_for_timeout(7000)
        save(await screen.screenshot(), "load", 900)
        # Chapter work: the quiz
        await page.goto(URL + "/work#ch1"); await page.wait_for_selector("#q1a")
        await page.check("#q1c"); await page.wait_for_timeout(300)
        q = await page.locator("#quiz-section").bounding_box()
        save(await page.screenshot(clip={"x": q["x"] - 10, "y": q["y"], "width": q["width"] + 20, "height": 420}), "work", 800)
        await page.close()
        # Phone with the on-screen keyboard
        phone = await b.new_page(viewport={"width": 412, "height": 900}, device_scale_factor=2, is_mobile=True, has_touch=True)
        await phone.goto(URL + "/login?next=/c64"); await phone.fill("#name", "Ace"); await phone.tap("button[type=submit]"); await phone.wait_for_url(URL + "/c64")
        await phone.wait_for_function("document.getElementById('status').textContent.startsWith('Ready')", timeout=90000)
        await phone.tap("#keyboard"); await phone.wait_for_timeout(3000)
        sb = await phone.locator(".screen").bounding_box(); ub = await phone.locator(".under-screen").bounding_box()
        save(await phone.screenshot(clip={"x": 0, "y": sb["y"] - 8, "width": 412, "height": ub["y"] + ub["height"] - sb["y"] + 16}), "phone", 600)
        await b.close()

asyncio.run(main())
