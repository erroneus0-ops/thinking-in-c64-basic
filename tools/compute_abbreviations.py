"""Compute BASIC V2 keyword abbreviations from the keyword table order (see reference/10-keywords.md
for the rules). The shifted letter may not be a keyword's last character. Output: abbreviation
per keyword, lowercase = typed plainly, capital = typed with SHIFT. Verify with
tools/verify_abbreviations.py against the running course site."""
# BASIC V2 keyword table, in token order from $80 (as in the ROM; also site/assets/c64.js).
T = ['END','FOR','NEXT','DATA','INPUT#','INPUT','DIM','READ','LET','GOTO','RUN','IF','RESTORE',
  'GOSUB','RETURN','REM','STOP','ON','WAIT','LOAD','SAVE','VERIFY','DEF','POKE','PRINT#','PRINT','CONT',
  'LIST','CLR','CMD','SYS','OPEN','CLOSE','GET','NEW','TAB(','TO','FN','SPC(','THEN','NOT','STEP','+','-',
  '*','/','^','AND','OR','>','=','<','SGN','INT','ABS','USR','FRE','POS','SQR','RND','LOG','EXP','COS',
  'SIN','TAN','ATN','PEEK','LEN','STR$','VAL','ASC','CHR$','LEFT$','RIGHT$','MID$','GO']
assert len(T) == 76
def winner(prefix, shifted):
    """What the tokenizer makes of the typed text prefix+SHIFT(shifted): the first keyword in table
    order that either matches completely within the unshifted prefix, or matches the prefix and then
    has `shifted` at the next position (an abbreviation ends a match)."""
    k = len(prefix)
    for J in T:
        if len(J) <= k and prefix[:len(J)] == J:      # a whole keyword matched before the shift
            return J
        if len(J) > k and J[:k] == prefix and J[k] == shifted:
            return J
    return None
abbr = {}
for K in T:
    if len(K) < 2 or not K[0].isalpha():
        continue
    for k in range(1, len(K) - 1):          # never shift the keyword's last character
        if not K[k].isalpha():           # only a shifted LETTER can end an abbreviation
            break
        if winner(K[:k], K[k]) == K:
            abbr[K] = K[:k].lower() + K[k]   # lowercase = typed plainly, capital = typed with SHIFT
            break
import json; json.dump(abbr, open('abbr.json','w'), indent=1)
none = [K for K in T if K[0].isalpha() and len(K) > 1 and K not in abbr]
print(len(abbr), "keywords have an abbreviation; none for:", none)
print({k: abbr[k] for k in ['LIST','LEFT$','LET','GOTO','GOSUB','RETURN','RESTORE','READ','RUN','PRINT#','INPUT#','STR$','STEP']})
