"""Type every abbreviation into the course site's C64 and check LIST expands it to the right
keyword. Needs the site running on 127.0.0.1:8064 (start.bat), Playwright, and abbr.json from
tools/compute_abbreviations.py. Reads the LAST row starting with '10 ' (the LIST output, not the
typed line, which shows the shifted letter as a graphics character)."""
import asyncio, json
from playwright.async_api import async_playwright
abbr = json.load(open('abbr.json'))
SCR = """() => { const w=document.getElementById('c64').contentWindow; let rows=[];
 for(let r=0;r<25;r++){let s='';for(let c=0;c<40;c++){let v=w.wasm_peek(0x400+r*40+c)&0x7f;
 s+= v===32?' ': v===30?'^': v<27&&v>0?String.fromCharCode(64+v): v<64?String.fromCharCode(v):'#';} rows.push(s.replace(/\\s+$/,''));}
 return rows;}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width":1280,"height":900})
        await page.goto("http://127.0.0.1:8064/login?next=/c64"); await page.fill("#name","Tester"); await page.click("button[type=submit]")
        await page.wait_for_url("http://127.0.0.1:8064/c64")
        await page.wait_for_function("document.getElementById('status').textContent.startsWith('Ready')", timeout=90000)
        t = lambda x: page.evaluate("document.getElementById('c64').contentWindow.wasm_auto_type(%r)" % x)
        bad = []; n = 0
        for k, ab in abbr.items():
            await page.click("button[data-keys='ShiftLeft home']"); await page.wait_for_timeout(250)
            await t(f'new\n10 {ab}\nlist\n'); await page.wait_for_timeout(1300)
            rows = await page.evaluate(SCR)
            line = ([r for r in rows if r.startswith('10 ')] or ['(missing)'])[-1]
            if line != f'10 {k}': bad.append((k, ab, line))
            n += 1
        print(f"verified {n-len(bad)} of {n}")
        for x in bad: print("MISMATCH", x)
        await b.close()
asyncio.run(main())
