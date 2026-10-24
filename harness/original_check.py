"""The original's own check, done exactly as its README states it, so Q4 and Q5 can run it.

    python3 harness/original_check.py OUTPUT INPUT_DIR

original/README.md:102-103: "Open the coverage block. Does `records_out` equal `rows_recorded`? Count
the data rows in the CSV. That equality is the whole guarantee and it is arithmetic."

Passes (exit 0) when the printed records_out equals the printed rows_recorded and both equal the CSV's
recorded rows. It reads the printed numbers only, because that is what the README tells a reader to do.
It does not count the records, because the README does not say to.
"""
import sys
from pathlib import Path

from common import coverage_number, read_rows


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 64
    text = Path(argv[0]).read_text(encoding="utf-8")
    csv_rows = sum(1 for r in read_rows(argv[1]) if r["Actual Result"].strip())
    out = coverage_number(text, "records_out")
    rec = coverage_number(text, "rows_recorded")
    print("records_out (printed)    %s" % out)
    print("rows_recorded (printed)  %s" % rec)
    print("data rows in the CSV     %d" % csv_rows)
    ok = out is not None and out == rec == csv_rows
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
