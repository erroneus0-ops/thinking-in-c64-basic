'use strict';
// If the server says "sign in first", go to the sign-in page and come back.
const _fetch = window.fetch.bind(window);
window.fetch = async (...a) => { const r = await _fetch(...a); if (r.status === 401) location.href = '/login?next=' + encodeURIComponent(location.pathname); return r; };
// Chapter work: exercises (written answers), the quiz, and beta tester notes.
// Everything is saved to the course database on this computer.

const chapterEl = document.getElementById('chapter');
let chapters = [];
let saved = {};   // latest save per kind:item: { text, at }

const el = (tag, props = {}, ...kids) => {
  const e = document.createElement(tag);
  Object.assign(e, props);
  for (const k of kids) e.append(k);
  return e;
};

async function save(chapter, kind, item, text) {
  const res = await fetch('/api/response', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chapter, kind, item, text }),
  });
  if (!res.ok) throw new Error('save failed');
  saved[kind + ':' + item] = { text, at: 'just now' };
}

// Each pass starts with an empty box; the previous answer is shown underneath for comparison.
function lastTime(key) {
  const prev = saved[key];
  if (!prev || !prev.text) return el('span');
  return el('p', { className: 'last' }, el('strong', { textContent: `Last time (${prev.at}): ` }), prev.text);
}

// A save button with its own little "Saved" message.
function saveRow(onSave) {
  const btn = el('button', { type: 'button', textContent: 'Save' });
  const msg = el('span', { className: 'saved', role: 'status' });
  btn.onclick = async () => {
    btn.disabled = true; msg.textContent = '';
    try { await onSave(); msg.className = 'saved'; msg.textContent = 'Saved.'; }
    catch (e) { msg.className = 'bad'; msg.textContent = 'Couldn’t save. Is start.bat still running?'; }
    finally { btn.disabled = false; }
  };
  return el('div', { className: 'save-row' }, btn, msg);
}

// For an exercise that asks for a program: has one been saved to a slot? Shows the newest slot and
// its first line (so a wrong program stands out), or a reminder of how to save one.
function slotStatus(ch, ex) {
  const box = el('p', { className: 'slot-status' }, 'Checking your save slots…');
  fetch('/api/versions?exercise=' + encodeURIComponent(ex.slot_id)).then(r => r.json()).then(rows => {
    if (!rows.length) {
      box.className = 'slot-status missing';
      box.textContent = `No program saved for this exercise yet. On the C64, choose “${ch.n === 0 ? 'Before you begin' : 'Chapter ' + ch.n}, exercise ${ex.n}” in the Exercise list, then press Save to a new slot.`;
      return;
    }
    const newest = rows[0], first = newest.first || '';
    box.className = 'slot-status saved';
    box.textContent = `Saved: slot ${newest.version}, ${newest.created_at}. It starts: ${first}`;
  }).catch(() => { box.textContent = ''; });
  return box;
}

function renderExercises(ch) {
  const box = document.getElementById('exercises');
  box.replaceChildren();
  document.getElementById('exercises-section').hidden = !ch.exercises.length;
  for (const ex of ch.exercises) {
    const id = ex.id || `ex${ex.n}`;   // the id changes when the exercise is rewritten
    const ta = el('textarea', { id: `t-${id}` });
    box.append(el('div', { className: 'card' },
      el('h3', { textContent: `${ex.n}. ${ex.title}` }),
      el('p', { textContent: ex.text }),
      saved['exercise:' + id] && saved['exercise:' + id].text
        ? el('p', { className: 'again', textContent: 'You’ve solved this before. This time, find a different answer that still works.' })
        : el('span'),
      el('label', { className: 'small', htmlFor: ta.id, textContent: 'Your answer' }), ta,
      lastTime('exercise:' + id),
      saveRow(() => save(ch.n, 'exercise', id, ta.value)),
      ex.program ? slotStatus(ch, ex) : el('span')));
  }
}

