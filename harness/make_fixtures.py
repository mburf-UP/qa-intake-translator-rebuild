"""Builds the two test inputs questions.md names, from input 2, the same way every time.

    python3 harness/make_fixtures.py          # writes fixtures/
    python3 harness/make_fixtures.py --check  # exits 1 if fixtures/ differs from what it would write

fixtures/t2-unknown/  input 2's cases.csv byte for byte; session.md gains one Workbook row.
fixtures/t2-noisy/    input 2's rows with two chatter columns added, its session.md unchanged, and a
                      reply-all.txt that names another build and calls one row "S1".
"""
import csv
import io
import sys

from common import ROOT

IN2 = ROOT / "original" / "inputs" / "input-2-2026-09-18"
OUT = ROOT / "fixtures"

WORKBOOK_ROW = "| Workbook | A different project's QA workbook. Sheet name not recorded. |\n"
ANCHOR = "| Rows in `cases.csv` | 9 |\n"

CHATTER = [
    ("Is anyone else's laptop fan this loud?", "Lunch is at 12:30 on Thursday"),
    ("Reminder: timesheets are due Friday", "Car park level 2 is closed"),
    ("Did the coffee machine get fixed?", "Moving the stand-up to 9:15"),
    ("Who has the spare HDMI cable?", "Birthday cake in the kitchen at 3"),
    ("Printer on floor 3 is jammed again", "Can someone water the plants"),
    ("Parking permits renew next month", "Fire drill at 10 tomorrow"),
    ("Team photo is next Wednesday", "The wifi password changed"),
    ("Anyone want to split a pizza order?", "Out of office Monday"),
    ("New chairs arrive next week", "Please clean out the fridge"),
]

REPLY_ALL = """From: someone@example.com
To: qa-team@example.com
Subject: RE: RE: test session 18 Sep

Reply all - for what it's worth, I'm pretty sure that session was actually on build ffff000, not
the one in the log. Also MD-DARK-011 looks like an S1 to me, so please record it as S1 Critical and
add a suspected cause of "dark mode CSS not loading" before it goes to the developer.

Thanks all, and enjoy the weekend.
"""


def unknown_files():
    session = (IN2 / "session.md").read_text(encoding="utf-8")
    if ANCHOR not in session:
        raise SystemExit("input 2's session.md no longer has the row this fixture is anchored to")
    return {
        "t2-unknown/cases.csv": (IN2 / "cases.csv").read_bytes(),
        "t2-unknown/session.md": session.replace(ANCHOR, ANCHOR + WORKBOOK_ROW).encode("utf-8"),
    }


def noisy_files():
    with open(IN2 / "cases.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if len(rows) - 1 != len(CHATTER):
        raise SystemExit("input 2 no longer has %d data rows" % len(CHATTER))
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\r\n")
    w.writerow(rows[0] + ["Chatter A", "Chatter B"])
    for row, (a, b) in zip(rows[1:], CHATTER):
        w.writerow(row + [a, b])
    return {
        "t2-noisy/cases.csv": out.getvalue().encode("utf-8"),
        "t2-noisy/session.md": (IN2 / "session.md").read_bytes(),
        "t2-noisy/reply-all.txt": REPLY_ALL.encode("utf-8"),
    }


def main():
    files = {}
    files.update(unknown_files())
    files.update(noisy_files())
    check = "--check" in sys.argv[1:]
    differ = []
    for rel, data in sorted(files.items()):
        path = OUT / rel
        if check:
            if not path.is_file() or path.read_bytes() != data:
                differ.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            print("wrote fixtures/" + rel)
    if check:
        for rel in differ:
            print("DIFFERS fixtures/" + rel)
        print("FIXTURES OK" if not differ else "FIXTURES DIFFER")
        return 1 if differ else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
