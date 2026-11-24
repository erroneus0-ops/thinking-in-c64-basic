'use strict';
// If the server says "sign in first", go to the sign-in page and come back.
const _fetch = window.fetch.bind(window);
window.fetch = async (...a) => { const r = await _fetch(...a); if (r.status === 401) location.href = '/login?next=' + encodeURIComponent(location.pathname); return r; };
// The C64 page: boots vc64web with real ROMs, captures the BASIC program
// from emulated memory for Submit, and puts saved versions back for Run.
// vc64web is served from this same server, so this page can call its
// wasm_* functions directly through the iframe.

const frame = document.getElementById('c64');
const statusEl = document.getElementById('status');
const messageEl = document.getElementById('message');
const exerciseEl = document.getElementById('exercise');
const submitBtn = document.getElementById('submit');
const resetBtn = document.getElementById('reset');
const versionsEl = document.getElementById('versions');
const emptyEl = document.getElementById('empty');
const listingBox = document.getElementById('listing-box');
const listingTitle = document.getElementById('listing-title');
const listingEl = document.getElementById('listing');

// ROM file on our server -> the name vc64web uses to recognise it.
const ROMS = [
  ['basic.rom', 'basic.rom'], ['kernal.rom', 'kernal.rom'],
  ['chargen.rom', 'charset.rom'], ['dos1541.rom', '1541.rom'],
];
// BASIC's pointers to the start and end of the program in memory.
const TXTTAB = 0x2b, VARTAB = 0x2d, ARYTAB = 0x2f, STREND = 0x31;
const READY_CODES = [18, 5, 1, 4, 25, 46];   // "READY." in screen codes

let emu = null;   // the emulator's window once it has started

const sleep = ms => new Promise(r => setTimeout(r, ms));
function setStatus(text, bad = false) { statusEl.textContent = text; statusEl.className = bad ? 'bad' : ''; }
function setMessage(text, kind = '') { messageEl.textContent = text; messageEl.className = kind; }

async function waitFor(test, ms, step = 100) {
  for (let t = 0; t < ms; t += step) { try { if (test()) return true; } catch (e) {} await sleep(step); }
  return false;
}
const peek = a => emu.wasm_peek(a);
const peek16 = a => peek(a) | (peek(a + 1) << 8);
function poke16(a, v) { emu.wasm_poke(a, v & 0xff); emu.wasm_poke(a + 1, (v >> 8) & 0xff); }

function screenShowsReady() {
  for (let a = 0x400; a <= 0x7e8 - READY_CODES.length; a++) {
    let k = 0;
    while (k < READY_CODES.length && (peek(a + k) & 0x7f) === READY_CODES[k]) k++;
    if (k === READY_CODES.length) return true;
  }
  return false;
}
function focusC64() {
  frame.focus();
  try { emu.document.getElementById('canvas').focus(); } catch (e) {}
}

// Press a C64 key that has no PC key of its own. vc64web knows these keys by name
// ('runStop', 'restore', 'commodore') but only offers them on its on-screen keyboard.
function c64Key(name) {
  const k = emu.translateKey2(name, '', true);
  return k && k.raw_key ? k.raw_key : null;
}
// vc64web releases every key whenever its window gains or loses focus, so hand focus
// back to the C64 first and let that settle before pressing anything.
async function pressKeys(names, holdMs = 150) {
  const keys = names.map(c64Key).filter(Boolean);
  if (document.activeElement !== frame) { focusC64(); await sleep(150); }
  for (const k of keys) emu.wasm_schedule_key(k[0], k[1], 1, 0);
  await sleep(holdMs);
  for (const k of keys.reverse()) emu.wasm_schedule_key(k[0], k[1], 0, 0);
}
// Same PC keys as VICE: Esc = RUN/STOP, Page Up = RESTORE, Home = CLR/HOME
// (so Shift + Home clears the screen, as SHIFT + CLR/HOME does on a real C64).
function specialKeys(e) {
  if (!emu) return;
  if (e.code === 'Escape') { e.preventDefault(); e.stopPropagation(); pressKeys(['runStop']); }
  else if (e.code === 'PageUp') { e.preventDefault(); e.stopPropagation(); pressKeys(['restore']); }
  else if (e.code === 'Home') { e.preventDefault(); e.stopPropagation(); pressKeys(e.shiftKey ? ['ShiftLeft', 'home'] : ['home']); }
  // The C64's up-arrow key (the power sign, as in 2↑3): vc64web has no PC key for it, so the
  // ^ character (Shift + 6 on most keyboards) presses it.
  else if (e.key === '^') { e.preventDefault(); e.stopPropagation(); pressKeys(['upArrow']); }
  // INSERT: on a C64 it's SHIFT + INST/DEL. vc64web ignores Shift on Backspace (it deletes), so
  // send the real key pair ourselves, for the Insert key and for Shift + Backspace.
  else if (e.code === 'Insert' || (e.code === 'Backspace' && e.shiftKey)) { e.preventDefault(); e.stopPropagation(); pressKeys(['ShiftLeft', 'Backspace']); }
}

