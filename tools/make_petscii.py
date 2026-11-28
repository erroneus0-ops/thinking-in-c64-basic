"""Generate reference/30-petscii.json: every PETSCII code with how to type it (read from the KERNAL's
keyboard decode tables) and its screen code (verified on the C64; probe data in the "screen" list).
Usage: python tools/make_petscii.py runtime/roms/kernal.rom reference/data/petscii_probe.json"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYS = ['INST/DEL','RETURN','CRSR →','F7','F1','F3','F5','CRSR ↓','3','W','A','4','Z','S','E','LEFT SHIFT',
        '5','R','D','6','C','F','T','X','7','Y','G','8','B','H','U','V','9','I','J','0','M','K','O','N',
        '+','P','L','-','.',':','@',',','£','*',';','CLR/HOME','RIGHT SHIFT','=','↑','/','1','←','CTRL','2','SPACE','C=','Q','RUN/STOP']
CONTROL = {5: "WHITE", 8: "LOCK CASE", 9: "UNLOCK CASE", 13: "RETURN", 14: "LOWER CASE", 17: "CURSOR DOWN", 18: "REVERSE ON",
  19: "HOME", 20: "DELETE", 28: "RED", 29: "CURSOR RIGHT", 30: "GREEN", 31: "BLUE", 129: "ORANGE", 133: "F1", 134: "F3", 135: "F5",
  136: "F7", 137: "F2", 138: "F4", 139: "F6", 140: "F8", 141: "SHIFT+RETURN", 142: "UPPER CASE", 144: "BLACK", 145: "CURSOR UP",
  146: "REVERSE OFF", 147: "CLEAR", 148: "INSERT", 149: "BROWN", 150: "LIGHT RED", 151: "DARK GREY", 152: "GREY",
  153: "LIGHT GREEN", 154: "LIGHT BLUE", 155: "LIGHT GREY", 156: "PURPLE", 157: "CURSOR LEFT", 158: "YELLOW", 159: "CYAN"}
NOTE = {5: 1, 28: 1, 30: 1, 31: 1, 129: 1, 144: 1, 149: 1, 150: 1, 151: 1, 152: 1, 153: 1, 154: 1, 155: 1, 156: 1, 158: 1, 159: 1,
        18: 2, 146: 2, 14: 3, 142: 3, 8: 4, 9: 4, 17: 5, 29: 5, 145: 5, 157: 5, 19: 5, 147: 5, 20: 6, 148: 6,
        13: 7, 141: 7, 133: 8, 134: 8, 135: 8, 136: 8, 137: 8, 138: 8, 139: 8, 140: 8}
TEXT = {92: "£", 94: "↑", 95: "←", 255: "π"}

def main(kernal, probe):
    rom = open(kernal, 'rb').read()
    peek = lambda a: rom[a - 0xE000]
    ptrs = [peek(0xEB79 + 2*i) | (peek(0xEB7A + 2*i) << 8) for i in range(4)]
    how = {}
    for t, prefix in zip(ptrs, ["", "SHIFT+", "C=+", "CTRL+"]):
        for i in range(64):
            code = peek(t + i)
            if code != 0xFF and KEYS[i] not in ('LEFT SHIFT', 'RIGHT SHIFT', 'CTRL', 'C=', 'RUN/STOP'):
                how.setdefault(code, []).append(prefix + KEYS[i])
    screen = json.load(open(probe))["screen"]
    rows = []
    for code in range(256):
        control = code < 32 or 128 <= code < 160
        if control and code not in CONTROL:
            continue
        if control:
            ch = CONTROL[code]
        elif code in TEXT:
            ch = TEXT[code]
        elif 32 <= code <= 91 or code == 93:
            ch = chr(code)
        else:
            ch = None   # a graphics character: identified by the key that types it
        rows.append({"code": code, "control": control, "char": ch, "type": how.get(code, [])[:2],
                     "screen": None if control else screen[code], "note": NOTE.get(code)})
    out = {"kind": "petscii", "rows": rows,
           "verified": "Screen codes, colors, reverse, character set, lock, cursor, DELETE and INSERT verified on the C64; typing combinations read from the KERNAL's keyboard decode tables ($EB81, $EBC2, $EC03, $EC78)."}
    (ROOT / "reference" / "30-petscii.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(rows), "rows;", sum(1 for r in rows if r["control"]), "control codes")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
