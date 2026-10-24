"""Scores one arm against questions.md, from its recorded runs. No mark is set by hand.

    python3 harness/score.py ARM        ARM is `original` or `rebuild`

Reads run-<ARM>/ and the arm's folder, prints each question's mark with every part that decided it,
and writes run-<ARM>/scores.json. A question scores 1 only if every part holds in both runs. The
expected values come from key.py, which reads the CSV files and neither arm. Exit 0 always: a 0 is a
result, not an error.

Q4 and Q5 run each arm's own documented check. For the original that is harness/original_check.py,
which does what original/README.md:102-103 says. For the rebuild it is the command questions.md fixes:
`python3 check.py OUTPUT INPUT_DIR`, run from inside rebuild/.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from common import (ROOT, FIELDS, parse_records, printed_refusal_count, refusal_cells, answer_line,
                    coverage_number, complete, is_refusal)
from key import IN2, LOCATOR_COLUMNS, expected_refusals, recorded

STOP_LABELS = ["RUN STOPPED", "Condition", "Detail", "Remedy", "rows_in", "records_out"]
TWO_BUILDS = "more than one build"
IDS2 = [tid for tid, _ in recorded(IN2)]
ROWS2 = dict(recorded(IN2))


# ---- reading recorded runs ---------------------------------------------------------------

def _ran(d):
    """The text of a run that succeeded, or None if it failed or did not run."""
    if not (d / "meta.json").is_file():
        return None
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    text = (d / "result.md").read_text(encoding="utf-8")
    if meta.get("exit_code") != 0 or meta.get("is_error") or not text.strip():
        return None
    return text


def result(arm, step, n):
    """Run n's text. Its retry is used only if run n failed; a retry after a success is ignored."""
    base = ROOT / ("run-" + arm) / step
    first = _ran(base / ("r%d" % n))
    if first is not None:
        return first
    return _ran(base / ("r%d-retry" % n))


def both(arm, step):
    return [result(arm, step, 1), result(arm, step, 2)]


def records_by_id(text):
    """Complete records keyed by Test ID, plus the list of Test IDs in the order they appear."""
    recs = [r for r in parse_records(text or "")]
    order = [r.get("test_id", "").split()[0] if r.get("test_id", "").strip() else "" for r in recs]
    return recs, order


# ---- reading the arm's folder ------------------------------------------------------------

def reference_files(arm):
    return sorted((ROOT / arm / "reference").glob("*.md"))


def cited_region(arm, answer, must_contain):
    """True if `path:line` names a reference/ file and lines line-3..line+3 contain every text."""
    m = re.match(r"^(?:\./)?(?:%s/)?(reference/[\w.-]+\.md):(\d+)" % re.escape(arm), answer or "")
    if not m:
        return False
    path = ROOT / arm / m.group(1)
    if not path.is_file():
        return False
    lines = path.read_text(encoding="utf-8").split("\n")
    line = int(m.group(2))
    region = "\n".join(lines[max(0, line - 4):line + 3])
    return all(t in region for t in must_contain)


def _starts(line, label):
    return re.match(r"^[\s|`*>-]*%s\b" % re.escape(label), line) is not None


def stop_definition(arm):
    """The lines of a reference/ section that defines the six stop fields, in order, each with a rule.

    A definition runs from a line starting `RUN STOPPED` to the `records_out` line, at most 40 lines,
    with each label starting a line in order (as a table row or a list item), and every label after
    `RUN STOPPED` followed by at least four more words on its line. The two-build condition must be
    named inside that run. Returns the lines, or None.

    This checks the shape of the definition, not the meaning of its prose: no script can. The values T3
    must print are fixed in questions.md Q6, not read from the rebuild's wording.
    """
    for p in reference_files(arm):
        lines = p.read_text(encoding="utf-8").split("\n")
        for i in range(len(lines)):
            if not _starts(lines[i], "RUN STOPPED"):
                continue
            j, ok = i, True
            for label in STOP_LABELS:
                end = min(len(lines), i + 40)
                while j < end and not _starts(lines[j], label):
                    j += 1
                if j >= end:
                    ok = False
                    break
                rest = lines[j].split(label, 1)[1]
                if label != "RUN STOPPED" and len(re.findall(r"[A-Za-z]{2,}", rest)) < 4:
                    ok = False
                    break
                j += 1
            if ok and TWO_BUILDS in "\n".join(lines[i:j]):
                return lines[i:j]
    return None


# ---- the questions -----------------------------------------------------------------------