async function renderQuiz(ch) {
  const form = document.getElementById('quiz');
  document.getElementById('quiz-section').hidden = !ch.quiz.length;
  document.getElementById('score').textContent = '';
  form.replaceChildren();
  if (!ch.quiz.length) return;
  for (const q of ch.quiz) {
    const fs = el('fieldset', { className: 'card' }, el('legend', { textContent: `${q.n}. ${q.question}` }));
    for (const o of q.options) {
      const id = `q${q.n}${o.letter}`;
      fs.append(el('div', { className: 'opt' },
        el('input', { type: 'radio', name: `q${q.n}`, id, value: o.letter }),
        el('label', { htmlFor: id, textContent: `(${o.letter}) ${o.text}` })));
    }
    fs.append(el('div', { className: 'result', id: `r${q.n}` }));
    form.append(fs);
  }
  const submit = el('button', { type: 'submit', className: 'primary', textContent: 'Check my answers' });
  form.append(submit);
  form.onsubmit = async (e) => {
    e.preventDefault();
    const answers = {};
    for (const q of ch.quiz) {
      const picked = form.querySelector(`input[name="q${q.n}"]:checked`);
      if (picked) answers[q.n] = picked.value;
    }
    submit.disabled = true;
    try {
      const res = await fetch('/api/quiz', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chapter: ch.n, answers }) });
      const out = await res.json();
      if (!res.ok || !out.results) {
        document.getElementById('score').textContent = (out && out.error) ? out.error : 'That quiz couldn’t be saved. Is start.bat still running?';
        return;
      }
      for (const r of out.results) {
        const box = document.getElementById(`r${r.n}`);
        box.className = 'result ' + (r.correct ? 'good' : 'bad');
        box.textContent = r.correct ? 'Right.' : (r.choice ? 'Not quite. Think it through, and try again any time.' : 'Skipped.');
      }
      document.getElementById('score').textContent = `You got ${out.score} out of ${out.total}. Try again any time; every attempt is kept.`;
      await renderHistory(ch);
    } catch (err) {
      document.getElementById('score').textContent = 'That quiz couldn’t be saved. Is start.bat still running?';
    } finally { submit.disabled = false; }
  };
  await renderHistory(ch);
}

async function renderHistory(ch) {
  const rows = await (await fetch('/api/quiz-history?chapter=' + ch.n)).json();
  const box = document.getElementById('history');
  box.replaceChildren();
  if (!rows.length) return;
  box.append(el('p', { className: 'quiet', textContent: 'Earlier attempts:' }),
    el('ul', { className: 'history' }, ...rows.map(r => el('li', { textContent: `${r.score} out of ${r.total}, ${r.created_at}` }))));
}

function renderNotes(ch) {
  const box = document.getElementById('notes');
  box.replaceChildren();
  if ((ch.questions || []).length) {
    const card = el('div', { className: 'card asks' }, el('h3', { textContent: 'Questions for you, from the editor' }));
    const fields = ch.questions.map(q => {
      const ta = el('textarea', { id: `n-${q.id}` });
      return { q, ta, nodes: [el('p', { textContent: `${q.n}. ${q.text}` }), ta, lastTime('note:' + q.id)] };
    });
    fields.forEach(f => card.append(...f.nodes));
    card.append(saveRow(async () => { for (const f of fields) if (f.ta.value.trim()) await save(ch.n, 'note', f.q.id, f.ta.value); }));
    box.append(card);
  }
  for (const lesson of ch.lessons) {
    const label = /^\d/.test(lesson.id) ? `Lesson ${lesson.id}: ${lesson.title}` : lesson.title;
    // Short questions that ask for a real answer, not a yes or no (editor's decision).
    const fields = ['explain', 'reaction'].map(kind => {
      const item = `${lesson.id}:${kind}`;
      const ta = el('textarea', { id: `n-${item}` });
      ta.style.minHeight = '3.6rem';
      const prompt = { explain: 'Explain this lesson’s big idea in your own words.',
                       reaction: 'What surprised you, confused you, or dragged? Tell me why.' }[kind];
      return { item, ta, nodes: [el('label', { className: 'small', htmlFor: ta.id, textContent: prompt }), ta, lastTime('note:' + item)] };
    });
    box.append(el('div', { className: 'card' },
      el('h3', { textContent: label }),
      ...fields.flatMap(f => f.nodes),
      saveRow(async () => { for (const f of fields) if (f.ta.value.trim()) await save(ch.n, 'note', f.item, f.ta.value); })));
  }
}

async function show() {
  const ch = chapters.find(c => String(c.n) === chapterEl.value);
  const rows = await (await fetch('/api/responses?chapter=' + ch.n)).json();
  saved = {};
  for (const r of rows) saved[r.kind + ':' + r.item] = { text: r.text, at: r.created_at };
  document.body.classList.toggle('testing', ch.status === 'testing');
  document.getElementById('testing-note').hidden = ch.status !== 'testing';
  renderExercises(ch);
  await renderQuiz(ch);
  renderNotes(ch);
  history.replaceState(null, '', '#ch' + ch.n);
}

// Inside the study view the C64 is already on screen beside the workbook: links to it become plain text.
if (document.documentElement.classList.contains('embed')) {
  for (const a of document.querySelectorAll('a[href="/c64"]')) a.replaceWith(document.createTextNode(a.textContent));
}

(async () => {
  chapters = await (await fetch('/api/chapters')).json();
  for (const c of chapters) chapterEl.append(new Option((c.n === 0 ? c.title : `Chapter ${c.n}: ${c.title}`) + (c.status === 'testing' ? ' (in testing)' : ''), c.n));
  const fromHash = (location.hash.match(/^#ch(\d+)$/) || [])[1];
  chapterEl.value = fromHash ?? (chapters.find(c => c.n === 1) ? '1' : String(chapters[0].n));
  chapterEl.onchange = show;
  show();
})();
