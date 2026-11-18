"""Lock the editor's edition behind a password, for GitHub Pages.

Reads build/book-editor.html (from `python tools/build.py`), encrypts it, and writes
docs/editor/index.html: a small page that asks for the password and decrypts the book
in the browser. Only the encrypted text is ever published.

The password comes from the C64BOOK_PASSWORD environment variable, or is asked for.
It is never stored in the repo.

Encryption: AES-256-GCM, key from the password via PBKDF2-SHA256 (600,000 rounds),
fresh random salt and nonce every build. Needs: pip install cryptography
"""
import base64, getpass, json, os, pathlib, secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROUNDS = 600_000

def main():
    password = os.environ.get("C64BOOK_PASSWORD") or getpass.getpass("Editor page password: ")
    if len(password) < 10:
        raise SystemExit("Use a password of at least 10 characters.")
    html = (ROOT / "build" / "book-editor.html").read_bytes()
    salt, nonce = secrets.token_bytes(16), secrets.token_bytes(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ROUNDS).derive(password.encode())
    sealed = AESGCM(key).encrypt(nonce, html, None)
    payload = {k: base64.b64encode(v).decode() for k, v in (("salt", salt), ("nonce", nonce), ("data", sealed))}
    payload["rounds"] = ROUNDS
    page = (ROOT / "tools" / "editor_lock_template.html").read_text(encoding="utf-8")
    page = page.replace("/*PAYLOAD*/null", json.dumps(payload))
    out = ROOT / "docs" / "editor"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print("wrote", out / "index.html")

if __name__ == "__main__":
    main()
