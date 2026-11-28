"""Run BASIC on the course site's C64 without typing it: lines are tokenized here (by the C64's own
rules) and placed in memory, then only RUN is typed. Used to verify the reference's examples.
Needs the course site on 127.0.0.1:8064 and Playwright."""
import asyncio, json, pathlib

TOKENS = ['END','FOR','NEXT','DATA','INPUT#','INPUT','DIM','READ','LET','GOTO','RUN','IF','RESTORE',
  'GOSUB','RETURN','REM','STOP','ON','WAIT','LOAD','SAVE','VERIFY','DEF','POKE','PRINT#','PRINT','CONT',
  'LIST','CLR','CMD','SYS','OPEN','CLOSE','GET','NEW','TAB(','TO','FN','SPC(','THEN','NOT','STEP','+','-',
  '*','/','^','AND','OR','>','=','<','SGN','INT','ABS','USR','FRE','POS','SQR','RND','LOG','EXP','COS',
  'SIN','TAN','ATN','PEEK','LEN','STR$','VAL','ASC','CHR$','LEFT$','RIGHT$','MID$','GO']

def crunch(text):
    """Tokenize one line's text as the C64 does: outside quotes, try keywords in table order at each
    position (first match wins); after DATA or REM, store the rest as typed. ? means PRINT."""
    text = text.upper().replace('↑', '^')
    out, i, quoted, raw = [], 0, False, False
    while i < len(text):
        c = text[i]
        if c == '"':
            quoted = not quoted
        if quoted or raw or c == ' ' or c == '"':
            out.append(ord(c)); i += 1; continue
        if c == '?':
            out.append(0x99); i += 1; continue
        for n, kw in enumerate(TOKENS):
            if text.startswith(kw, i):
                out.append(0x80 + n); i += len(kw)
                if kw in ('DATA', 'REM'): raw = True
                break
        else:
            out.append(ord(c)); i += 1
    return out

def prg(lines, load=0x0801):
    """lines: list of (number, text). Returns PRG bytes: load address, linked lines, end marker."""
    body, addr = [], load
    for num, text in lines:
        data = [num & 255, num >> 8] + crunch(text) + [0]
        nxt = addr + 2 + len(data)
        body += [nxt & 255, nxt >> 8] + data
        addr = nxt
    return bytes([load & 255, load >> 8] + body + [0, 0])

SCREEN = """() => { const w=document.getElementById('c64').contentWindow; const rows=[];
  for (let r=0;r<25;r++){ let s=''; for (let c=0;c<40;c++){ const v=w.wasm_peek(0x400+r*40+c)&0x7f;
    s += v===32?' ': v===0?'@': v<27?String.fromCharCode(64+v): v===27?'[': v===29?']': v===30?'↑': v<64?String.fromCharCode(v):'#'; }
    rows.push(s.replace(/\\s+$/,'')); } return rows; }"""

class C64:
    async def open(self, chrome=None, url="http://127.0.0.1:8064"):
        from playwright.async_api import async_playwright
        self.pw = await async_playwright().start()
        self.b = await (self.pw.chromium.launch(executable_path=chrome) if chrome else self.pw.chromium.launch())
        self.page = await self.b.new_page(viewport={"width": 1280, "height": 900})
        await self.page.goto(url + "/login?next=/c64"); await self.page.fill("#name", "Verifier")
        await self.page.click("button[type=submit]"); await self.page.wait_for_url(url + "/c64")
        await self.page.wait_for_function("document.getElementById('status').textContent.startsWith('Ready')", timeout=90000)
        await self.page.wait_for_timeout(500)
        return self

    async def run(self, lines, wait=1500):
        """Put a program in memory (after a clear-screen first line), type RUN, return the output rows."""
        data = list(prg([(1, 'PRINT CHR$(147);')] + lines))
        await self.page.evaluate("""(d) => { const w=document.getElementById('c64').contentWindow;
            const load=d[0]|(d[1]<<8); for (let i=2;i<d.length;i++) w.wasm_poke(load+i-2, d[i]);
            const end=load+d.length-2; const p=(a,v)=>{w.wasm_poke(a,v&255);w.wasm_poke(a+1,v>>8);};
            p(43,load); p(45,end); p(47,end); p(49,end); w.wasm_auto_type('run\\n'); }""", data)
        await self.page.wait_for_timeout(wait)
        return [r for r in await self.page.evaluate(SCREEN) if r and r != 'READY.']

    async def peek(self, start, count):
        """Read count bytes of C64 memory from start."""
        return await self.page.evaluate("""([s, n]) => { const w=document.getElementById('c64').contentWindow;
            return Array.from({length: n}, (_, i) => w.wasm_peek(s + i)); }""", [start, count])

    async def close(self):
        await self.b.close(); await self.pw.stop()