def q1(arm):
    stated = any(re.search(r"sheet name", ln, re.I) and "Test Cases" in ln
                 for p in reference_files(arm) for ln in p.read_text(encoding="utf-8").split("\n"))
    parts = {"a reference/ line names `Test Cases` as the sheet name": stated}
    for n, t in enumerate(both(arm, "T2"), 1):
        recs, order = records_by_id(t)
        r96 = [r for r, tid in zip(recs, order) if tid == "MD-SHELL-014"]
        parts["T2 r%d: row 96's locator begins `Test Cases!`" % n] = (
            len(r96) == 1 and r96[0].get("source", "").startswith("Test Cases!"))
    for n, t in enumerate(both(arm, "Q1"), 1):
        parts["Q1 r%d: the answer cites a reference/ line that names it" % n] = cited_region(
            arm, answer_line(t or ""), ["Test Cases"])
    return parts


def q2(arm):
    parts = {}
    for n, t in enumerate(both(arm, "T2-unknown"), 1):
        recs, order = records_by_id(t)
        ok = order == IDS2 and all(complete(r) for r in recs)
        for r, tid in zip(recs, order):
            sheet, bang, cells = r.get("source", "").partition("!")
            want = ["%s%s" % (c, ROWS2.get(tid, "?")) for c in LOCATOR_COLUMNS]
            got = re.findall(r"\b[A-Z]{1,2}\d+\b", cells)
            ok = ok and bang == "!" and sheet.strip() == "NOT IN SOURCE" and got == want
        parts["T2-unknown r%d: the nine Test IDs in order, 14 fields each, every locator "
              "`NOT IN SOURCE!` then its own row's cells A, K to S" % n] = ok
    return parts


def q3(arm):
    folder = ROOT / arm
    md = "\n".join(p.read_text(encoding="utf-8") for p in sorted(folder.rglob("*.md"))
                   if "inputs" not in p.relative_to(folder).parts)
    examples = (folder / "examples.md").read_text(encoding="utf-8")
    ex_recs, ex_order = records_by_id(examples)
    row96 = [r for r, tid in zip(ex_recs, ex_order) if tid == "MD-SHELL-014"]
    want = expected_refusals(IN2)
    parts = {
        "no `(none cited)` anywhere in the folder": "(none cited)" not in md,
        "a reference/ line gives `NOT IN SOURCE` as the value of an empty `evidence_cited`": any(
            "evidence_cited" in ln and "NOT IN SOURCE" in ln and re.search(r"\b(empty|no evidence|none)\b", ln, re.I)
            for p in reference_files(arm) for ln in p.read_text(encoding="utf-8").split("\n")),
        "examples.md: every row-96 record's `evidence_cited` is `NOT IN SOURCE` (at least two)": (
            len(row96) >= 2 and all(is_refusal(r.get("evidence_cited", "")) for r in row96)),
        "examples.md: the input-2 `NOT IN SOURCE` count is %d" % len(want): (
            printed_refusal_count(examples) == len(want)),
    }
    for n, t in enumerate(both(arm, "T2"), 1):
        recs, order = records_by_id(t)
        got = refusal_cells(recs)
        parts["T2 r%d: nine complete records, in order" % n] = order == IDS2 and all(complete(r) for r in recs)
        parts["T2 r%d: `NOT IN SOURCE` exactly where the CSV is empty (%d cells, MD-SHELL-014 "
              "evidence_cited among them)" % (n, len(want))] = got == want
        parts["T2 r%d: printed `NOT IN SOURCE` count is %d" % (n, len(want))] = (
            printed_refusal_count(t or "") == len(want))
    for n, t in enumerate(both(arm, "Q3"), 1):
        value, _, cite = (answer_line(t or "") or "").partition("|")
        parts["Q3 r%d: answers `NOT IN SOURCE`, citing a reference/ line about `evidence_cited`" % n] = (
            value.strip().strip("`") == "NOT IN SOURCE" and cited_region(arm, cite.strip(), ["evidence_cited"]))
    return parts


def run_check(arm, output_text):
    """Run the arm's own documented check on an output. Returns (exit code, printed text)."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "output.txt"
        path.write_text(output_text, encoding="utf-8")
        if arm == "original":
            argv, cwd = [sys.executable, str(ROOT / "harness" / "original_check.py"), str(path), str(IN2)], ROOT
        else:
            argv, cwd = [sys.executable, "check.py", str(path), str(IN2)], ROOT / arm
        try:
            p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=120)
            return p.returncode, p.stdout + p.stderr
        except (OSError, subprocess.TimeoutExpired) as exc:
            return None, "check could not run: %s" % exc


def planted(arm, mode, must_say):
    """The check must accept T2 as produced, then reject the planted fault and name it."""
    parts = {}
    for n, t in enumerate(both(arm, "T2"), 1):
        code, _ = run_check(arm, t or "")
        parts["T2 r%d: the check accepts the output as produced" % n] = bool(t) and code == 0
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "t2.txt", Path(d) / "mutated.txt"
            src.write_text(t or "", encoding="utf-8")
            p = subprocess.run([sys.executable, str(ROOT / "harness" / "mutate.py"), mode, str(src), str(dst)],
                               capture_output=True, text=True)
            if p.returncode != 0:
                parts["T2 r%d: the fault could be planted" % n] = False
                continue
            code, said = run_check(arm, dst.read_text(encoding="utf-8"))
        lines = said.split("\n")
        named = all(any(word in ln and tid in ln for ln in lines) for word, tid in must_say)
        parts["T2 r%d: the check rejects the fault, printing %s" % (
            n, " and ".join("`%s ... %s`" % w for w in must_say))] = code not in (0, None) and named
    return parts


def q4(arm):
    return planted(arm, "delete", [("MISSING", "MD-DARK-011")])


def q5(arm):
    return planted(arm, "swap", [("DUPLICATE", "MD-DARK-011"), ("MISSING", "MD-DARK-014")])


def _stop_value(text, label):
    """A stop field's value: the rest of its line and any indented lines under it."""
    m = re.search(r"(?m)^[\s|`*>-]*%s\b[:\s|`*]*(.*(?:\n[ \t]+\S.*)*)" % re.escape(label), text)
    return m.group(1) if m else None


