// The C64 page: boots vc64web with real ROMs, captures the BASIC program
// from emulated memory for Submit, and puts saved versions back for Run.
// vc64web is served from this same server, so this page can call its
// wasm_* functions directly through the iframe.
'use strict';

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

async function boot() {
  const config = { navbar: false, dialog_on_missing_roms: false, dialog_on_disk: false };
  frame.src = '/emu/index.html#' + encodeURIComponent(JSON.stringify(config));
  const started = await waitFor(() => typeof frame.contentWindow.wasm_loadfile === 'function'
                                   && typeof frame.contentWindow.wasm_peek === 'function', 60000);
  if (!started) { setStatus('The emulator didn’t start. Check that setup has been run, then reload the page.', true); return; }
  emu = frame.contentWindow;
  for (const [file, name] of ROMS) {
    const res = await fetch('/roms/' + file);
    if (!res.ok) { setStatus(`The C64 ROM file ${file} is missing. Run setup.bat again, then reload.`, true); return; }
    const bytes = new Uint8Array(await res.arrayBuffer());
    emu.wasm_loadfile(name, bytes, bytes.byteLength, 8);
  }
  await resetAndWait();
  submitBtn.disabled = false; resetBtn.disabled = false;
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
resetBtn.onclick = async () => { setMessage(''); await resetAndWait(); setStatus('Ready. Click the C64 screen, then type.'); focusC64(); };
loadExercises();
boot();
