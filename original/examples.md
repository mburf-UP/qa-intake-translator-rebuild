# Examples — the contract holding

Three worked examples, all from the inputs in this repository, all reproducible by opening the named
file at the named row.

1. **A dense row** — many observations, evidence in two places, a value the translator must not fix.
2. **A sparse row that contradicts itself** — and the translator copies both halves.
3. **A whole input that produces nothing** — the stop condition, on a real day.

Then one full coverage block, for the smallest input, with every figure listed rather than counted.

**Every value below is quoted from the shipped CSVs.** Where this file says a cell is empty, it is
empty in the file.

---

## Example 1 — a dense row

**Source:** `inputs/input-2-2026-09-18/cases.csv`, `MD-SHELL-012`, worksheet row 94.
**Build:** `a17e3d0`, from `inputs/input-2-2026-09-18/session.md`.

The `Actual Result` cell runs 1,684 characters across three dated visits to the same test case. It
names five of the six screenshots this row cites, asks the reader two questions, and says partway through
that it is upgrading the severity.

```
intake_id            INTAKE-2026-09-26-002
test_id              MD-SHELL-012
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Fail
recorded_severity    S2 Major
recorded_defect_id   OBS-201, OBS-213, OBS-214, OBS-215, OBS-216
expected_result      <col K verbatim>
observed             <col L verbatim, all 1,684 characters, beginning
                      "I did as many searches as I could - 48 searches - but never hit a cap.">
tester_notes         NOT IN SOURCE                        (col S is empty)
evidence_cited       MD-SHELL-012-searches-no-limit         NOT CHECKED
                     MD-SHELL-012-Request-Count-18Sep       NOT CHECKED
                     MD-SHELL-012-some-docs-missing-20Sep   NOT CHECKED
                     MD-SHELL-012-repeated-selections-20Sep NOT CHECKED
                     MD-SHELL-012-docs-actions-20Sep        NOT CHECKED
                     MD-SHELL-012-resend-limit-20Sep        NOT CHECKED
observation_spans    line 1
                     line 2
                     line 3
                     line 4
                     line 5
                     line 6
source               Test Cases!A94, K94, L94, M94, N94, O94, P94, Q94, R94, S94
```

**What those six spans cover, and why the record above does not say so.** Line 1 is the first run, 48
searches with no cap; line 2 the 14/9 retest at 116 searches; line 3 the 20/9 retest and the “some
results may be missing” string; line 4 the Documents and Actions split, working; line 5 the free
account returning restricted links; line 6 Part B and the 429 string. **That paragraph is this page
talking to you, and it is deliberately not in the output.** `rules.md` §4 constraint 1: a span is an
index, and a span with a label attached is a summary wearing a number. The line numbers are the record;
the gloss is a convenience that a downstream reader can discard without losing anything.

**Three things this row shows.**

**The severity is `S2 Major` and the prose explains why it was raised** — *"upgrading severity on this
as it’s a bad user experience"*. The translator copies the cell. It does not agree, check or re-derive
it, and if the prose had argued for `S1` the field would still read `S2 Major`, because the field is a
record of what the cell says.

**`recorded_status` is `Fail`, and the prose says something different.** *"Unless you can make sense of
what is required here and what is a Pass vs a Fail I will mark this as a Pass."* The cell says `Fail`.
Both are transcribed, neither is reconciled, and a reader can see the disagreement — which is the point.
Resolving it requires knowing which of the three visits the status belongs to, and that fact is not in
the input.

**`evidence_cited` is `NOT CHECKED`, six times, and one of the six is only in the `Evidence`
column.** Five are named in the prose as well; `MD-SHELL-012-Request-Count-18Sep` is not, which is why
field 12 reads both columns and not just one. The evidence folder holds real screenshots of a live
commercial product and is not in this repository, so no file could be looked for. **`NOT CHECKED` is not
`NOT FOUND` and it is certainly not `ON DISK`** — the translator did not look, and says so, rather than
reporting an absence it never established.

---

## Example 2 — a sparse row that contradicts itself

**Source:** `inputs/input-2-2026-09-18/cases.csv`, `MD-SHELL-014`, worksheet row 96.
**Build:** `a17e3d0`.

This is the most instructive row in the repository. It is a `Pass` whose prose says *"Marking as
Partial"*, it carries a severity it should not need, and two of its cells are empty.

The whole of `Actual Result`. Line 1 ends with **two trailing spaces**, which a blockquote cannot
render, so they are written here as `␣␣` and are the only thing on this page that is not the
literal cell:

