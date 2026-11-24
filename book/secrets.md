# C64 BASIC Secrets: Catalog

Collected from the C64 Programmer's Reference Guide, the User's Guide, C64-Wiki, and
period magazines (COMPUTE!, COMPUTE!'s Gazette). Each entry has a proposed home: a
chapter (as a lesson point or a "Good to know" box) or the appendix of secrets.

**Status:** *Tested* = run on the emulated C64 (vc64web, real ROMs) and behaves exactly
as written. *Manual* = documented in the official manuals, not yet tested in our
emulators (mostly key combinations, whose PC-keyboard mapping differs between VICE and
the browser emulator; check before writing them into a lesson).

## Typing and the screen editor

| # | Secret | Status | Proposed home |
| --- | --- | --- | --- |
| 1 | `?` is short for `PRINT`; `LIST` spells it out | Tested | Ch 1 (done) |
| 2 | Keyword abbreviations: first letter, then the next letter with Shift (`lI` = LIST, `gO` = GOTO). `LIST` always spells keywords out in full | Tested | Ch 2 Good to know; full table in Appendix E |
| 3 | Abbreviations let a line go past 80 characters, but such a line can't be edited after `LIST` (the editor reads only 80) | Manual | Appendix E, with the warning |
| 4 | Abbreviations don't save memory: every keyword is stored as one byte (a "token") however it was typed | Manual | Appendix E |
| 5 | Spaces are optional: `10 IFA=5THENPRINT"YES"` works. LIST keeps the spaces you typed | Tested | Ch 2 (already noted); readability point in Ch 11 |
| 6 | Holding CTRL slows down a `LIST` (or any screen output); RUN/STOP stops a `LIST` | Manual | Ch 2 Good to know, once the PC key for CTRL is confirmed in both emulators |
| 7 | SHIFT + RETURN moves to the next line *without* entering the current one: an escape hatch after a bad edit | Manual | Ch 2 Good to know (test first) |
| 8 | SHIFT + INST/DEL inserts a space to make room in the middle of a line | Manual | Ch 2 or Appendix A (test first) |
| 9 | Quote mode: after typing an odd number of `"`, cursor and color keys become reversed symbols that are *stored* in the string; DEL still works normally | Tested (CLR) | Ch 2: the `{clr}` reversed heart (done). Full treatment in Ch 15 (cursor and color codes) |
| 10 | CTRL + 1 to 8 and C= + 1 to 8 change the text color; CTRL + 9 / CTRL + 0 turn reverse on/off | Manual | Ch 15; Appendix A keyboard map |
| 11 | SHIFT + C= switches between capitals-and-graphics and lowercase-and-capitals | Manual | Ch 15 |
| 12 | RUN/STOP + RESTORE resets the screen and colors but keeps the program | Tested | Ch 2 Good to know (already on the C64 page) |

## The language

| # | Secret | Status | Proposed home |
| --- | --- | --- | --- |
| 13 | `LET` is optional: `A = 5` and `LET A = 5` are the same | Manual | Ch 1 Good to know |
| 14 | A comparison is a number: true is **-1**, false is **0** (`?5>3,5<3` prints `-1  0`) | Tested | Ch 7 lesson point |
| 15 | `IF X THEN 30` jumps to line 30 (no GOTO needed); `IF X GOTO 30` also works | Tested | Ch 7 Good to know |
| 16 | `IF A THEN ...` is true for any A that isn't 0 | Manual | Ch 7 Good to know |
| 17 | `GO TO` with a space works, kept for compatibility with older BASICs | Tested | Appendix |
| 18 | A bare `GOTO` (no number) jumps to line 0 | Tested | Appendix (trivia, not style) |
| 19 | A lone period means zero: `?.` prints 0 | Tested | Appendix (trivia, not style) |
| 20 | Commas in PRINT jump to the next 10-character column; semicolons keep things together | Tested | Ch 1 or Ch 15 |
| 21 | Putting items side by side in PRINT, with no separator, works like a semicolon (`? A "APPLES."`) | Tested | Ch 1 (done) |
| 22 | In direct mode, `GOTO 20` starts a program at line 20 and *keeps* the variables; `RUN 20` starts there but wipes them (`A=7:GOTO 20` prints 7, `A=7:RUN 20` prints 0) | Tested | Ch 2: `RUN 20` (done). Ch 11 lesson point: test one block at a time with hand-set variables, `GOTO`, and a `STOP` at the block's end (editor's own habit, as an anecdote) |
| 23 | `STOP` in a program pauses it like RUN/STOP (`BREAK IN 20`); `CONT` carries on from there. A built-in breakpoint for finding bugs | Tested | Ch 9 or Ch 10 lesson point (debugging) |
| 24 | Several statements fit on one line, separated by colons | Tested | Ch 3 (with the style advice: one idea per line) |