def q6(arm):
    parts = {"reference/ defines the six stop fields in order, each with a rule, and names the "
             "two-build condition": stop_definition(arm) is not None}
    for n, t in enumerate(both(arm, "T3"), 1):
        t = t or ""
        lines = t.split("\n")
        idx, in_order = 0, bool(t)
        for label in STOP_LABELS:
            while idx < len(lines) and not _starts(lines[idx], label):
                idx += 1
            in_order = in_order and idx < len(lines)
            idx += 1
        condition = _stop_value(t, "Condition") or ""
        detail = _stop_value(t, "Detail") or ""
        remedy = _stop_value(t, "Remedy") or ""
        parts["T3 r%d: the six stop fields in order, and no records" % n] = in_order and not parse_records(t)
        parts["T3 r%d: Condition names more than one build; Detail names b41c07e and c98f215" % n] = (
            TWO_BUILDS in condition and "b41c07e" in detail and "c98f215" in detail)
        parts["T3 r%d: rows_in 18, records_out 0" % n] = (
            coverage_number(t, "rows_in") == 18 and coverage_number(t, "records_out") == 0)
        parts["T3 r%d: the Remedy assigns no row to a build (names neither build)" % n] = (
            bool(remedy.strip()) and "b41c07e" not in remedy and "c98f215" not in remedy)
    for n, t in enumerate(both(arm, "Q6"), 1):
        parts["Q6 r%d: the answer cites the reference/ definition" % n] = cited_region(
            arm, answer_line(t or ""), ["RUN STOPPED"])
    return parts


def q7(arm):
    def comparable(t):
        recs, order = records_by_id(t)
        if order != IDS2 or not all(complete(r) for r in recs):
            return None
        return [{k: v for k, v in r.items() if k != "intake_id"} for r in recs]
    clean = [comparable(t) for t in both(arm, "T2")]
    parts = {}
    for n, t in enumerate(both(arm, "T2-noisy"), 1):
        noisy = comparable(t)
        parts["T2-noisy r%d: nine complete records, identical to T2 r%d apart from intake_id" % (n, n)] = (
            noisy is not None and noisy == clean[n - 1])
    return parts


def q8(arm):
    return {"Q8 r%d: answers NO" % n: (answer_line(t or "") or "").upper() == "NO"
            for n, t in enumerate(both(arm, "Q8"), 1)}


def variation(arm):
    """Not scored. How far the two clean T2 runs differ, so a Q7 difference can be read against it."""
    a, b = (parse_records(t or "") for t in both(arm, "T2"))
    diffs = []
    for ra, rb in zip(a, b):
        for f in FIELDS[1:]:
            if ra.get(f) != rb.get(f):
                diffs.append("%s %s" % (ra.get("test_id", "?"), f))
    if len(a) != len(b):
        diffs.append("record count %d vs %d" % (len(a), len(b)))
    return diffs


QUESTIONS = [("Q1", q1), ("Q2", q2), ("Q3", q3), ("Q4", q4), ("Q5", q5), ("Q6", q6), ("Q7", q7), ("Q8", q8)]


def main(argv):
    if len(argv) != 1 or argv[0] not in ("original", "rebuild"):
        print(__doc__)
        return 64
    arm = argv[0]
    scores = {}
    for q, fn in QUESTIONS:
        parts = fn(arm)
        mark = 1 if parts and all(parts.values()) else 0
        scores[q] = {"mark": mark, "parts": parts}
        print("%s  %d" % (q, mark))
        for k, v in parts.items():
            print("     %s  %s" % ("yes" if v else "NO ", k))
    scores["T2 run-to-run variation (not scored)"] = variation(arm)
    print("T2 r1 vs r2, fields that differ (not scored): %s" % (", ".join(scores["T2 run-to-run variation (not scored)"]) or "none"))
    out = ROOT / ("run-" + arm) / "scores.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
