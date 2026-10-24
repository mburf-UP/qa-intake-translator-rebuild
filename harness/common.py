"""Shared helpers for the harness. Python 3.9 or later, standard library only.

Nothing here reads original/ or rebuild/ to decide what is correct. The answer key comes from the
CSV files alone (key.py); these helpers only read outputs and folders so they can be scored.
"""
import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The fourteen fields, in order (feedback.md line 11: "Fourteen fields, same order").
FIELDS = [
    "intake_id", "test_id", "build", "date_tested", "tester", "recorded_status",
    "recorded_severity", "recorded_defect_id", "expected_result", "observed", "tester_notes",
    "evidence_cited", "observation_spans", "source",
]
COVERAGE = [
    "build", "rows_in", "rows_recorded", "rows_not_recorded", "records_out",
    "substantive_pass_rows", "multi_observation_rows", "evidence_not_found", "refusal_counts",
]
REFUSALS = ("NOT IN SOURCE", "IN SOURCE, UNRESOLVABLE", "NOT APPLICABLE")

_FIELD = re.compile(r"^\**([a-z_]+)\**:?(?:[ \t]+(.*))?$")
_FENCE = re.compile(r"^\s*```")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def tree_hashes(folder):
    """SHA-256 of every file under folder, keyed by its path relative to folder."""
    folder = Path(folder)
    return {
        str(p.relative_to(folder)): sha256_file(p)
        for p in sorted(folder.rglob("*")) if p.is_file()
    }


def read_rows(input_dir):
    with open(Path(input_dir) / "cases.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _lines(text):
    """The output's lines, with Markdown code fences removed."""
    return [ln.rstrip("\r") for ln in text.split("\n") if not _FENCE.match(ln)]


def split_records(text):
    """Return (lines, blocks): each block is (start, end) line indexes of one record.

    A record starts at a line beginning `intake_id`. It continues through field lines, indented
    continuation lines and blank lines, and ends at the next `intake_id`, or at the first line that is
    neither indented nor a field name (a code fence included, so fences are left where they are).
    """
    lines = [ln.rstrip("\r") for ln in text.split("\n")]
    blocks = []
    start = None
    for i, ln in enumerate(lines):
        m = _FIELD.match(ln)
        name = m.group(1) if m else None
        if name == "intake_id":
            if start is not None:
                blocks.append((start, _trim(lines, start, i)))
            start = i
            continue
        if start is None:
            continue
        if ln.strip() == "" or ln[:1] in (" ", "\t") or name in FIELDS:
            continue
        blocks.append((start, _trim(lines, start, i)))
        start = None
    if start is not None:
        blocks.append((start, _trim(lines, start, len(lines))))
    return lines, blocks


def _trim(lines, start, end):
    while end > start and lines[end - 1].strip() == "":
        end -= 1
    return end


def parse_records(text):
    """Every record in an output, as a dict of field name to value (continuation lines joined by \\n)."""
    lines, blocks = split_records(text)
    records = []
    for start, end in blocks:
        rec = {}
        current = None
        for ln in lines[start:end]:
            m = _FIELD.match(ln)
            if m and m.group(1) in FIELDS and ln[:1] not in (" ", "\t"):
                current = m.group(1)
                if current in rec:
                    rec["(duplicate field)"] = current  # makes the record incomplete
                rec[current] = (m.group(2) or "").strip()
            elif current is not None and ln.strip():
                rec[current] += "\n" + ln.strip()
        records.append(rec)
    return records


def coverage_number(text, name):
    """The first number printed after a coverage field name at the start of a line, or None."""
    m = re.search(r"(?m)^%s[ \t]+(\d+)" % re.escape(name), "\n".join(_lines(text)))
    return int(m.group(1)) if m else None


def printed_refusal_count(text, verdict="NOT IN SOURCE"):
    """The count printed beside a verdict in a coverage block's refusal_counts, or None."""
    m = re.search(r"(?m)^(?:refusal_counts)?[ \t]*%s[ \t]+(\d+)[ \t]*$" % re.escape(verdict),
                  "\n".join(_lines(text)))
    return int(m.group(1)) if m else None


def complete(rec):
    """True if the record has exactly the fourteen fields, in order."""
    return list(rec.keys()) == FIELDS


def is_refusal(value, verdict="NOT IN SOURCE"):
    """True if the whole value is the verdict alone, optionally followed by one parenthesised note."""
    return re.match(r"^%s(?:\s+\([^()\n]*\))?$" % re.escape(verdict), value.strip()) is not None


def refusal_cells(records, verdict="NOT IN SOURCE"):
    """The (test_id, field) pairs whose value is that verdict. `source` and spans are not values."""
    out = set()
    for rec in records:
        tid = rec.get("test_id", "").split()[0] if rec.get("test_id", "").strip() else ""
        for name in FIELDS:
            if name not in ("source", "observation_spans") and is_refusal(rec.get(name, ""), verdict):
                out.add((tid, name))
    return out


def answer_line(text):
    """The value after the last line beginning `ANSWER:`, or None."""
    found = re.findall(r"(?m)^\**ANSWER:\**[ \t]*(.+?)[ \t]*$", text)
    return found[-1].strip().strip("`*") if found else None
