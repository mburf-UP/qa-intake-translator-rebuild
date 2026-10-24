"""Checks a translator output against the input it came from. Python 3.9 or later, standard library only.

    python3 check.py OUTPUT-FILE INPUT-DIR

Counts the records actually present, instead of trusting the numbers the output prints about itself.

For an output with records (reference/output-schema.md §3 and §5):
  - every recorded row in INPUT-DIR/cases.csv has exactly one record, in input row order;
  - every record has the fourteen fields, in order, each once;
  - the printed rows_recorded equals the CSV's recorded rows, and the printed records_out equals the
    records actually present.

For a stopped run (§6.1): the six stop lines are present in order, there are no records, rows_in is the
CSV's row count and records_out is 0.

Prints one line per problem, then PASS or FAIL. Exit 0 on PASS, 1 on FAIL, 2 if it cannot read its input.
Problem lines start with a fixed word so they can be searched for: MISSING, DUPLICATE, UNEXPECTED,
ORDER, INCOMPLETE, COUNT, STOP.

It checks presence, order and shape. It does not check that any value is right.
"""
import csv
import re
import sys
from pathlib import Path

FIELDS = [
    "intake_id", "test_id", "build", "date_tested", "tester", "recorded_status",
    "recorded_severity", "recorded_defect_id", "expected_result", "observed", "tester_notes",
    "evidence_cited", "observation_spans", "source",
]
STOP_LINES = ["RUN STOPPED", "Condition", "Detail", "Remedy", "rows_in", "records_out"]

_FIELD = re.compile(r"^\**([a-z_]+)\**:?(?:[ \t]+(.*))?$")
_FENCE = re.compile(r"^\s*```")


def records(text):
    """Each record's fields, in the order they appear. A record starts at a line beginning `intake_id`
    and ends at the next one, or at the first line that is neither indented nor a field name."""
    out, current = [], None
    for ln in text.split("\n"):
        ln = ln.rstrip("\r")
        m = _FIELD.match(ln)
        name = m.group(1) if m else None
        if name == "intake_id":
            current = {"fields": ["intake_id"], "test_id": ""}
            out.append(current)
            continue
        if current is None:
            continue
        if ln.strip() == "" or ln[:1] in (" ", "\t"):
            continue
        if name in FIELDS and not _FENCE.match(ln):
            current["fields"].append(name)
            if name == "test_id":
                current["test_id"] = (m.group(2) or "").split()[0] if (m.group(2) or "").split() else ""
            continue
        current = None
    return out


def printed(text, name):
    m = re.search(r"(?m)^[\s|`*>-]*%s[`*|:\s]+(\d+)" % re.escape(name), text)
    return int(m.group(1)) if m else None


def starts(line, label):
    return re.match(r"^[\s|`*>-]*%s\b" % re.escape(label), line) is not None


_STOP_LINE = {
    "Condition": re.compile(r"^Condition:[ \t]+\S"),
    "Detail": re.compile(r"^Detail:[ \t]+\S"),
    "Remedy": re.compile(r"^Remedy:[ \t]+\S"),
    "rows_in": re.compile(r"^rows_in[ \t]+(\d+)[ \t]*$"),
    "records_out": re.compile(r"^records_out[ \t]+(\d+)[ \t]*$"),
}


def check_stop(text, rows, recs):
    """The stop output of reference/output-schema.md §6.1: the first line, then the five labelled lines
    in order, each once and each with a value. Only Condition, Detail and Remedy may run on to indented
    lines. Nothing else, outside code fences and blank lines."""
    problems = []
    lines = [ln.rstrip("\r") for ln in text.split("\n")
             if ln.strip() and not _FENCE.match(ln)]
    if not lines or lines[0].strip() != "RUN STOPPED — no records produced.":
        problems.append("STOP the first line is not `RUN STOPPED — no records produced.`")
    seen, last = [], None
    for ln in lines[1:]:
        label = next((k for k, rx in _STOP_LINE.items() if rx.match(ln)), None)
        if label:
            seen.append(label)
            last = label
        elif ln[:1] in (" ", "\t") and last in ("Condition", "Detail", "Remedy"):
            continue
        else:
            problems.append("STOP extra text, not part of the stop output: %s" % ln.strip()[:60])
    if seen != STOP_LINES[1:]:
        problems.append("STOP labelled lines are %s; required, each once and in order: %s"
                        % (", ".join(seen) or "none", ", ".join(STOP_LINES[1:])))
    if recs:
        problems.append("STOP output contains %d records; a stopped run has none" % len(recs))
    rows_in = next((int(_STOP_LINE["rows_in"].match(l).group(1)) for l in lines if _STOP_LINE["rows_in"].match(l)), None)
    out = next((int(_STOP_LINE["records_out"].match(l).group(1)) for l in lines if _STOP_LINE["records_out"].match(l)), None)
    if rows_in != len(rows):
        problems.append("COUNT rows_in printed %s, CSV has %d rows" % (rows_in, len(rows)))
    if out != 0:
        problems.append("COUNT records_out printed %s, a stopped run has 0" % out)
    return problems


def check_records(text, rows, recs):
    problems = []
    want = [r["Test ID"] for r in rows if r["Actual Result"].strip()]
    got = [r["test_id"] for r in recs]
    for tid in sorted(set(got)):
        if got.count(tid) > 1:
            problems.append("DUPLICATE %s appears in %d records" % (tid, got.count(tid)))
        if tid not in want:
            problems.append("UNEXPECTED %s has a record but no recorded row in the CSV" % (tid or "(no test_id)"))
    for tid in want:
        if tid not in got:
            problems.append("MISSING %s is a recorded row in the CSV and has no record" % tid)
    present = [t for t in got if t in want]
    if not problems and present != want:
        problems.append("ORDER records are not in input row order: %s" % ", ".join(present))
    for r in recs:
        if r["fields"] != FIELDS:
            problems.append("INCOMPLETE %s does not have the fourteen fields, in order, each once"
                            % (r["test_id"] or "(no test_id)"))
    rec_printed = printed(text, "rows_recorded")
    out_printed = printed(text, "records_out")
    if rec_printed != len(want):
        problems.append("COUNT rows_recorded printed %s, CSV has %d recorded rows" % (rec_printed, len(want)))
    if out_printed != len(recs):
        problems.append("COUNT records_out printed %s, %d records are present" % (out_printed, len(recs)))
    return problems


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        text = Path(argv[0]).read_text(encoding="utf-8")
        with open(Path(argv[1]) / "cases.csv", newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except (OSError, UnicodeDecodeError) as exc:
        print("cannot read input: %s" % exc)
        return 2
    if not rows or "Test ID" not in rows[0] or "Actual Result" not in rows[0]:
        print("cannot read input: %s/cases.csv has no Test ID and Actual Result columns" % argv[1])
        return 2
    recs = records(text)
    stopped = any(starts(ln, "RUN STOPPED") for ln in text.split("\n"))
    problems = check_stop(text, rows, recs) if stopped else check_records(text, rows, recs)
    for p in problems:
        print(p)
    print("FAIL" if problems else "PASS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
