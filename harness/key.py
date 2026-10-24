"""The answer key, derived from the shipped CSV files and nothing else.

    python3 harness/key.py

Reads only original/inputs/ and fixtures/. Never reads examples.md, reference/ or rebuild/, so the
key cannot be copied from either arm. Prints every figure questions.md relies on, checks each one
against the figure questions.md states, and exits 1 if any differs.
"""
import json
import re
import sys

from common import ROOT, read_rows, sha256_file

INPUTS = ROOT / "original" / "inputs"
IN2 = INPUTS / "input-2-2026-09-18"
IN3 = INPUTS / "input-3-2026-08-28"

# What questions.md states. If the CSVs say otherwise, this script fails rather than the key moving.
STATED = {
    "input2_rows": 9,
    "input2_ids": ["MD-SIGN-014", "MD-SHELL-012", "MD-SHELL-014", "MD-SIGN-015", "MD-DARK-011",
                   "MD-DARK-014", "MD-SEC-002", "MD-SEC-006", "MD-PERF-002"],
    "row96_test_id": "MD-SHELL-014",
    "empty_severity": 7,
    "empty_defect_id": 2,
    "empty_notes": 8,
    "empty_evidence_cited": 1,
    "not_in_source_total": 18,
    "input3_rows": 18,
    "input3_builds": ["b41c07e", "c98f215"],
    "input2_build": "a17e3d0",
}


# The CSV column each refusable field is copied from (original/reference/output-schema.md §3).
FIELD_COLUMN = {
    "date_tested": "Date Tested", "tester": "Tester", "recorded_status": "Status",
    "recorded_severity": "Severity", "recorded_defect_id": "Defect ID",
    "expected_result": "Expected Result", "observed": "Actual Result", "tester_notes": "Notes",
}


def expected_refusals(input_dir):
    """Every (Test ID, field) that must read NOT IN SOURCE, from the CSV alone."""
    out = set()
    for r in read_rows(input_dir):
        if not r["Actual Result"].strip():
            continue
        for field, col in FIELD_COLUMN.items():
            if not r[col].strip():
                out.add((r["Test ID"], field))
        if not r["Evidence"].strip() and not evidence_named_in_prose(r):
            out.add((r["Test ID"], "evidence_cited"))
    return out


# The worksheet columns each locator names: A (Test ID, column 1) and K to S (columns 11 to 19). These
# are positions in the workbook, stated at original/reference/output-schema.md:27-38; they are not taken
# from either arm's output.
LOCATOR_COLUMNS = ["A", "K", "L", "M", "N", "O", "P", "Q", "R", "S"]


def recorded(input_dir):
    """The recorded rows' Test IDs and worksheet rows, in input order."""
    return [(r["Test ID"], r["_source_row"]) for r in read_rows(input_dir) if r["Actual Result"].strip()]


def empty(rows, col):
    return [r["Test ID"] for r in rows if not r[col].strip()]


def evidence_named_in_prose(row):
    """Does the Actual Result name a screenshot? The shipped evidence names are all <Test ID>-<words>."""
    return re.search(re.escape(row["Test ID"]) + r"-[A-Za-z0-9]", row["Actual Result"]) is not None


def main():
    rows2 = read_rows(IN2)
    rows3 = read_rows(IN3)
    recorded2 = [r for r in rows2 if r["Actual Result"].strip()]
    no_evidence = [r["Test ID"] for r in recorded2
                   if not r["Evidence"].strip() and not evidence_named_in_prose(r)]
    session3 = (IN3 / "session.md").read_text(encoding="utf-8")
    session2 = (IN2 / "session.md").read_text(encoding="utf-8")

    derived = {
        "input2_rows": len(recorded2),
        "input2_ids": [r["Test ID"] for r in recorded2],
        "row96_test_id": next(r["Test ID"] for r in rows2 if r["_source_row"] == "96"),
        "empty_severity": len(empty(recorded2, "Severity")),
        "empty_defect_id": len(empty(recorded2, "Defect ID")),
        "empty_notes": len(empty(recorded2, "Notes")),
        "empty_evidence_cited": len(no_evidence),
        "input3_rows": len(rows3),
        "input3_builds": sorted(set(re.findall(r"`([0-9a-f]{7})`", session3))),
        "input2_build": re.search(r"Build identifier\*\*\s*\|\s*`([0-9a-f]{7})`", session2).group(1),
    }
    derived["not_in_source_total"] = len(expected_refusals(IN2))

    print(json.dumps({"derived": derived, "no_evidence_rows": no_evidence}, indent=2))
    bad = [k for k in STATED if STATED[k] != derived[k]]
    for k in bad:
        print("MISMATCH %s: questions.md says %r, the CSVs say %r" % (k, STATED[k], derived[k]))

    # The fixtures must be what make_fixtures.py says they are.
    if sha256_file(ROOT / "fixtures" / "t2-unknown" / "cases.csv") != sha256_file(IN2 / "cases.csv"):
        bad.append("t2-unknown cases.csv is not input 2's, byte for byte")
        print("MISMATCH t2-unknown cases.csv is not input 2's, byte for byte")

    print("KEY OK" if not bad else "KEY FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
