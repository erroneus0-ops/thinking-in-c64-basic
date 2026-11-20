"""Build the C64 tour: docs/tour/index.html plus its screenshots (from tools/tour_shots/).
Run after tools/capture_tour.py whenever the course site's look changes."""
import html, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "tour"

# (title, image or None, body as HTML)
SLIDES = [
    ("A real Commodore 64, in your browser", "ready",
     "<p>This is a full C64, the 1982 home computer, running inside a web page. When you see "
     "<code>READY.</code> and a blinking square, it’s waiting for you.</p>"
     "<p>Ten quick slides show you everything you need. Use the arrows, your keyboard’s arrow keys, or swipe.</p>"),
    ("Click, then type. Caps Lock off.", "capslock",
     "<p>Click the C64 screen first, so your typing goes to the C64.</p>"
     "<p>Type in ordinary small letters: the C64 shows them as capitals. Typing real capitals, with Shift or "
     "Caps Lock, gives graphics symbols instead. That’s the strange line here, and why it ended in an error.</p>"),
    ("Nothing happens until you press RETURN", "return",
     "<p>Think of the screen as a web form. Each line is sent to the C64 only when you press "
     "<kbd>RETURN</kbd> (Enter on your keyboard). In the book, a <kbd>↵</kbd> at the end of a line means: press it.</p>"
     "<p>A line with a number in front is stored for later. <code>RUN</code> carries it out.</p>"),
    ("Errors are normal", "error",
     "<p>When the C64 doesn’t understand, it says so: <code>?SYNTAX  ERROR</code>. Here, the name GOLD "
     "hides the word GO, which the C64 has claimed for itself. Changing it to GLD fixed it.</p>"
     "<p>Every C64 programmer meets errors all the time. Each one is a clue.</p>"),
    ("The special keys", "keys",
     "<p><kbd>Esc</kbd> is <strong>RUN/STOP</strong>: it stops a running program.<br>"
     "<kbd>Shift</kbd> + <kbd>Home</kbd> clears the screen (on many laptops, Home is <kbd>Fn</kbd> + <kbd>←</kbd>).<br>"
     "<kbd>Page Up</kbd> is <strong>RESTORE</strong>.</p>"
     "<p>Prefer clicking? The same keys are buttons beside the C64.</p>"),
    ("Shift-click to move the cursor", "shiftclick",
     "<p>Hold <kbd>Shift</kbd> and click anywhere on the C64 screen, and the cursor jumps there. Here it "
     "landed on the I of PIRNT, ready to fix the typo by typing over it.</p>"
     "<p>It works while you’re typing commands. While a program runs, it waits.</p>"),
    ("Pick the exercise first", "picker",
     "<p>Before you submit, choose the exercise you’re working on from the <strong>Exercise</strong> list, "
     "so your program is filed in the right place. <strong>Free practice</strong> is for anything else.</p>"
     "<p>Chapter 1 has nothing to submit: you type commands that run right away. Programs to submit start in Chapter 2.</p>"),
    ("Submit saves a new version", "submit",
     "<p><strong>Submit program</strong> saves whatever program is in the C64’s memory right now. Each "
     "submit becomes a new version: 1, 2, 3 and so on. Nothing is ever overwritten.</p>"
     "<p>Submit before you press <strong>Reset</strong> (which clears the C64’s memory) and before you try "
     "something risky. It costs nothing.</p>"),
    ("Run, Load, and Listing", "load",
     "<p><strong>Run</strong> puts a saved version back into the C64 and runs it.<br>"
     "<strong>Load</strong> puts it back and lists it, so you can keep working on it. Submit again when "
     "you’re done, and it becomes the next version.<br>"
     "<strong>Listing</strong> just shows the program as text. The C64 isn’t touched.</p>"
     "<p>Careful: Run and Load <em>replace</em> whatever is in the C64 right now. Submit first if you want to keep it.</p>"),
    ("On a phone or tablet", "phone",
     "<p>Phones can’t show their own keyboard for the C64, so tap <strong>Show keyboard</strong> under the "
     "screen for a real C64 keyboard to tap on.</p>"
     "<p>Reading and running work great on a phone. For writing longer programs, a computer is easier.</p>"),
    ("Chapter work: exercises, quiz, notes", "work",
     "<p>Each chapter has exercises, a five-question quiz, and space for your notes: what was confusing, "
     "what was boring, what was fun. Everything is saved as you go.</p>"
     "<p>Take a quiz as many times as you like. Every attempt is kept, so you can watch your scores climb.</p>"),
    ("A discovery, not a failure", None,
     "<p class=\"big\">Every mistake you make on the C64 teaches you something about how it works.</p>"
     "<p>You don’t need to remember all of this. Come back to this tour whenever you like.</p>"
     "<p><a class=\"btn\" href=\"../\">Back to the book</a></p>"),
]

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "img").mkdir(exist_ok=True)
    sections = []
    for i, (title, img, body) in enumerate(SLIDES, 1):
        picture = ""
        if img:
            shutil.copy(ROOT / "tools" / "tour_shots" / f"{img}.webp", OUT / "img" / f"{img}.webp")
            picture = f'<figure><img src="img/{img}.webp" alt="" loading="{"eager" if i < 3 else "lazy"}"></figure>'
        sections.append(f'<section class="slide{"" if img else " closing"}" id="slide-{i}" aria-label="Slide {i} of {len(SLIDES)}">'
                        f'<div class="text"><h1>{html.escape(title)}</h1>{body}</div>{picture}</section>')
    page = (ROOT / "tools" / "tour_template.html").read_text(encoding="utf-8")
    page = page.replace("<!--SLIDES-->", "\n".join(sections)).replace("/*COUNT*/0", str(len(SLIDES)))
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print("wrote", OUT / "index.html", f"({len(SLIDES)} slides)")

if __name__ == "__main__":
    build()