// vc64web docks its on-screen keyboard at the bottom of its frame and stacks the C64
// picture on top of it, but only if the frame is tall enough for both. While the
// keyboard is showing, grow the frame to picture + keyboard. The keyboard's own size
// changes a little with the frame's height, so measure and adjust until it settles.
const keyboardBtn = document.getElementById('keyboard');
async function fitFrame() {
  const box = frame.parentElement;
  const kb = emu.$('#virtual_keyboard');
  const open = kb.is(':visible');
  keyboardBtn.textContent = open ? 'Hide keyboard' : 'Show keyboard';
  if (!open) { box.style.height = ''; box.style.aspectRatio = ''; return; }
  // Key size depends on both the frame's width and height, so fit the two together:
  // shrink the keys until the keyboard fits the width, grow the frame until picture
  // and keyboard both fit, and repeat until neither changes.
  const root = emu.document.documentElement;
  const rows = emu.document.getElementById('divKeyboardRows');
  const canvas = emu.document.getElementById('canvas');
  box.style.aspectRatio = 'auto';
  let zoom = parseFloat(root.style.getPropertyValue('--keycap_zoom')) || 1;
  for (let i = 0; i < 10; i++) {
    await sleep(200);
    let changed = false;
    const target = box.getBoundingClientRect().width - 6;
    const w = rows.scrollWidth;
    if (w > target + 1 || (w < target - 25 && zoom < 1)) {
      const z = Math.max(0.4, Math.min(1, Math.floor(zoom * target / w * 100) / 100));
      if (z !== zoom) { zoom = z; root.style.setProperty('--keycap_zoom', zoom.toFixed(2)); changed = true; }
    }
    const want = Math.ceil(canvas.getBoundingClientRect().height + kb.outerHeight() + 4);
    if (Math.abs(box.getBoundingClientRect().height - want) >= 2) { box.style.height = want + 'px'; changed = true; }
    if (!changed) break;
  }
}

// SHIFT+CLICK on the C64 screen moves the cursor there, by feeding cursor keys through the
// C64's own keyboard buffer, so the C64 moves its cursor exactly as if the keys were pressed.
// Only while typing commands: BASIC in direct mode (157 = 128), waiting for input (204 = 0),
// and not in quote mode (212) or insert mode (216), where cursor keys would become characters.
// The visible picture is 384 x 270 C64 pixels with the 320 x 200 text area at (32, 35).
const KEYBUF = 631, KEYCOUNT = 198;
const CRSR = { down: 17, up: 145, right: 29, left: 157 };
let hintTimer = null;
function hint(text) {
  setStatus(text);
  clearTimeout(hintTimer);
  hintTimer = setTimeout(() => setStatus('Ready. Click the C64 screen, then type.'), 4000);
}
async function feedKeys(codes) {
  for (let i = 0; i < codes.length; i += 10) {
    for (let t = 0; t < 40 && peek(KEYCOUNT) !== 0; t++) await sleep(25);   // wait for the buffer to empty
    const chunk = codes.slice(i, i + 10);
    chunk.forEach((c, k) => emu.wasm_poke(KEYBUF + k, c));
    emu.wasm_poke(KEYCOUNT, chunk.length);
  }
}
async function shiftClick(e) {
  if (!e.shiftKey) return;
  e.preventDefault(); e.stopPropagation();
  const r = e.currentTarget.getBoundingClientRect();
  const col = Math.floor(((e.clientX - r.left) / r.width * 384 - 32) / 8);
  const row = Math.floor(((e.clientY - r.top) / r.height * 270 - 35) / 8);
  if (col < 0 || col > 39 || row < 0 || row > 24) return;
  if (peek(157) !== 128 || peek(204) !== 0) { hint('Shift-click moves the cursor while you type commands, not while a program runs.'); return; }
  if (peek(212) !== 0) { hint('Close the quotes first: inside quotes, cursor moves would be typed into your text.'); return; }
  if (peek(216) !== 0) { hint('Finish inserting first: in insert mode, cursor moves would be typed as characters.'); return; }
  const curRow = peek(214), curCol = peek(211) % 40;
  const codes = [];
  const dy = row - curRow, dx = col - curCol;
  for (let i = 0; i < Math.abs(dy); i++) codes.push(dy > 0 ? CRSR.down : CRSR.up);
  for (let i = 0; i < Math.abs(dx); i++) codes.push(dx > 0 ? CRSR.right : CRSR.left);
  await feedKeys(codes);
  focusC64();
}