> Clicking on the user icon at the top right provides a "Help & support" option which when selected opens the "Support" page.␣␣
> At the bottom right of each page is an "Ask" button which enables questions to be asked and provides answers/guidance.
> There is nothing labelled "guide" or "guidance" though and nothing in the cookies with those words.
> Marking as Partial as the Test has failed but the functionality in the website seems correct

```
intake_id            INTAKE-2026-09-26-003
test_id              MD-SHELL-014
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Pass
recorded_severity    S3 Minor
recorded_defect_id   NOT IN SOURCE                        (col O is empty)
expected_result      the whole of col K. It opens: "PASS = you find NOTHING. No guide panel, no
                     guide switch, no "md-guide" cookie." and continues from there
observed             <the four lines above, verbatim — the two trailing spaces on line 1 are in the
                      field, and are shown above as ␣␣>
tester_notes         the whole of col S, 567 characters. It opens "QA note, 2026-09-18 (session 30):
                     the Pass is correct and the sentence above it is older than it." and closes
                     "Nothing of yours has been changed or re-graded." The field carries all of it;
                     only this page abbreviates
evidence_cited       (none cited)                         (col P is empty)
observation_spans    line 1
                     line 2
                     line 3
                     line 4
source               Test Cases!A96, K96, L96, M96, N96, O96, P96, Q96, R96, S96
```

**What the translator refused to do here, four times over.**

**It did not resolve `Pass` against "Marking as Partial".** A reader can see both and decide. A
summariser would have picked one, and whichever it picked would have been an invented fact — because
the `Notes` cell, written 34 days later by a different person, says the `Pass` is correct and the
sentence is stale. **The translator does not know that and does not need to.** It carries the status,
the prose and the note as three separate values, and the reconciliation belongs to whoever owns the
register.

**It did not merge `Notes` into `observed`.** They are different columns, written by different people,
weeks apart. Merging them would produce a single fluent account in one voice, and destroy the fact that
the correction came from outside.

**It did not drop the severity.** `S3 Minor` on a `Pass` row looks like a mistake. It is transcribed.

**It did not invent a defect ID.** The row describes behaviour at length and cites no defect. That is a
complete record, not a gap.

**This row is also why `substantive_pass_rows` exists.** It is marked `Pass`. Filtered on status — which
is what the process this replaces does at intake — it never enters the pipeline, and the four lines above
are never read by anyone downstream.

---

## Example 3 — the run that produces nothing

**Source:** `inputs/input-3-2026-08-28/` — 18 rows, and the translator emits **no records at all.**

```
RUN STOPPED — no records produced.

Condition:  Rows from more than one build in one input   (output-schema.md §6)
Detail:     inputs/input-3-2026-08-28/session.md records two sittings on 2026-08-28,
            session log rows 18 and 19, builds b41c07e and c98f215.
            The 18 rows in cases.csv carry no per-row build, so no row can be
            assigned to either one.
Remedy:     Split the input by sitting and run twice. That requires knowing which
            sitting each row belongs to, which is not in this input.
rows_in     18
records_out 0
```

**Why this input is in the repository.** It would have been easy to ship three inputs that all work.
This one is an ordinary Friday in a live engagement: a new build landed mid-day and the same test range
was re-run against it.

The tempting behaviour is to produce 18 records and pick one of the builds, or to leave `build` empty.
Both would be worse than stopping. **A true observation attached to the wrong build is the most
expensive kind of invention**, because nothing about it looks wrong — it is an accurate sentence about a
version of the product that never behaved that way. The engagement's own method states that results
from two builds cannot be compared, so the refusal is not this translator's invention; it is a rule it
inherited and made mechanical.

A stopped run is a result. It is not an error to retry with the check disabled.

---

## One record with nothing left out

The two examples above abbreviate their long fields so the point of each is visible. This one does not.
**Every field below carries its whole value**, so a reader can open `inputs/input-2-2026-09-18/cases.csv`
at `_source_row` 96 and compare the record against the row character for character. The only mark that
is not in the cell is `␣␣` for the two trailing spaces on line 1 of `observed`, which no page can render.

