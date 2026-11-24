# Handoff notes

Read this first in every new session. Update it at the end of each session.

## Privacy rule

This repo is PUBLIC. Describing the target audience is fine. Never name the student
or say how he is related to anyone on the project.

## Target audience

A young adult beginner with no programming experience. Bright and strong in spatial
reasoning; good at video games; easily distracted, so lessons are short and every
lesson ends with something that runs. Basic math and logic are reasonable but benefit
from extra practice and repetition. Interested in writing fiction (hence the Story
Engine project). The goal is less "learn C64 BASIC" than "use programming to build
organized, orderly thinking habits."

## People and roles

- **Repo owner** (`erroneus0-ops`): editor. Decides platform and content questions.
- **Claude**: C64 subject expert and author. Works through the machine account
  `C64BookDev`, scoped to this one repo
  (see the owner's `MACHINE_ACCOUNT_SETUP_GUIDE.md` in `erroneus0-ops/WebUI-debug-dev`).

## Where things are

- Book plan, editing copy: the Claude Doc "Thinking in C64 BASIC — Book Plan &
  Chapter 1 Draft" (https://claude.ai/artifact/PJj9Ywwp1HJwWLtHqncpUm). The editor edits and
  comments there while the plan is in flux.
- `book/plan.md`: snapshot of that doc (re-export after changes; drop the byline line).
  The Claude Doc is the source of truth for the plan.
- `book/chapters/NN-name.md`: the book itself, one file per chapter. These are the source
  of truth for chapter text (Chapter 1 now lives here, not in the plan).
- Public site (student edition, no answers): GitHub Pages from the `docs/` folder.
- Editor's edition (with answers), password-locked on GitHub Pages: .../thinking-in-c64-basic/editor/
  The password is NEVER in the repo; ask the editor for it in each new session. (The old claude.ai
  preview link is retired.)

## The C64 tour (docs/tour/)

Twelve slides introducing the C64 and the course site (the submission guide is three slides: pick the
exercise, Submit saves a new version, Run/Load/Listing; expanded at the editor's request), linked from the top of the book's HTML editions
as "New to the Commodore 64 and the emulator? Take the quick tour" (not in the PDF; editor's choice).
Slide text lives in `tools/build_tour.py`; real screenshots in `tools/tour_shots/`, captured by
`tools/capture_tour.py` from the running course site (needs runtime/, Playwright, Pillow). After the
site's look changes: capture, then `python tools/build_tour.py`, and commit docs/tour/.

## Building the book

`pip install -r tools/requirements.txt`, then `python tools/build.py` (editor's edition,
answers shown, output in `build/`) or `python tools/build.py --student --pages` (answers
removed, written to `docs/` for the public site). Then lock the editor's edition:
`python tools/build.py --no-pdf` followed by `python tools/lock_editor.py` (password from the
C64BOOK_PASSWORD environment variable, or asked for; AES-256-GCM, PBKDF2-SHA256 600k rounds;
writes docs/editor/index.html). Commit `docs/` after building. Note: the quiz answers are still
readable in the public chapter sources (honor system, by the editor's decision). Pandoc Markdown; template and styles in `tools/template.html`.

Content ideas from the editor (to place in chapters):
- SECRETS: catalog in `book/secrets.md` (43 entries, status and proposed chapter for each).
  Placed ones get marked there. Unplaced ones form the appendix.
- PLANNED CHAPTER (editor approved): "Detective Work", right after Ch 11 Program Maps (book becomes
  23 chapters; later chapters shift by one). Tools in rising order: reading the error; playing
  computer with a trace table (one column per variable, one row per step; suits spatial strength);
  print probes in a reserved line range; STOP/PRINT/CONT breakpoints; testing one block alone
  (editor's GOTO technique; game picture: speedrunner practicing a segment from a save state);
  splitting the search in halves with STOP. Plus a thread in every chapter: "an error is a clue".
- PLANNED TOOL (editor approved), build alongside Ch 11, not before: block-aware RENUMBER on the C64
  page. Start/step fields; rewrites GOTO, GOSUB, THEN n, ON..GOTO/GOSUB lists, RUN n, LIST n in
  programs; lists computed jumps (GOTO X) it can't fix; before/after preview; saves as a new version.
  Block markers are the Ch 11 REM headers (e.g. `1000 REM ===== MENU =====`): blocks keep their
  hundreds/thousands. Editor's additions from his CoCo 3 experience (RENUM was "simple only"):
  DATA regions stay together; important subroutines can be PINNED so they never move. Teach it in
  Ch 11 AFTER he has felt the pain of renumbering by hand; present it honestly as what C64
  programmers added via cartridges and BASIC extensions (the C64 itself had no RENUMBER).
- Ch 11: "test one neighborhood at a time": set variables by hand, `GOTO` the block's first line
  (keeps variables; RUN n wipes them, tested), `STOP` at the block's end, PRINT to check, CONT.
  The editor's own habit, told as a parenthetical anecdote.
- Reserved words: Ch 1 Lesson 1.4 (editor asked for a briefing so names don't feel like a minefield).
  Key safe rule (tested): any two-letter name is safe except IF ON OR TO GO FN ST TI.
- INTEGERS AND BINARY (editor's plan): Ch 1 keeps "whole numbers", with one parenthetical naming them
  "signed integers" (done, Lesson 1.2). Ch 7 teaches boolean logic (AND, OR, NOT; true = -1, tested).
  The sprite chapter teaches binary AS A PICTURE: rows of pixels on graph paper become numbers (8
  squares = one byte); then 16 squares = one integer explains the -32768..32767 range in a sentence.
  Leave the -1 = all sixteen bits on connection (why AND/OR work on bits) as an earned discovery.
- Ch 3 must teach that RND(1) repeats after every reset (tested); the opener now hints at it.
- The ↑ (power) key: `^` on a PC keyboard types nothing in the browser emulator. Solve before Ch 3.
- OPENER (editor's decision): the book's first page is the classic one-line maze,
  10 PRINT CHR$(205.5 + RND(1)); / 20 GOTO 10, stopped with RUN/STOP (Esc). Instant payoff,
  with a promise that within a few chapters he'll understand every character. Use the readable
  version; the golfed one (0 I=205.5:PRINTCHR$(RND(.)+I);:GOTO) can be a Good to know box.
- Chapter 7 price checker: "buy only at the maker's price, never collector prices"; markup percent.
- Wish list with a waiting period; Spending Tracker flags purchases above the maker's price.
- Variable dictionary gets units in "What it holds" (e.g. "in cents"); Mars Climate Orbiter story.
- Arrays: the Roman calendar off-by-two (September = 7th month, now 9th).
- FOREWORD (book/chapters/00-0-foreword.md, the first page): why a 1982 machine; plan, organize, then
  code; modern languages are easier and more powerful but overwhelming without a foundation; where
  the book leads (the tracker, a future port to a phone app); the motto. Ends by sending the reader
  to the maze, which stays the first thing he DOES.
- THE LONG ARC (editor): the concepts carry forward; a future SECOND BOOK ports the Spending Tracker
  from C64 BASIC to a modern language (likely a web app, so it runs on his phone), with the C64
  version as the specification. In THIS book: write programs so they port cleanly (blocks as future
  functions, named record columns), and end the capstone with a short "Where next?" page mapping
  C64 ideas to modern ones (GOSUB -> functions, record rows -> structs/objects, code numbers +
  lookup arrays -> enums/dictionaries, relative files -> database tables, array windows -> paging).
- CP CALCULATOR (editor's idea; for Ch 12-13): Pokemon GO combat power, verified against the main
  reference sites: CP = INT((baseAtk+ivAtk) * SQR(baseDef+ivDef) * SQR(baseSta+ivSta) * CPM^2 / 10).
  CPM (CP multiplier) has no formula: it's a LOOKUP TABLE by level, with half levels (1, 1.5 ... 50;
  e.g. level 50 = 0.84029999), so: CPM values in DATA (Ch 12), read into an array indexed by
  level*2-1 (Ch 13). Uses INT (floor) and SQR, both built in. Bonus lesson: several web sources
  give wrong CP formulas -> check your sources (and test everything).
- RECORD TABLES (editor's idea): a 2-D integer array as an in-memory database table. Rows = records,
  column 0 = ID, columns 1..N = properties stored as CODES into string lookup arrays (e.g. CL$(3) =
  "BLUE"). Name the columns with variables (HT=1:WD=2:WT=3, then T%(R,WT)) and document the layout
  in the variable dictionary. Whole-number arrays pay off here (2 bytes vs 5 per box). The array
  is a WINDOW onto a relative file: load a page of records, page through. Bridge from Ch 13-14
  arrays to Ch 20-21 (Tracker v3a/v3b: relative files + lookup tables). The Show variables panel
  displays T%() as a grid, i.e. a live view of the in-memory table.
- Sorting (Ch 14): box 0 is the "parking space" for swaps (A(0)=A(I):A(I)=A(I+1):A(I+1)=A(0)).
  This is box 0's first "special job", promised in Ch 13.
- Box 0's second special job: tables whose numbers naturally start at 0 (hex digits 0-F, the 16
  colors 0-15, sprites 0-7), so the number and the box always match. E.g. DIM H$(15) hex table.
  Underlying habit: make the box number mean something.
- TI jiffies (1/60 s) to HH:MM:SS with INT and division.
- Sprites: a Windows-style spinner ("baller coaster") with 8 sprites and a DATA position table.
- Premise gains the habit "know the subject before you write the code."
- "Break it" challenge (Ch 5, habit "never trust input"): the editor tries to crash the student's
  program (letters for numbers, negatives, empty input, very long text); points both ways. Also a
  deliberately fragile sample program for the student to break, then fix. From the editor's own
  classroom, where students tried to crash each other's BASIC and so learned validation for life.
  Arrays chapter: trigger ?BAD SUBSCRIPT ERROR on purpose (BASIC checks bounds; C does not).

Conventions in chapter files:
- Show C64 messages exactly as on screen: error messages have TWO spaces before ERROR
  (`?SYNTAX  ERROR IN 20`). Inline code keeps double spaces (white-space: pre-wrap).
- Verify every example on the emulated C64 before publishing (headless test harness in this repo's
  history: auto_type the lines, read screen RAM at $0400).
- Anecdotes go in parentheses in the running text (editor's decision).
- Optional clarifying details go in a "Good to know" box: a fenced div `::: good-to-know` ... `:::`.
  The template styles it and adds the heading. Readers can skip these on a first pass.
- Plain fenced code block = something to type. Renders as a C64 screen.
- ` ```{.diagram} ` fenced block = a picture, not to be typed. Renders as a dashed box.
- Every non-blank line in a typed block gets a ↵ keycap (U+21B5, editor's choice), added by the build (mark_return_keys)
  and drawn by CSS, never part of the text (beta tester kept forgetting RETURN; editor's choice).
  So never write RETURN symbols into chapter code blocks yourself.
- Quiz answers written as `**Answer: x**` at the end of each question; the student build
  strips them.

## Course site (Milestones 1-3 drafted)

- Design doc (private Claude Doc): "Work Environment - Implementation Sketch",
  https://claude.ai/artifact/8Ze8EH2K5wBTC686yjHn4T
- `setup.bat` -> `tools/setup.ps1`: downloads PHP 8.4 (php.net "latest" zip), vc64web pinned to
  commit 469b63818d1a8f4d654fd3985b82aeb4e03fabba (skips its doc/ folder: long paths), removes
  vc64web's analytics script, copies ROMs from the local VICE install (fallback: VICE's GitHub mirror).
  TESTED on the editor's Windows 10 LTSC 2021 machine (17 Nov 2026): setup, start, boot, typing,
  Esc = RUN/STOP, Submit, Run all work. Fixes needed on the way: VC++ runtime check reads the real
  vcruntime140.dll version (needs 14.44; registry can claim newer while an update waits for restart);
  unpacking uses C:\Windows\System32\tar.exe (PortableGit's GNU tar can't read zip; the earlier
  .NET unzip silently extracted nothing under Windows PowerShell 5.1).
- Update notices to the editor: end every message that changes the site with
  "To pick this up: git pull, then Ctrl+F5".
- Downloads go through Get-Download in setup.ps1: 3 retries, browser-like user agent, system proxy
  with default credentials; on failure it prints the URL and the exact file path to save it to by
  hand (work networks may cut off .zip downloads), and a saved file is used on the next run.
  Zips are test-opened first (Test-Zip): a cut-off zip is deleted and downloaded again.
  Files saved by a browser under their own names (php-*-Win32-*.zip, the vc64web commit zip) are
  found and used automatically. Editor's work network does TLS interception (MitM) and cut off
  PowerShell downloads; browser downloads got through.
- `start.bat`: PHP built-in server on port 8064, router `site/router.php`.
- Routes: `/` home, `/c64` emulator page, `/book/` = docs/, `/emu/` = runtime/vc64web,
  `/roms/` = runtime/roms, `/api/*` = site/lib/api.php.
- C64 page talks to vc64web directly through the same-origin iframe: `wasm_loadfile` (ROMs),
  `wasm_reset`, `wasm_peek`/`wasm_poke`, `wasm_auto_type`. Submit copies memory from TXTTAB ($2B)
  to VARTAB ($2D) into a PRG. Run/Load resets, pokes the PRG back, sets $2D/$2F/$31, types run/list.
- Tested end to end in headless Chrome: boot to READY, keyboard typing, Submit -> version 1 with
  correct listing, NEW, Run -> program runs.
- Special keys: vc64web maps no PC key to RUN/STOP, RESTORE, CLR/HOME or C= (only its on-screen
  keyboard). Our page adds Esc = RUN/STOP, Page Up = RESTORE, Home = CLR/HOME (Shift + Home clears;
  same as VICE) plus buttons incl. "Clear screen" (beta tester reached for CLS and couldn't clear), via
  `emu.translateKey2(name,'',true)` + `emu.wasm_schedule_key(row,col,pressed,0)`. vc64web calls
  wasm_keyboard_reset on every focus change, so focus the iframe and wait ~150 ms before pressing.
- On-screen keyboard (phones/touch): "Show keyboard" button under the screen toggles vc64web's
  #virtual_keyboard (bootstrap collapse). fitFrame() grows our frame to picture + keyboard and sets
  vc64web's CSS var --keycap_zoom so the keyboard fits the width; key size depends on frame width AND
  height, so it adjusts both in turns until stable. Phone browsers can't raise their native keyboard
  for the emulator canvas, so this is the only way to type on a phone.
- Gotchas found: the standard character ROM is chargen-901225-01 (906143-02 is the Japanese one);
  typed capitals arrive as Shift+letter = C64 graphics, so Caps Lock must be off and auto_type text
  must be lowercase; headless tests need ~110 ms key holds.
- Exercise list: `site/exercises.json` (placeholder entries for now). Chapter 1 has no
  submittable programs (direct mode only).

## Beta test log

- 23 Nov, draft 3 of Ch 1-2 (a long day: morning, afternoon, evening). The two open note questions
  WORKED: real explanations instead of "maybe". VERDICT FROM THE TESTER: NO MORE FULL RE-RUNS ("going
  back again with everything rebooted... it's just not the same anymore"; "like repeating a video
  game you already know"; dotted-out answers on 2.4/2.5). DECISION: each chapter is REQUIRED only
  once; the editor promised no more required repeats. Fixes later are announced, never re-run. But
  coming back by choice (retaking quizzes to raise a score, playing with examples) is always open
  and welcome (editor's clarification).
  "How This Book Works" now says so, and describes the once-through flow and the tools. Next: Ch 3.
  Evidence of learning: avoided ROUND1/ROUND2 (RO) on his own by using R1/R2; fixed ARMOR -> ARMR and
  ENDURANCE -> DURANCE with reasons; Ch 1 quiz 4/5 -> 5/5, Ch 2 quiz 5/5 first try; used the {clr}
  heart (calls it "CLS"); enjoyed the developer getting caught by name collisions.
  Gaps he found (fixed): (1) INSERT: asked twice; also a real BUG: vc64web ignores Shift on
  Backspace (it deletes) and maps no Insert key. Now Insert and Shift+Backspace send SHIFT+INST/DEL;
  Lesson 2.4 teaches "making room". (2) Blank lines: "PRINT" alone prints an empty line; now a Good
  to know in Lesson 2.2. (3) The variable dictionary had no home (no notebook): Lesson 1.5 now says
  any paper notebook or sheet of paper works. Still self-blaming on traps ("I blame my head").

- 22 Nov: DRAFT 3 of Chapters 1-2 (editor): same lessons and rules, NEW particulars everywhere
  (pictures, examples, exercises, quizzes) so each pass has something new to read. Ch 1: lockers,
  XP (X), G/G$/G% "GEMS FOUND", SHIELD/SHOTS = SH, FORTUNE (FOR) -> LUCK, ARMOR/ENDURANCE fix-it,
  MAGIC/MANA quiz. Ch 2: GAME ON, START/HALFWAY/FINISH LINE + QUARTER WAY, PRITN fix by typing NT,
  {clr}ROUND 1, game-over build exercise, LIST 20-40 quiz. All examples verified on the C64.
  Exercise ids now carry a fingerprint of their wording (ex1-4f27a2), so rewritten exercises start
  fresh on Chapter work; the Editor's view marks old answers "(earlier draft)".
  Third name collision of the project, in tools/build.py: a loop variable `text` overwrote the
  chapter's `text`, and the quizzes vanished. Renamed ex_text. Keep a dictionary, even in Python.

- 18 Nov evening, Chapter 1 draft 2 (second pass), ~1 hour, laptop, notes on all 5 lessons:
  * PATIENCE "running thin" in nearly every "boring" note (he added "it's my own problem, not
    yours"). Likely: second pass is slow for him, AND the notes form is heavy (3 boxes x 5 lessons).
    Answers turned terse ("maybe", "I guess so") = form fatigue.
  * Productive struggle in his own words: discovering the error was "oh, now it makes sense, yet
    very frustrating" = the target zone.
  * Exercises show real understanding: fixed SCORE/TOTAL as SC/TTL (no hidden words); exercise 3
    combined two strings and a number in one PRINT.
  * Two-letter trap still "some of it" confusing despite the ? CO proof -> supports building the
    "Show variables" shelf panel.
  * Quiz: he DID try it; it failed silently. Bug: in the quiz handler a loop variable `$c` overwrote
    `$c = client()` (who is signed in), so the attempt had no user and the insert failed. Fixed
    (loop var renamed) and the page now reports save failures. Lesson: retest every save path after
    changing shared code.
  * UNPROMPTED EXPERIMENTING (told the editor at dinner): changed values, displayed them, added more
    math to the addition lines. Strongest engagement signal; it's in variables + arithmetic, so
    Ch 3 (Working Things Out) should land.
  * His model of RETURN: "a text box like a web form". Nearly right; the C64 twist is that the
    whole screen is the form and RETURN submits WHICHEVER line the cursor is on. Candidate opening
    picture for Lesson 2.4 (screen editor), in his own words. DONE: Lesson 2.4 now opens with it.
  * NOTES REFORMATTED (editor's decision): short questions that demand a real answer, not yes/no.
    Two per lesson: "Explain this lesson's big idea in your own words." and "What surprised you,
    confused you, or dragged? Tell me why." (item keys LESSON:explain, LESSON:reaction).

- Story-framed lessons (Micro Adventure style): ASKED, beta tester unsure/not interested; editor:
  better suited to younger readers. DECISION: no story frame. He wants real work (job/challenge).
  Stories live in the Story Engine project, where he is the AUTHOR, not a character.

- 18 Nov, Chapters 0-1 (first session): he treats it as a job/challenge (good: matches his work-ethic
  motivation); asked if it might be addicting (editor: yes, the healthy kind). Struggled with the
  two-letter rule until the editor's `? PR` demonstration; GOLD fixed as GLD; A and A$ demo.
  All three demos are now in Chapter 1. He liked "MILLION DOLLARS" much more than "APPLES":
  category = STAKES AND ASPIRATION, i.e. words of POSITIVE VALUE (editor): points, rewards, coins,
  credits, gems, stars, bonus points, XP, treasure, high scores, prize funds, paychecks, but VARY the specifics so none wears out by repetition
  (editor's rule: never take a reaction literally). He edits by using the full screen, and wants the MOUSE to
  place the cursor.
- He opened the book and the emulator side by side on his laptop almost immediately (reference
  on one side, machine on the other). Idea, not built: a "study view" page with both in one window.
- BUILT (beta tester request): SHIFT+CLICK on the C64 screen moves the cursor there. Allowed only
  when 157 = 128 (direct mode), 204 = 0 (waiting for typing), 212 = 0 (not quote mode) and
  216 = 0 (not insert mode); otherwise a status message explains why. Cursor = row 214, column
  211 mod 40 (211 is the column in the LOGICAL line, 0-79). Click -> cell via the measured
  picture geometry: 384 x 270 C64 pixels, text area 320 x 200 at (32, 35). Moves are fed as
  cursor-key PETSCII codes through the keyboard buffer (631-640, count at 198), 10 at a time.
  Note: 57/58 (current line) is NOT a direct-mode test: it reads 0 at a fresh READY.

## Course site: chapter work (Milestones 4-5, partly)

- `/work` (Chapter work): per chapter, exercises with written answers, the quiz (graded on the
  server; answers never sent to the page), and beta tester notes (confusing / boring / fun per lesson).
- Second passes (editor: "then why would he revise them?"): Chapter work boxes always START EMPTY;
  the previous answer shows underneath in grey ("Last time (date): ..."). Every save is a new row;
  empty note boxes are never saved, so they can't wipe earlier notes. Book page loads (/book/) are
  logged in visits too (user may be blank: the book doesn't require sign-in).
- REMIX ON REPEAT (editor): on a second pass, each exercise that already has an answer shows "You've
  solved this before. This time, find a different answer that still works." Each chapter's
  Exercises section says the same in one line. Ways to vary (for writers, NOT spelled out to the
  student; finding them is the point): names, ? vs PRINT, calculating inside PRINT vs storing first,
  one PRINT with semicolons vs several, data types (e.g. LB%), order of independent steps.
- `/review` (Editor's view): everyone's latest notes and answers, every quiz attempt, recent
  programs, each tagged with who / device / IP, plus a "Who and where" visit log.
- SIGN-IN by name only (editor's decision; family LAN). Cookie `c64user`, case-insensitive names
  (users table). /c64 and /work require a name and log visits (visits table: user, ip, device
  like "Phone (Android)", user agent, page). Every save records user, ip, device. Work, quiz
  history and program versions are per person; ?everyone=1 for the Editor's view. Databases from
  before sign-in are upgraded in place; old rows are labelled "(before sign-in)".
- Content comes from the chapter files: `tools/build.py` writes `site/content.json` (lessons,
  exercises, quizzes with answers) and `site/exercises.json` (the C64 page's picker: practice plus
  every exercise from Chapter 2 on, ids like ch02-ex3). Rebuild after any chapter change.
- Tables: quiz_attempts, quiz_answers, responses (every save is a new row; newest wins).
- Chapters 1-2 are labelled DRAFTS and the reader is the BETA TESTER (editor's decision). Examples
  were refreshed after the first test session so his second pass isn't a rerun; data types became
  Lesson 1.2 (the A;A$ demo "lit a bulb"). Keep refreshing specifics between passes.

## Decisions made

- **Language and machine:** Commodore 64 BASIC V2. Reference emulator is VICE; TheC64
  gets its own appendix. Cassette covered only via VICE's datasette (appendix).
- **Known limits, no loopholes:** the book teaches the machine's documented limits as firm rules
  (8 sprites, 2-letter names, 80-character lines) and works within them. No sidebars on tricks that
  break limits (sprite multiplexing, opening the borders, etc.). Fun for the editor, confusing for
  a learner who does best with rules that hold.
- **Proof beats explanation** (from the first beta test, 18 Nov): the label-maker picture didn't
  land; the editor's demo `? PRICE`, `? PRIZE`, `? PR` (all print 3) did. Every rule a lesson
  explains should also give the student a way to catch the C64 in the act.
- **Earned discoveries, never announced** (the editor's lifelong way of teaching his sons): each part
  of the book quietly contains things worth noticing, pitched just beyond easy but within reach,
  so finding them gives the feeling of being smart. Never label them ("puzzle", "trick", "secret
  challenge"); at most, a small honest hint. Examples: the opener's hint that "random" holds a
  surprise (Ch 3: same maze after every reset); a message hidden in a sample program's DATA,
  revealed once CHR$ and READ are known; a findable-but-not-obvious bug in the Detective chapter;
  something in the sample story's scene numbering. All of it must still be true (simplify, never
  falsify) and inside known limits.
- **Rules, not innards** (editor's decision): state the machine's behavior as rules the reader can rely
  on; leave out the internals behind them (variable-table bytes, type bits, string pointers, etc.).
  Fascinating, but not this book.
- **Least liked first, best last** (from the editor's dinner-table lesson, which the student adopted):
  each lesson saves its most satisfying moment (the thing that runs, the surprise, the payoff) for
  the end; careful parts come first. Same at every scale: the book opens on the maze; each sitting
  stops on a success. Habits are always given with a reason and framed as "what programmers do".
- **Exercises only use what's been taught.** Before publishing, check every exercise against the lessons
  before it. (Beta test caught Ch 1 Ex 3 needing PRINT with words and boxes mixed, which draft 2 had
  dropped; fixed in Lesson 1.2.) Joining strings with + stays in Ch 4.
- **Short patience is a design constraint** (the student's known trait, per the editor): short steps,
  fast payoffs, light forms. Never treat it as his problem to fix. But it is UNDERDEVELOPED, so
  TRAINABLE: early chapters give instant payoffs; later ones slowly stretch the gap (multi-sitting
  builds like Tracker v0 to v3, each version a visible milestone). ALWAYS show the finish line
  (where he is, what's next, how far to go): he was patient for years with braces because the end
  was visible. The waiting-period wish list is patience practice in its purest form.
- **Motto: "A discovery, not a failure."** (editor) Knowing a trap exists turns frustration into
  "oh, found another one." Every chapter that warns about traps or errors should carry this spirit.
  (Appendices: `book/chapters/90-appendices.md` lists A-G as planned, so references like Lesson
  1.4's "Appendix E will list every one" stay honest. Files starting with 9 are skipped by the
  content extractor.)
- **Know where to look:** chapters that front-load rules say so (Ch 1 opening): read once, don't
  memorize, come back when something bites. "Good programmers know where to look."
- **Simplify, never falsify:** every rule the book states must be literally true on a real C64.
  Leaving things out is fine; a simplified rule that is false is not. Example (from the editor's own
  schooling): DIM A(10) creates ELEVEN elements, 0 to 10, never ten. The book says so plainly, then
  adopts a stated convention (editor's decision): data in boxes 1..N; box 0 is mentioned briefly as
  existing and "saved for special jobs", not taught as a lesson. Never claim DIM A(10) = 10 elements.
- **Writing style:** for a young adult beginner; plain language at roughly an 11-12-year-old reading level, never
  childish (no mascots, no cartoons, no talking down). Short sentences.
- **Core mental model:** a shelf of labelled boxes, used for every idea from variables
  to arrays, sorting, files and lookup tables. Each idea also gets a video-game picture.
- **Lesson format (7 steps):** Goal, Picture, Try it, Predict, Why it works,
  Organize it, Exercises and quiz.
- **Recurring projects:** Spending Tracker (v0 menu skeleton, v1 DATA + arrays,
  v2 sequential file, v3a relative file, v3b relative file + lookup tables) and
  Story Engine (DATA-driven scenes, later sprite, tune and disk files). The student's
  own stories are never submitted; only the engine is.
- **Money:** stored as whole cents in floating-point variables (integer variables
  overflow past 32767).
- **Course site:** portable, runs from a USB stick. PHP built-in web server + SQLite,
  started from a batch file. No Apache/MySQL needed. Student data in `data/`, never in git.
- **Emulator in the browser:** start with vc64web (maintained WebAssembly port of
  VirtualC64). Programs are stored as PRG bytes plus a text listing (via VICE's `petcat`);
  "Run" loads a stored PRG into the emulator. A custom VICE WebAssembly build is a
  possible later option, not a starting point.

## Naming traps already caught in drafts

Check every BASIC example name for hidden keywords. Caught so far: SPEND (END),
COLOR (OR), COST (COS), MONEY (ON), TOTAL (TO), SCORE (OR), TIME (TI).

## Open questions (waiting on the editor)

- Second-language support: English only, or Japanese key terms and short bilingual summaries?
- Final title (working title: *Thinking in C64 BASIC*).

Settled along the way: example names are varied invented names, never the student's; quiz answers
live in the public chapter sources (honor system) and the answer edition is password-locked; the
programmer's notebook is paper; the voice is plain and never childish; the reference machine is
VICE or the browser C64, with TheC64 notes planned for Appendix F.

## Show variables panel (built; editor-approved design)

ARRAYS cabinet (added after the editor's DIM A(10) test showed arrays were missing): reads the
array list (47/48 to 49/50). Per array: 2-byte name (type bits as for variables), total size
(little-endian), dimension count, then each dimension's size (big-endian) stored LAST dimension
first; elements follow with the FIRST index changing fastest (5 bytes number, 2 bytes integer high
first, 3 bytes string: length + address). Drawn as a row of numbered boxes (1-D) or a grid with
row/column numbers (2-D up to 11 x 11); box 0 is shown, since DIM A(10) really makes 11 boxes.

Layout (editor): FOUR CABINETS, one per type (Numbers, Text ($), Whole numbers (%), Functions (FN)),
always shown, empty ones labelled "Empty"; boxes in creation order inside each.

"Show variables" under the C64 screen opens a shelf of boxes, one per variable, read live (every
0.5 s) from BASIC's variable table: label AS THE C64 STORED IT (two letters + $ or %, or "FN XX"),
value, type. EDITOR'S RULE: never map back to the longer typed name (COINS -> CO is the reader's
discovery to make). Numbers are decoded from the 5-byte float and formatted like the C64's own
PRINT (.5, 1E+10, 1E-03, 9 digits): verified identical to PRINT for 11 tricky values. Values change
live while a program runs, so it doubles as a watch window. FN boxes are shown too (editor: "they
exist, they will create questions and curiosity, and they will eventually get an answer"): label
"FN PR", value "(X) = X*2+1" read from the program text via the entry's formula pointer, parameter
name via its pointer to the parameter's own box (which DEF FN creates, and which stays 0 after a
call because BASIC saves and restores it; a future 'why?' moment). It is the start of a BASIC debugger (planned
next: line stopped at, highlight what changed, arrays for Ch 13, Detective Work chapter).

## Variable list helper (tested)

BASIC V2 can't list variables, but its variable table is documented: from VARTAB (45/46) to
ARYTAB (47/48), 7 bytes each, 2-byte name (only two letters stored), type in the high bits.
Program version, run with GOTO 63000 (keeps variables; RUN would wipe them):

    63000 ZS=PEEK(45)+256*PEEK(46):ZE=PEEK(47)+256*PEEK(48)-1
    63010 FOR ZI=ZS TO ZE STEP 7:ZA=PEEK(ZI):ZB=PEEK(ZI+1)
    63020 ZT=1-(ZA>127)-2*(ZB>127)
    63030 PRINT CHR$(ZA AND 127)CHR$(ZB AND 127)MID$(" F$%",ZT,1)
    63040 NEXT:END

After COINS=40:COMBO=6:P$="BONUS":P%=3:G=1 it prints CO, P$, P%, G, ZS, ZE. Idea (editor
interested): a "Show variables" panel on the C64 page that draws the shelf from the same table.
Discovered on the way: a TYPED line must be under 80 characters (an 80-character line is never
stored: the cursor wraps and RETURN enters the empty row). Chapter 2 and the plan now say so.

## Next steps

1. DONE: Chapter 3 drafted (Exercise 1 is the editor's Pokemon GO IV idea: (AT+DF+HP)/45*100, which
   needs parentheses and INT(x+.5); verified: 60.3333334 wrong vs 93.3333334, rounds to 93) (5 lessons; every example verified on the C64; the course site maps ^ to
   the C64's up-arrow). Next: the beta tester's one pass through it. Then Chapter 4, Words as Data.
2. Improvement chart: quiz score per attempt over time, on /work and /review.
3. Autosave on Chapter work, plus a warning before leaving with unsaved text (awaiting go-ahead).
4. Later, each with its chapter: debugger additions (current line, change log, error explainer),
   the block-aware Renumber tool (Ch 11), Appendix E and the other appendices.