// ---- Variables, as the C64 knows them ---------------------------------------
// Reads BASIC's own variable list (from the address in 45/46 to the one in 47/48, 7 bytes each)
// and shows each box with the label the C64 actually stored: two letters plus the type mark.
// No translation back to the longer names typed: noticing that is the reader's job.
function c64Number(n) {
  if (n === 0) return '0';
  const a = Math.abs(n);
  if (a >= 1e9 || a < 0.01) {                       // the C64 switches to E notation here
    let [m, e] = n.toExponential(8).split('e');
    m = m.replace(/\.?0+$/, '');
    const ev = parseInt(e, 10);
    return `${m}E${ev < 0 ? '-' : '+'}${String(Math.abs(ev)).padStart(2, '0')}`;
  }
  let t = String(parseFloat(n.toPrecision(9)));
  return t.replace(/^(-?)0\./, '$1.');                // the C64 writes .5, not 0.5
}
function petsciiText(bytes) {
  return bytes.map(b => (b >= 32 && b < 91) ? String.fromCharCode(b) : (b === 92 ? '£' : b === 94 ? '↑' : '·')).join('');
}
// BASIC V2's keywords, in token order from 128 (the same table the C64 uses to store them).
const TOKENS = ['END','FOR','NEXT','DATA','INPUT#','INPUT','DIM','READ','LET','GOTO','RUN','IF','RESTORE',
  'GOSUB','RETURN','REM','STOP','ON','WAIT','LOAD','SAVE','VERIFY','DEF','POKE','PRINT#','PRINT','CONT',
  'LIST','CLR','CMD','SYS','OPEN','CLOSE','GET','NEW','TAB(','TO','FN','SPC(','THEN','NOT','STEP','+','-',
  '*','/','↑','AND','OR','>','=','<','SGN','INT','ABS','USR','FRE','POS','SQR','RND','LOG','EXP','COS',
  'SIN','TAN','ATN','PEEK','LEN','STR$','VAL','ASC','CHR$','LEFT$','RIGHT$','MID$','GO'];
// A function's formula, read from inside the program: from where its box points, up to the
// end of that statement.
function formulaAt(addr) {
  let out = '', quoted = false;
  for (let i = 0; i < 80; i++) {
    const t = peek(addr + i);
    if (t === 0 || (t === 58 && !quoted)) break;
    if (t === 34) quoted = !quoted;
    out += (!quoted && t >= 128 && t - 128 < TOKENS.length) ? TOKENS[t - 128] : (t === 255 ? 'π' : petsciiText([t]));
  }
  return out;
}

// One stored value, decoded. kind: 'number' (5 bytes), 'whole number' (2 bytes, high first),
// 'text' (length + address of the characters).
function decodeValue(kind, a) {
  if (kind === 'number') {
    const e = peek(a); if (!e) return '0';
    const m1 = peek(a + 1);
    const mant = ((m1 | 128) * 2 ** 24 + peek(a + 2) * 2 ** 16 + peek(a + 3) * 2 ** 8 + peek(a + 4)) / 2 ** 32;
    return c64Number((m1 & 128 ? -1 : 1) * mant * 2 ** (e - 128));
  }
  if (kind === 'whole number') { let v = (peek(a) << 8) | peek(a + 1); if (v > 32767) v -= 65536; return String(v); }
  const len = peek(a), ptr = peek(a + 1) | (peek(a + 2) << 8);
  return '"' + petsciiText([...Array(len)].map((_, i) => peek(ptr + i))) + '"';
}

