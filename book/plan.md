# Thinking in C64 BASIC — Book Plan & Chapter 1 Draft

## The premise

Commodore 64 BASIC (BASIC V2) gives the programmer almost no help with organization, so every bit of order in a program has to come from the person writing it. That weakness is the book's teaching tool.

BASIC V2 has no ELSE, no WHILE loop, no named procedures, no RENUMBER command, and no disk commands of its own. Variable names are only two characters deep. A program that is not planned turns into tangled GOTOs within an afternoon, and the learner sees the mess directly. A program that is planned reads cleanly even in this primitive language. The contrast is visible on one screen.

Every chapter therefore teaches two things side by side: a piece of the language, and a habit of mind that keeps it organized. The language parts are small. The habits are the real curriculum.

| Language piece | Habit it carries |
| --- | --- |
| Variables | Name things deliberately and keep a written list of names |
| IF/THEN | State the question precisely before answering it |
| FOR/NEXT | Notice repetition and describe it once |
| GOSUB/RETURN | Break a big job into named, separate jobs |
| Line-number blocks | Give every part of the program its own place |
| DATA and arrays | Separate the information from the instructions |
| Files | Plan the shape of information before storing it |
| Lookup tables | Never write the same fact twice |

## Who it is for and how each lesson runs

The reader is a young adult who is bright, strong in spatial reasoning, good at video games, and easily distracted. The book is written in plain, simple language, about the reading level of a book for 11- or 12-year-olds, but it never looks or sounds like a children's book: no mascots, no cartoons, no talking down. Lessons are short enough to finish in one sitting, and every lesson ends with a program that runs.

Design rules for every lesson:

- **One idea per lesson.** If a lesson needs two new ideas, it becomes two lessons.
- **Show it as a picture first.** Memory as a wall of labelled boxes, the screen as a 40 × 25 grid, the program as a map of neighborhoods. Pictures come before prose.
- **Type before explaining.** The reader types a few lines and sees a result within the first two minutes.
- **Predict, then run.** Before running anything, the reader writes down what he thinks will happen. Being wrong is useful, not a failure.
- **Errors are expected.** Each chapter deliberately triggers at least one error message and explains it.

Every lesson follows the same seven steps, so the shape itself becomes familiar:

1. **Goal** — one sentence: what you will be able to do.
2. **Picture** — a diagram of the idea.
3. **Try it** — type a short program and run it.
4. **Predict** — change one thing, guess the result, then run it.
5. **Why it works** — a short explanation, no more than a page.
6. **Organize it** — the habit this lesson teaches, with a checklist item to add to his personal "programmer's notebook."
7. **Exercises and quiz** — two or three exercises (type it, change it, build it) and five multiple-choice questions, submitted through the course site.

## Mental models: the shelf and the game

The whole book is built on one picture: **a shelf of labelled boxes**. Every new idea is shown as something happening to that shelf, so each chapter adds to a picture he already has instead of starting a new one. Each idea also gets a video-game picture, because games already use every one of these ideas.

| Big idea | Everyday picture | Game picture | Ch |
| --- | --- | --- | --- |
| Variable | A box on a shelf with a label on the front | Your coin counter or health bar | 1 |
| Number box vs. text box | A box for coins vs. a box for a written note | A score vs. a player name | 1 |
| Two-letter names | A label maker that only prints two letters | Two items stacking into one inventory slot by mistake | 1 |
| Program | A recipe: steps in order, top to bottom | A level you play from start to finish | 2 |
| IF/THEN | A locked door: you go through only if you have the key | "You need the red key to open this door" | 7 |
| Loop | Doing laps of a running track | Grinding the same area until you level up | 8 |
| Subroutine | Going to the kitchen for a drink, then coming back to your seat | A side quest that returns you to where you were | 10 |
| Line-number blocks | Rooms in a house: kitchen things go in the kitchen | Zones on a world map | 11 |
| Array | A row of numbered boxes on one shelf | An inventory bar with numbered slots | 13 |
| Two-dimensional array | A shelving unit: rows and columns of boxes | A chest inventory grid, or a tile map | 13 |
| Sorting | Rearranging boxes on the shelf into order | The "sort inventory" button | 14 |
| Screen memory | Graph paper, one letter per square | The tile grid a level is drawn on | 15 |
| Sprite | A picture drawn on a small grid that can slide over the background | Literally a game sprite | 16 |
| File | Packing the shelf into a moving box so it survives the trip | A save file | 19 |
| Sequential file | A cassette: you must listen from the start to reach a song | Replaying a cutscene you can't skip | 19 |
| Relative file | Numbered lockers: walk straight to locker 37 | Save slots: load slot 3 directly | 20 |
| Lookup table | A catalog: the order slip says "item 37," the catalog says what 37 is | Item ID numbers: the game stores 37, its item database knows 37 is a sword | 21 |
| GOSUB without RETURN | A stack of plates that keeps growing until it falls | Opening menus inside menus without closing any | 10 |

