# C64 facts verified in this project

Each fact was observed on the course site's C64 (vc64web with the original ROMs: BASIC V2, KERNAL
901227-03) unless marked otherwise. If a fact is here, it does not need testing again. Add new facts
as they are verified. String-function edge cases live in `reference/entries/20-strings.json` (all verified).

## Names and keywords

| Fact | Detail |
| --- | --- |
| Two significant characters | COINS = COMBO = CO; SHIELD = SHOTS = SH; MAGIC = MANA = MA; DAMAGE = DASH = DA; PRICE = PRIZE = PR |
| Keywords found inside names (?SYNTAX  ERROR) | GOLD (GO), LIFE (IF), POINTS (INT), BONUS (ON), SCORE (OR), MONEY (ON), TOTAL (TO), COST (COS), FRIEND (END), LENGTH (LEN), FORMAT (FOR), STATUS (ST), TIME (TI), FORTUNE (FOR), DEFENSE (DEF), VALUE (VAL), TOKEN (TO), DIFFICULTY (IF), ARMOR (OR), ENDURANCE (END), STARS (ST) |
| Safe examples | LEVEL, LIVES, LUCK, GLD, LV, LK, HP, XP, SC, GM, SH, CO, DURANCE, ARMR |
| Taken two-letter names | IF ON OR TO GO FN (keywords), ST TI (reserved variables): all ?SYNTAX  ERROR as targets |
| TITLE$ is TI$ | `TITLE$="MY GAME"` → ?ILLEGAL QUANTITY  ERROR; `TITLE$="120000"` silently sets the clock |
| Abbreviations | 52 verified (`reference/keywords.json`). Shifted letter can't be the last character; table order, first match wins. None: INPUT IF REM ON PRINT NEW TO FN OR INT POS LOG COS TAN LEN GO |
| `?` | Stored as the PRINT token; LIST shows PRINT |

## Values and arithmetic

| Fact | Detail |
| --- | --- |
| True / false | `?5>3,5<3` → -1, 0 |
| Integer variables | `G%=5.7` → 5 (truncates); `G%=40000` → ?ILLEGAL QUANTITY  ERROR |
| Type mismatch | `G="GEMS"`; `"SCORE: "+5` → ?TYPE MISMATCH  ERROR |
| Order | `2+3*4`=14, `(2+3)*4`=20, `12/2*3`=18, `10-4-3`=3, `2+3↑2`=11, `2↑3*2`=16 |
| Division | `7/2`=3.5; `10/0` → ?DIVISION BY ZERO  ERROR |
| INT | `INT(7.9)`=7, `INT(-2.5)`=-3 (floor), `INT(2.5+.5)`=3 |
| Number display | `.5` (no leading 0), `1E+10`, `1E-03`, `.333333333`, `(13+14+15)/45*100` = 93.3333334 (last digit 4) |
| RND after reset | first three `RND(1)`: .185564016, .0468986348, .827743801, identical every reset |
| Seeding | `X=RND(-TI)` then `RND(1)` differs across resets |
| FRE(0) at boot | -26627 (add 65536 → 38909) |
| A lone period | `?.` → 0 |

## Statements and program flow

| Fact | Detail |
| --- | --- |
| Functions alone | `STR$(5)`, `LEN("DRAGON")` as statements → ?SYNTAX  ERROR |
| IF | `IF 1 THEN 30` and `IF 1 GOTO 50` both jump; there is NO `ELSE` (prints the THEN part, then ?SYNTAX  ERROR) |
| GO TO | `GO TO 30` works; bare `GOTO` → line 0 |
| RUN n vs GOTO n | `A=7:GOTO 20` keeps A (7); `A=7:RUN 20` clears it (0) |
| STOP / CONT | STOP → BREAK IN n; CONT resumes |
| FOR | Always runs at least once: `FOR I=10 TO 1` runs once, then I=11. After `FOR I=0 TO 10`, I=11; after `FOR I=10 TO 1 STEP -1`, I=0 |
| INPUT | Prompt needs `;` (`INPUT "NAME",N$` → ?SYNTAX  ERROR IN 10); INPUT adds "? " (prompt ending in ? shows ??); INPUT can't be used in direct mode |
| PRINT | Commas → 10-column zones; `PRINT` alone prints an empty line; items side by side act like `;`. PRINT never erases the rest of a row (READY over READY! leaves READY!); spaces in quotes do overwrite |
| SPC(n) on screen | Moves the cursor right WITHOUT erasing: SPC(3);"Y" over XXXXXXXX gives XXXYXXXX. No control code clears a line |
| Control code in a variable | CS$=CHR$(147) then PRINT CS$;"LEVEL 1" clears and prints |
| DEF FN | Program mode only; creates the parameter variable; parameter is restored after the call |