// Arrays live in their own list after the simple variables (from 47/48 to 49/50). Each starts
// with its name, its total size, how many dimensions, and each dimension's size, stored LAST
// dimension first. The boxes follow, with the FIRST index changing fastest.
function readArrays() {
  const out = []; let a = peek16(47); const end = peek16(49);
  while (a + 5 <= end && out.length < 20) {
    const b0 = peek(a), b1 = peek(a + 1), total = peek(a + 2) | (peek(a + 3) << 8), n = peek(a + 4);
    if (!total) break;
    const kind = !(b0 & 128) && !(b1 & 128) ? 'number' : !(b0 & 128) ? 'text' : 'whole number';
    const size = { number: 5, text: 3, 'whole number': 2 }[kind];
    const stored = [...Array(n)].map((_, i) => (peek(a + 5 + 2 * i) << 8) | peek(a + 6 + 2 * i));
    const dims = stored.slice().reverse();                   // as written in DIM: first index first
    const name = String.fromCharCode(b0 & 127) + ((b1 & 127) ? String.fromCharCode(b1 & 127) : '');
    const first = a + 5 + 2 * n, count = dims.reduce((x, y) => x * y, 1);
    const at = (idx) => {                                     // idx = [i, j, ...] -> address
      let off = 0, mul = 1;
      for (let k = 0; k < idx.length; k++) { off += idx[k] * mul; mul *= dims[k]; }
      return first + off * size;
    };
    out.push({ label: name + { number: '', text: '$', 'whole number': '%' }[kind] + '()', kind, dims, count,
               value: (...idx) => decodeValue(kind, at(idx)) });
    a += total;
  }
  return out;
}

function readVariables() {
  const start = peek16(45), end = peek16(47), out = [];
  for (let a = start; a + 7 <= end && out.length < 200; a += 7) {
    const b = [...Array(7)].map((_, i) => peek(a + i));
    const n1 = b[0] & 127, n2 = b[1] & 127, hi1 = b[0] & 128, hi2 = b[1] & 128;
    const name = String.fromCharCode(n1) + (n2 ? String.fromCharCode(n2) : '');
    if (!hi1 && !hi2) {                                  // number: 5-byte floating point
      let v = 0;
      if (b[2]) {
        const mant = ((b[3] | 128) * 2 ** 24 + b[4] * 2 ** 16 + b[5] * 2 ** 8 + b[6]) / 2 ** 32;
        v = (b[3] & 128 ? -1 : 1) * mant * 2 ** (b[2] - 128);
      }
      out.push({ label: name, type: 'number', value: c64Number(v) });
    } else if (!hi1 && hi2) {                            // string: length + address of the text
      const len = b[2], ptr = b[3] | (b[4] << 8);
      out.push({ label: name + '$', type: 'text', value: '"' + petsciiText([...Array(len)].map((_, i) => peek(ptr + i))) + '"' });
    } else if (hi1 && hi2) {                             // whole number: high byte first
      let v = (b[2] << 8) | b[3]; if (v > 32767) v -= 65536;
      out.push({ label: name + '%', type: 'whole number', value: String(v) });
    } else {
      // A function box holds where its formula is, and which box is its parameter.
      const par = b[4] | (b[5] << 8);
      const pn = String.fromCharCode(peek(par - 2) & 127) + ((peek(par - 1) & 127) ? String.fromCharCode(peek(par - 1) & 127) : '');
      out.push({ label: 'FN ' + name, type: 'function', value: `(${pn}) = ${formulaAt(b[2] | (b[3] << 8))}` });
    }
  }
  return out;
}