How games are used beyond pictures:

- **Side quests.** Every chapter has optional extra exercises for practice and repetition, especially the arithmetic he needs more of. They are optional so they feel like extra play, not homework.
- **A boss at the end of each part.** Each part ends with one larger exercise that uses everything in that part.
- **Visible progress.** The course site shows chapters completed and exercises passed, like a game's progress screen.
- **Games as projects.** Small games appear as exercises (a number-guessing game in Part 2, a dodging game with a sprite in Part 4), and the capstone can be a game if he chooses.

Game words are used lightly, as seasoning. The book stays a programming book, not a game with lessons bolted on.

## Book outline

The book has 22 chapters in six parts, plus appendices. Each chapter is two to four lessons. The two recurring projects start in Part 2 and are rebuilt as each new tool arrives.

| Ch | Part | Title | Language taught | Habit taught | Project milestone |
| --- | --- | --- | --- | --- | --- |
| 1 | Foundations | This Is a Variable | Numeric and string variables, PRINT, LET | Name things deliberately | Start the variable dictionary |
| 2 | Foundations | Talking to the Computer | Direct vs. program mode, line numbers, LIST, RUN, NEW, screen editing | A program is steps in order | — |
| 3 | Foundations | Working Things Out | Arithmetic, order of operations, INT, RND | Work it out on paper first | — |
| 4 | Foundations | Words as Data | Joining strings, `LEN`, `LEFT$`, `MID$`, `RIGHT$`, `STR$`, `VAL` | Text is information too | — |
| 5 | Foundations | Asking Questions | INPUT, GET | Never trust input; check it | — |
| 6 | Foundations | Saving Your Work | SAVE, LOAD, VERIFY, `LOAD"$",8` | Keep numbered versions | First submission to the course site |
| 7 | Control | Making Decisions | IF/THEN, comparisons, AND, OR, NOT | State the question precisely | — |
| 8 | Control | Repetition | FOR/NEXT, STEP, nested loops | Describe repetition once | — |
| 9 | Control | Jumping Carefully | GOTO, ON...GOTO | Every jump needs a reason | — |
| 10 | Control | Subroutines | GOSUB/RETURN, ON...GOSUB | Break big jobs into named jobs | — |
| 11 | Control | Program Maps | Line-number neighborhoods, REM headers, menus | Everything has a place | Tracker v0: menu skeleton |
| 12 | Data | DATA and READ | DATA, READ, RESTORE | Separate information from instructions | Story Engine v1 |
| 13 | Data | Arrays | DIM, one- and two-dimensional arrays | Group what belongs together | Tracker v1 |
| 14 | Data | Searching and Totals | Linear search, simple sort, totals by category | Process data in passes | Tracker v1 reports |
| 15 | Screen and Sound | The Screen Grid | Cursor and color codes, TAB, SPC, POKE to screen and color memory | Plan layouts on graph paper | Tracker menus get a real screen |
| 16 | Screen and Sound | Sprites | Sprite design, sprite pointers, VIC-II registers | Turn pictures into numbers | Story Engine character sprite |
| 17 | Screen and Sound | Sound and Music | SID registers, waveforms, envelopes, tunes from DATA | Build from tested parts | Story Engine theme tune |
| 18 | Storage | The Disk Drive | Directory, command channel 15, scratch, rename, validate, reading drive errors | Check for errors every time | — |
| 19 | Storage | Sequential Files | OPEN, PRINT#, INPUT#, CLOSE, ST | Plan the record before storing it | Tracker v2 (flat file), Story Engine v2 |
| 20 | Storage | Relative Files | Fixed-length records, record positioning | Fixed shapes make data findable | Tracker v3a |
| 21 | Storage | Lookup Tables | Code tables for categories and payees | Never write the same fact twice | Tracker v3b (compressed register) |
| 22 | Putting It Together | Capstone | Everything | Finish what you start | A finished program of his choosing |

Appendices: (A) setting up VICE and the browser emulator, with a keyboard map; (B) using the cassette datasette in VICE; (C) every error message and what usually causes it; (D) memory map and POKE reference; (E) BASIC keywords and their abbreviations; (F) notes for TheC64.

**Approved additions (Nov 18).** A new chapter, *Detective Work*, goes right after Chapter 11, so later chapters shift by one and the book becomes 23 chapters. It teaches debugging in rising order: reading the error, playing computer with a trace table, print probes, `STOP`/`CONT` breakpoints, testing one block alone, and splitting the search in halves. Alongside Chapter 11, the C64 page gains a block-aware **Renumber** tool that keeps REM-headed blocks on their hundreds, keeps DATA regions together, and lets important subroutines be pinned in place. It is introduced only after the student has felt the pain of renumbering by hand.

## The two recurring projects

The Spending Tracker is rebuilt four times, and each rebuild shows why the new tool is better than the old one. The Story Engine gives his interest in fiction a home without anyone having to read his writing.

### Spending Tracker