## Screen editor and memory (used by the course site)

| Fact | Detail |
| --- | --- |
| Typed line length | 79 maximum: typing the 80th character wraps and RETURN enters the empty row |
| Logical lines | Link table at 217–241 (high bit = row starts a line). The maze joins rows in pairs, so the screen scrolls two rows at a time |
| Error text | Two spaces before ERROR: `?SYNTAX  ERROR IN 20` |
| Cursor | row = PEEK(214); column within the logical line = PEEK(211) (0–79) |
| Modes | PEEK(157)=128 direct mode, 0 program; PEEK(204)=0 waiting for input; PEEK(212) quote mode; PEEK(216) insert count |
| Keyboard buffer | 631–640, count at 198 |
| Program pointers | TXTTAB 43/44, VARTAB 45/46, ARYTAB 47/48, STREND 49/50 |
| Variable table | 7 bytes each: 2-byte name (bit 7 of byte 1 / byte 2: 00 number, 01 string, 11 integer, 10 FN), then value: 5-byte float; integer high byte first; string = length + address (literals point into program text); FN = formula address + parameter address |
| Array table | name, total length (low/high), dimension count, sizes stored LAST dimension first (high/low); elements with the FIRST index varying fastest; 5/2/3 bytes per element |
| Picture geometry | 384 × 270 visible pixels, text area 320 × 200 at (32, 35) |

## Emulator (vc64web, as embedded in the course site)

| Fact | Detail |
| --- | --- |
| Unmapped keys (course site adds them) | RUN/STOP=Esc, RESTORE=Page Up, CLR/HOME=Home, clear=Shift+Home, INSERT=Insert or Shift+Backspace (vc64web ignores Shift on Backspace), ↑=^ |
| Character ROM | Standard 901225-01 begins 3C 66 6E; the Japanese 906143-02 must not be used |
| Not reliable for testing | auto-type and key events (see CLAUDE.md pitfalls) |

## Characters (PETSCII and screen codes)

| Fact | Detail |
| --- | --- |
| Two numbering systems | PETSCII (CHR$, ASC, PRINT) vs screen codes (screen memory, POKE/PEEK): A = 65 vs 1. Full verified table: `reference/30-petscii.json` (screen codes measured: `reference/data/petscii_probe.json`) |
| Keyboard decode tables | KERNAL $EB79 holds pointers: plain $EB81, SHIFT $EBC2, C= $EC03, CTRL $EC78; 64 bytes each in matrix order (W=87 check). Source of every "type it" combination |
| Color codes → color numbers | 144→0 black, 5→1 white, 28→2 red, 159→3 cyan, 156→4 purple, 30→5 green, 31→6 blue, 158→7 yellow, 129→8 orange, 149→9 brown, 150→10 light red, 151→11 dark grey, 152→12 grey, 153→13 light green, 154→14 light blue, 155→15 light grey |
| Reverse | CHR$(18) then "A" → screen code 129 (1 + 128) |
| Character sets | CHR$(14): 53272 goes 21 → 23 (lower/upper); CHR$(142) back to 21 |
| Case lock | CHR$(8): location 657 = 128; CHR$(9): 0 |
| Cursor and editing codes | 17 down, 145 up, 29 right, 157 left, 19 home, 147 clear, 20 delete (closes gap), 148 insert (opens gap): verified by position |