// The shelf panel: refreshed twice a second while open, so values change as a program runs.
const shelf = document.getElementById('shelf'), boxesEl = document.getElementById('boxes');
const varsBtn = document.getElementById('vars-btn');
let shelfTimer = null, lastShelf = '';
// Four cabinets, one per kind of box, always shown (an empty one invites the question
// "what goes in here?"). Boxes keep the order the C64 created them in.
const CABINETS = [
  { type: 'number', title: 'Numbers' },
  { type: 'text', title: 'Text ($)' },
  { type: 'whole number', title: 'Whole numbers (%)' },
  { type: 'function', title: 'Functions (FN)' },
];
function drawArray(arr) {
  const MAX = 121;   // up to an 11 x 11 grid; bigger arrays show their first boxes
  const box = el('div', { className: 'array' },
    el('div', { className: 'label', textContent: arr.label }),
    el('div', { className: 'dims', textContent: arr.dims.map(d => `0 to ${d - 1}`).join(', ') }));
  if (arr.dims.length === 2 && arr.dims[0] <= 11 && arr.dims[1] <= 11) {
    const [rows, cols] = arr.dims;
    const table = el('table', { className: 'grid' },
      el('tr', {}, el('th', {}), ...[...Array(cols)].map((_, j) => el('th', { textContent: j }))),
      ...[...Array(rows)].map((_, i) => el('tr', {}, el('th', { textContent: i }),
        ...[...Array(cols)].map((_, j) => el('td', { textContent: arr.value(i, j) })))));
    box.append(el('div', { className: 'grid-wrap' }, table));
  } else {
    const cells = el('div', { className: 'cells' });
    for (let k = 0; k < Math.min(arr.count, MAX); k++) {
      const idx = []; let r = k;
      for (const d of arr.dims) { idx.push(r % d); r = Math.floor(r / d); }
      cells.append(el('div', { className: 'cell' }, el('span', { className: 'idx', textContent: idx.join(',') }),
                                                    el('span', { textContent: arr.value(...idx) })));
    }
    box.append(cells);
    if (arr.count > MAX) box.append(el('p', { className: 'none', textContent: `…and ${arr.count - MAX} more boxes` }));
  }
  return box;
}
function drawShelf() {
  const vars = readVariables();
  const arrays = readArrays();
  const key = JSON.stringify([vars, arrays.map(a => [a.label, a.dims, a.value(...a.dims.map(() => 0)),
    [...Array(Math.min(a.count, 121))].map((_, k) => { const idx = []; let r = k; for (const d of a.dims) { idx.push(r % d); r = Math.floor(r / d); } return a.value(...idx); })])]);
  if (key === lastShelf) return;          // only redraw when something changed
  lastShelf = key;
  boxesEl.replaceChildren(...CABINETS.map(cab => {
    const mine = vars.filter(v => v.type === cab.type);
    return el('section', { className: 'cabinet' },
      el('h3', { textContent: cab.title }),
      el('div', { className: 'drawers' }, ...(mine.length
        ? mine.map(v => el('div', { className: 'box' },
            el('div', { className: 'label', textContent: v.label }),
            el('div', { className: 'value', textContent: v.value })))
        : [el('p', { className: 'none', textContent: 'Empty' })])));
  }), el('section', { className: 'cabinet arrays' },
    el('h3', { textContent: 'Arrays' }),
    ...(arrays.length ? arrays.map(drawArray) : [el('p', { className: 'none', textContent: 'Empty' })])));
}
function el(tag, props = {}, ...kids) { const e = document.createElement(tag); Object.assign(e, props); e.append(...kids); return e; }
varsBtn.onclick = () => {
  shelf.hidden = !shelf.hidden;
  varsBtn.textContent = shelf.hidden ? 'Show variables' : 'Hide variables';
  clearInterval(shelfTimer);
  if (!shelf.hidden) { lastShelf = ''; drawShelf(); shelfTimer = setInterval(drawShelf, 500); }
  focusC64();
};

async function boot() {
  const config = { navbar: false, dialog_on_missing_roms: false, dialog_on_disk: false };
  frame.src = '/emu/index.html#' + encodeURIComponent(JSON.stringify(config));
  const started = await waitFor(() => typeof frame.contentWindow.wasm_loadfile === 'function'
                                   && typeof frame.contentWindow.wasm_peek === 'function', 60000);
  if (!started) { setStatus('The emulator didn’t start. Check that setup has been run, then reload the page.', true); return; }
  emu = frame.contentWindow;
  emu.addEventListener('keydown', specialKeys, true);
  emu.document.getElementById('canvas').addEventListener('click', shiftClick, true);
  window.addEventListener('keydown', specialKeys, true);
  for (const [file, name] of ROMS) {
    const res = await fetch('/roms/' + file);
    if (!res.ok) { setStatus(`The C64 ROM file ${file} is missing. Run setup.bat again, then reload.`, true); return; }
    const bytes = new Uint8Array(await res.arrayBuffer());
    emu.wasm_loadfile(name, bytes, bytes.byteLength, 8);
  }
  await resetAndWait();
  submitBtn.disabled = false; resetBtn.disabled = false;
  for (const b of document.querySelectorAll('[data-keys]')) b.disabled = false;
  emu.$('#virtual_keyboard').on('shown.bs.collapse hidden.bs.collapse', fitFrame);
  window.addEventListener('resize', () => setTimeout(fitFrame, 200));
  keyboardBtn.disabled = false;
  varsBtn.disabled = false;
  setStatus('Ready. Click the C64 screen, then type.');
  focusC64();
}

