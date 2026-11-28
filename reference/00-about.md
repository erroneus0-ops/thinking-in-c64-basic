# About this reference

This volume documents Commodore 64 BASIC V2 completely, in standard terminology: every keyword, operator, reserved variable and error message. It is a companion to *Thinking in C64 BASIC*.

**Verification.** Every example and every stated output in this volume was produced on an emulated C64 running the original Commodore ROMs (BASIC V2, KERNAL 901227-03), and is reproduced exactly as the C64 displays it, including the two spaces before `ERROR` in error messages.

**Coverage.** The keyword index lists all 76 tokens of BASIC V2 plus π. Entries for individual keywords are added in families; the index shows the full scope from the start.

## Conventions

| Notation | Meaning |
| --- | --- |
| `KEYWORD` | Typed exactly as shown (on the C64 keyboard, unshifted letters appear as capitals). |
| *expression* | Any valid expression of the stated type: *numeric expression*, *string expression*. |
| `[ ... ]` | Optional part. |
| { A \| B } | Exactly one of the alternatives. |
| `...` | The preceding item may be repeated. |
| L ⇧I | An abbreviation: type `L`, then hold SHIFT and type `I`. |

## Terminology

| Term | Meaning in this volume |
| --- | --- |
| Keyword | A word reserved by BASIC V2. The interpreter recognizes keywords anywhere outside quotation marks, including inside variable names. |
| Token | The single byte ($80–$CB, and $FF for π) that replaces a keyword when a line is stored. `LIST` converts tokens back into keywords. |
| Statement | An instruction that performs an action, such as `PRINT` or `GOTO`. A line contains one or more statements separated by colons. |
| Function | A keyword that returns a value computed from its argument(s), such as `LEN` or `MID$`. A function cannot stand alone as a statement. |
| Operator | A symbol or keyword that combines values: arithmetic, relational or logical. |
| Expression | A combination of constants, variables, functions and operators that evaluates to a single value. |
| Numeric variable | Floating point: 5 bytes per value, about 9 significant digits. Name has no suffix. |
| Integer variable | Signed 16-bit integer, −32768 to 32767. Name ends in `%`. Arithmetic on integers is performed in floating point. |
| String variable | Up to 255 characters. Name ends in `$`. |
| Variable name | Begins with a letter; may contain letters and digits; only the first two characters are significant. |
| Direct mode | A line entered without a line number is executed immediately. |
| Program mode | A line entered with a line number (0–63999) is stored as part of the program. |
| Logical line | Up to two physical screen rows (80 characters) that the screen editor treats as one line. A line is entered by pressing RETURN with the cursor anywhere on it. |