```
intake_id            INTAKE-2026-09-26-003
test_id              MD-SHELL-014
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Pass
recorded_severity    S3 Minor
recorded_defect_id   NOT IN SOURCE
expected_result      PASS = you find NOTHING. No guide panel, no guide switch, no "md-guide" cookie. If ANY of the three turns up, record Fail and screenshot it: it means an unfinished feature has leaked into production, which is the single most serious class of problem this phase hunts for.
observed             Clicking on the user icon at the top right provides a "Help & support" option which when selected opens the "Support" page.␣␣
                     At the bottom right of each page is an "Ask" button which enables questions to be asked and provides answers/guidance.
                     There is nothing labelled "guide" or "guidance" though and nothing in the cookies with those words.
                     Marking as Partial as the Test has failed but the functionality in the website seems correct
tester_notes         QA note, 2026-09-18 (session 30): the Pass is correct and the sentence above it is older than it. This case is deliberately back-to-front - it asks you to confirm something is ABSENT, so finding nothing IS the pass. You found no guide panel, no guide switch and no "md-guide" cookie, which is all three. The "Marking as Partial" line dates from 15 August, when the case read as though finding a help surface was a failure; Help & support and the Ask button are separate features and were never what this case hunts for. Nothing of yours has been changed or re-graded.
evidence_cited       NOT IN SOURCE
observation_spans    line 1
                     line 2
                     line 3
                     line 4
source               Test Cases!A96, K96, L96, M96, N96, O96, P96, Q96, R96, S96
                     intake_id assigned by this run; build from session.md
```

`expected_result` is 271 characters, `observed` 437 and `tester_notes` 567. Three of the fourteen fields are
refusals or assigned rather than copied cells, and each says which it is. **Nothing here is summarised,
and nothing is filled in from anywhere but the row and the session log.**

## A full coverage block

`inputs/input-2-2026-09-18/`, all nine rows, build `a17e3d0`. Every figure below was measured from the
shipped CSV.

```
build                    a17e3d0
rows_in                  9
rows_recorded            9
rows_not_recorded        0  (none — every row on this worksheet slice carries an Actual Result)
records_out              9          ✓ equals rows_recorded

substantive_pass_rows    3, listed:
                           MD-SHELL-014   Pass, 437 chars — the row in example 2
                           MD-DARK-011    Pass, 528 chars
                           MD-DARK-014    Pass, 419 chars

multi_observation_rows   all nine, listed by Test ID (46 spans across 9 rows):
                           MD-SIGN-014    2 spans
                           MD-SHELL-012   6 spans
                           MD-SHELL-014   4 spans
                           MD-SIGN-015    3 spans
                           MD-DARK-011    6 spans
                           MD-DARK-014    6 spans
                           MD-SEC-002     6 spans
                           MD-SEC-006     9 spans
                           MD-PERF-002    4 spans   (lines 1-5 are one observation
                                                     the tester wrapped across five lines)

evidence_not_found       none established — the evidence folder was not supplied to this run,
                         so all 32 references across the 9 rows are NOT CHECKED

refusal_counts           NOT IN SOURCE            17
                         IN SOURCE, UNRESOLVABLE   0
                         NOT APPLICABLE            0
```

**`records_out` equals `rows_recorded`.** That one line is the guarantee, and a reader with the CSV open
can check it in under a minute.

**Every recorded row in this input carries more than one observation, so the list is all nine and not a
subset.** That is not a quirk of the slice. A tester writing into a single cell over three visits to the
same case produces a stack of findings in one box, and the first draft of this example listed four rows
instead of nine — the field was right and the list was wrong, which is the failure the field exists to
catch happening to the example that describes it. **46 spans across 9 rows** is the number to check.

**Seventeen refusals across nine rows, and that is the system working.** Fifteen of them are an empty
`Severity` or an empty `Notes` cell; the other two are an empty `Defect ID`. Severity in this engagement is set by an analyst from evidence, not
by the tester, so a blank is the correct and expected state — **a run in which this field is usually
filled is a run in which something is inventing severities.**

**Zero `IN SOURCE, UNRESOLVABLE` in this input, and that is worth saying plainly** rather than quietly
omitting. Every date in these nine rows is a date. The verdict exists for cells reading *"retest next
Tuesday"*, and this particular slice of the worksheet does not contain one. A refusal type with a count
of zero is not decoration; it is the run reporting that it looked.

---

## One thing the larger input shows that this one does not

In `inputs/input-1-2026-09-20/`, one row cites evidence **in the prose that is not in the `Evidence`
column**: `MD-SEC-008` names `MD-SEC-008-sent-status` and `MD-SEC-008-link-landing`, and neither appears
in its own `Evidence` cell.

Two references, on one row, that a translator reading only the `Evidence` column would lose. This is
`rules.md` §3, and it is the reason that rule is not optional: **the tester names screenshots inline
while describing what they saw, and the inline one is frequently the more interesting.**