| Version | Chapter | Where the data lives | What is new | Approx. bytes per entry |
| --- | --- | --- | --- | --- |
| v0 | 11 | Nowhere yet | Menu skeleton with empty subroutines in their own line-number blocks | — |
| v1 | 13–14 | DATA statements loaded into arrays | Entries, running total, totals by category | Lost when the computer is switched off |
| v2 | 19 | One sequential file | Add entries and keep them between sessions; whole file read to report | About 40 |
| v3a | 20 | Relative file, fixed-length records | Jump straight to entry number N; edit one entry in place | About 44 (padded) |
| v3b | 21 | Relative register file plus category and payee tables | Register stores small codes instead of repeated words | About 22 |

What v3b changes, using one grocery purchase as the example:

| Field | v2 / v3a stores | v3b stores |
| --- | --- | --- |
| Date | `2026-11-03` | `261103` |
| Category | `GROCERIES` | `03` (row 3 of the category table) |
| Payee | `FOOD LION` | `012` (row 12 of the payee table) |
| Amount | `23.45` | `0002345` (whole cents) |

The lesson is not only smaller records. When a store changes its name, v3b fixes it in one place, and every entry that points to it is instantly correct.

### Story Engine

A story is a set of numbered scenes. Each scene has text and up to three choices, and each choice names the scene it leads to. That is a data structure, and he designs it himself in Chapter 12.

- **v1 (Chapter 12):** scenes stored in DATA statements; the engine reads, shows, and follows choices.
- **v1 plus (Chapters 16–17):** a character sprite and a theme tune.
- **v2 (Chapter 19):** each story is a file on disk, so one engine can play many stories.

The book ships with a short sample story for all examples and grading. His own stories live only on his own disk images, and only the engine is ever submitted.

## C64 traps the book teaches on purpose

These are the behaviors that confuse every C64 beginner. Each one is taught deliberately in the chapter listed, usually by triggering it on purpose.

| Trap | What actually happens | Chapter |
| --- | --- | --- |
| Only two letters of a name count | `SHIELD` and `SHOTS` are the same variable (`SH`), so one silently overwrites the other | 1 |
| Keywords hidden inside names | `MONEY` contains `ON`, `TOTAL` contains `TO`, `SCORE` contains `OR`; each gives `?SYNTAX ERROR` | 1 |
| Reserved variables | `ST`, `TI` and `TI$` belong to the system; even `TIME` fails because it starts with `TI` | 1 |
| Numbers print with extra spaces | `PRINT 5` shows a space before the 5 (room for a minus sign) and one after | 1 |
| Integer variables are small | `A%` holds only −32768 to 32767, so cents stored in an integer overflow past $327.67 | 3, 13 |
| 80-character line limit | A line can be at most two screen rows, and a typed line must stay under 80 characters: typing the 80th wraps the cursor to a new row, and RETURN enters that empty row instead (tested). Abbreviated keywords can make a line LIST longer than it can be re-edited | 2 |
| INPUT and commas | Typing a comma into a string INPUT gives `?EXTRA IGNORED` and loses the rest | 5 |
| `LOAD"$",8` erases your program | The directory is loaded as if it were a program, replacing what is in memory | 6 |
| Save-with-replace | `SAVE"@0:NAME",8` has a long reputation for corrupting 1541 disks; the book always scratches first, then saves | 6, 18 |
| Arrays without DIM | Up to 11 elements (0 to 10) work without DIM; a second DIM of the same array gives `?REDIM'D ARRAY` | 13 |
| Garbage-collection pauses | Heavy string work can freeze the machine for seconds while BASIC tidies memory | 14 |
| Files left open | A program that stops mid-write leaves an unclosed "splat" file (`*PRG`, `*SEQ`); the fix is VALIDATE, not scratch | 18, 19 |
| GOSUB without RETURN | Jumping out of subroutines or loops fills the stack and ends in `?OUT OF MEMORY` | 10 |

## The chapters themselves

The chapter text lives in `book/chapters/`, one file per chapter, and is the source of truth for
everything readers see. (An early draft of Chapter 1 used to sit here; it was removed once the
chapters moved into their own files, to avoid two conflicting versions.)

## Open questions for the editor

- [ ] **Japanese support.** English only, or Japanese key terms (with furigana) and short bilingual summaries at the end of each lesson?
- [ ] **Title.** Working title is *Thinking in C64 BASIC*. Alternatives: *Order from Chaos*, *Two Letters Deep*, *Boxes, Labels and Plans*.
- [x] **Names in examples.** Decided: varied invented names, never the reader's own.
- [x] **Answer keys.** Decided: answers stay in the chapter sources (honor system); the editor's edition with answers is password-locked.
- [x] **Programmer's notebook.** Decided: paper.
- [x] **Voice.** Decided: plain language at roughly an 11- to 12-year-old reading level, never childish, with an everyday picture and a game picture for every idea.
- [x] **Reference machine.** Decided: VICE or the browser C64; TheC64 gets its own notes in Appendix F.