async function resetAndWait() {
  emu.wasm_reset();
  await sleep(400);
  const ok = await waitFor(screenShowsReady, 15000);
  if (!ok) setStatus('The C64 didn’t reach READY. Try Reset, or reload the page.', true);
  return ok;
}

// Copy the BASIC program out of memory as a PRG: load address + bytes.
function captureProgram() {
  const start = peek16(TXTTAB), end = peek16(VARTAB);
  if (end <= start + 2) return null;
  const prg = new Uint8Array(end - start + 2);
  prg[0] = start & 0xff; prg[1] = start >> 8;
  for (let i = 0; i < end - start; i++) prg[i + 2] = peek(start + i);
  return prg;
}
function toBase64(bytes) {
  let s = '';
  for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  return btoa(s);
}

async function submit() {
  const prg = captureProgram();
  if (!prg) { setMessage('There’s no program in memory yet. Type a line with a line number first.', 'bad'); return; }
  submitBtn.disabled = true;
  try {
    const res = await fetch('/api/submit', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exercise: exerciseEl.value, prg: toBase64(prg), capture: 'memory' }),
    });
    const out = await res.json();
    if (!res.ok) { setMessage(out.error || 'Submit failed.', 'bad'); return; }
    setMessage(`Saved as version ${out.version} (${out.lines} ${out.lines === 1 ? 'line' : 'lines'}).`, 'good');
    await showVersions();
    showListing(out.id, out.version);
  } catch (e) {
    setMessage('Couldn’t reach the course server. Is start.bat still running?', 'bad');
  } finally { submitBtn.disabled = false; focusC64(); }
}

// Put a saved version into a freshly reset C64, then type RUN or LIST.
async function putBack(id, command) {
  const res = await fetch('/api/prg/' + id);
  if (!res.ok) { setMessage('That version couldn’t be loaded.', 'bad'); return; }
  const prg = new Uint8Array(await res.arrayBuffer());
  setMessage('Resetting the C64…');
  if (!(await resetAndWait())) return;
  const load = prg[0] | (prg[1] << 8);
  for (let i = 2; i < prg.length; i++) emu.wasm_poke(load + i - 2, prg[i]);
  const end = load + prg.length - 2;
  poke16(TXTTAB, load); poke16(VARTAB, end); poke16(ARYTAB, end); poke16(STREND, end);
  emu.wasm_auto_type(command.toLowerCase() + '\n');   // lowercase types as normal C64 letters
  setMessage('');
  setStatus('Ready. Click the C64 screen, then type.');
  focusC64();
}

async function showListing(id, version) {
  const res = await fetch('/api/listing/' + id);
  listingEl.textContent = await res.text();
  listingTitle.textContent = `Listing of version ${version}`;
  listingBox.hidden = false;
}

async function showVersions() {
  const res = await fetch('/api/versions?exercise=' + encodeURIComponent(exerciseEl.value));
  const rows = await res.json();
  versionsEl.replaceChildren();
  emptyEl.hidden = rows.length > 0;
  for (const r of rows) {
    const li = document.createElement('li');
    const what = document.createElement('span');
    what.className = 'what';
    what.textContent = `Version ${r.version}`;
    const small = document.createElement('small');
    small.textContent = `${r.lines} ${r.lines === 1 ? 'line' : 'lines'}, ${r.created_at}`;
    what.append(small);
    const mk = (label, fn) => { const b = document.createElement('button'); b.textContent = label; b.onclick = fn; return b; };
    li.append(what,
      mk('Run', () => putBack(r.id, 'RUN')),
      mk('Load', () => putBack(r.id, 'LIST')),
      mk('Listing', () => showListing(r.id, r.version)));
    versionsEl.append(li);
  }
}

async function loadExercises() {
  const list = await (await fetch('/api/exercises')).json();
  for (const ex of list) exerciseEl.append(new Option(ex.title, ex.id));
  exerciseEl.onchange = () => { listingBox.hidden = true; setMessage(''); showVersions(); };
  await showVersions();
}

submitBtn.onclick = submit;
keyboardBtn.onclick = () => {
  emu.$('#virtual_keyboard').collapse('toggle');
  frame.parentElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
};
for (const b of document.querySelectorAll('[data-keys]')) b.onclick = () => pressKeys(b.dataset.keys.split(' '));
resetBtn.onclick = async () => { setMessage(''); await resetAndWait(); setStatus('Ready. Click the C64 screen, then type.'); focusC64(); };
loadExercises();
boot();