## Numbers, randomness, and time

| # | Secret | Status | Proposed home |
| --- | --- | --- | --- |
| 25 | `RND(1)` gives the same sequence after every reset (`.185564016`, `.0468986348`, `.827743801`...), so the first maze after power-on is always the same maze | Tested | Ch 3, Lesson 3.5 (done) |
| 26 | `X = RND(-TI)` mixes in the clock, so each run starts somewhere different | Tested | Ch 3, Lesson 3.5 (done) |
| 27 | `INT(RND(1)*6)+1` rolls a die (whole numbers 1 to 6) | Tested | Ch 3, Lesson 3.4 (done) |
| 28 | `TI` counts jiffies (1/60 second) since power-on; `TI$` shows the time as HHMMSS; `TI$="000000"` sets the clock | Manual | Ch 3 or Ch 4 (the base-60 exercise) |
| 29 | `TITLE$` is really `TI$`: `TITLE$="MY GAME"` gives `?ILLEGAL QUANTITY  ERROR`, and `TITLE$="120000"` sets the clock | Tested | Ch 1, Lesson 1.4 (done) |
| 30 | `FRE(0)` reports free memory, but shows a negative number on a fresh C64 (`-26627`); add 65536 for the real figure (38909) | Tested | Ch 13 (arrays and memory) Good to know |
| 31 | The power operator is the up-arrow key: `2↑3` is 8 | Tested | Ch 3, Lesson 3.1 (done). The course site maps ^ (Shift + 6) to the C64's up-arrow |

## Memory, keyboard, and the system

| # | Secret | Status | Proposed home |
| --- | --- | --- | --- |
| 32 | `PRINT CHR$(147)` clears the screen from inside a program | Tested | Ch 4 or Ch 15 |
| 33 | `POKE 53280,n` sets the border color and `POKE 53281,n` the background (n = 0 to 15) | Manual | Ch 15 |
| 34 | `POKE 646,n` sets the text color | Manual | Ch 15 |
| 35 | The keyboard buffer holds 10 keypresses; `POKE 198,0` empties it, so a "press any key" waits for a fresh press | Manual | Ch 5 Good to know |
| 36 | `PEEK(197)` tells which key is held down right now (64 = none), handy for games | Manual | Ch 16 (sprite games) or Appendix |
| 37 | `POKE 650,128` makes every key repeat when held (normally only cursor keys, space and DEL repeat) | Manual | Appendix |
| 38 | `SYS 64738` restarts the C64 as if switched off and on: the program is gone | Manual | Appendix, with a clear warning |
| 39 | Integer variables (`A%`) don't make math faster (BASIC converts them to decimals); they save memory in large arrays | Manual | Ch 13 Good to know |

## Disk and tape

| # | Secret | Status | Proposed home |
| --- | --- | --- | --- |
| 40 | `LOAD"$",8` then `LIST` shows the disk's directory (and replaces the program in memory) | Manual | Ch 6 (already in the traps table) |
| 41 | `LOAD"*",8` loads the first file on the disk (or the last one used) | Manual | Ch 6 Good to know |
| 42 | Wildcards: `LOAD"SP*",8` loads the first file starting with SP; `?` matches any single character | Manual | Ch 18 |
| 43 | SHIFT + RUN/STOP loads and runs the next program from tape | Manual | Appendix B (cassette in VICE) |

## Left out on purpose

Per the book's "known limits, no loopholes" rule, these are documented but excluded:
POKEs that disable RUN/STOP or RESTORE, list protection (hiding line numbers or the whole
listing), keyboard locks, switching off the screen or interrupts, bank-switching POKEs,
recovering a program after `NEW`, and the line-number crash bug (`GOTO 350720`).
They break the machine's rules rather than teach them.
