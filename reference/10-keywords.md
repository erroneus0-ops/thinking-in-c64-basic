# Keyword index

<!--KEYWORD-INDEX-->

## Abbreviations

Most keywords can be entered in an abbreviated form: one or more leading letters typed normally, followed by the next letter typed with SHIFT. The interpreter stores the abbreviation as the full keyword's token, so it saves typing but not memory, and `LIST` always shows the keyword in full.

The rules, verified by entering each abbreviation:

- The shifted letter can never be a keyword's **last** character. In the keyword table, the final character of each keyword has its high bit set, as a shifted letter does, so a shifted final letter matches as an ordinary character and the keyword is not recognized. This is why `IF`, `ON`, `OR`, `TO`, `FN`, `REM`, `NEW` and `INT` have no abbreviation.
- Keywords are tried in token order, and the first match wins. A shorter abbreviation may already belong to an earlier keyword: L ⇧E is `LET` (token $88), so `LEN` (token $C3) cannot use it; C ⇧O is `CONT`, not `COS`; L ⇧O is `LOAD`, not `LOG`; P ⇧O is `POKE`, not `POS`; T ⇧A is `TAB(`, not `TAN`.
- `PRINT` has no abbreviation in this sense; instead, `?` is accepted in place of the whole word and stored as the `PRINT` token.
- `INPUT` and `GO` have none.

Of the 76 keywords, 52 have an abbreviation; each is listed in the index above.

An abbreviated line that would `LIST` longer than 80 characters can be stored but cannot be edited after listing, because the screen editor reads at most one 80-character logical line.

## Reserved variables and constants

| Name | Value | Notes |
| --- | --- | --- |
| `ST` | Status byte of the last input/output operation | Read-only. `ST = 1` gives `?SYNTAX  ERROR`. Any variable name beginning with ST refers to it. |
| `TI` | Jiffy clock: 1/60 seconds since power-on or the last setting of `TI$` | Read-only. `TI = 1` gives `?SYNTAX  ERROR`. Any name beginning with TI refers to it. |
| `TI$` | The jiffy clock as a six-digit string `HHMMSS` | Assignable with a six-digit string (`TI$ = "093000"`). Other strings give `?ILLEGAL QUANTITY  ERROR`. Any string name beginning with TI, such as `TITLE$`, refers to it. |
| π | 3.14159265 | Entered with SHIFT + ↑. Stored as token $FF. |
