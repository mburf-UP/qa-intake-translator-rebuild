"""The two planted faults for Q4 and Q5. Everything outside the named records is left byte for byte.

    python3 harness/mutate.py delete OUTPUT MUTATED   # Q4: remove the MD-DARK-011 record
    python3 harness/mutate.py swap   OUTPUT MUTATED   # Q5: MD-DARK-014's record becomes a copy of MD-DARK-011's

Exits 2 if a named record is not in the output, so the fault cannot be planted.
"""
import sys
from pathlib import Path

from common import parse_records, split_records

DELETED = "MD-DARK-011"
REPLACED = "MD-DARK-014"


def find(text, test_id):
    lines, blocks = split_records(text)
    records = parse_records(text)
    hits = [b for b, r in zip(blocks, records) if r.get("test_id", "").split()[:1] == [test_id]]
    if len(hits) != 1:
        raise LookupError("%s appears in %d records, not 1" % (test_id, len(hits)))
    return lines, hits[0]


def delete(text):
    lines, (s, e) = find(text, DELETED)
    while e < len(lines) and lines[e].strip() == "":
        e += 1  # take the blank line after the record too, so no gap is left where it was
    return lines[:s] + lines[e:]


def swap(text):
    lines, (s1, e1) = find(text, DELETED)
    _, (s2, e2) = find(text, REPLACED)
    return lines[:s2] + lines[s1:e1] + lines[e2:]


def main(argv):
    if len(argv) != 3 or argv[0] not in ("delete", "swap"):
        print(__doc__)
        return 64
    mode, src, dst = argv
    text = Path(src).read_text(encoding="utf-8")
    try:
        out = delete(text) if mode == "delete" else swap(text)
    except LookupError as exc:
        print("CANNOT PLANT: %s" % exc)
        return 2
    Path(dst).write_text("\n".join(out), encoding="utf-8")
    print("planted %s in %s" % (mode, dst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
