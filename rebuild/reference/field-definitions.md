# Field definitions

`output-schema.md` is the contract: it says which cell each field comes from and in what order the fields appear. **This file never restates it.**

This file answers a different question, one per field: **what would make a value in this field wrong?**

It exists because "verbatim from column 12" tells a reader where to look but not what to check. A field can be filled from exactly the right cell and still be wrong — a date reformatted, a refusal used in place of a value, a list collapsed to a count. Those are the failures a reader can catch, and this is where they are named.

**Version 1.0 · 2026-09-26.** Tracks schema version 1.0.

---

## How to read an entry

| Line | Means |
|---|---|
| **Is** | What the field is for, in one sentence |
| **Accepts** | What a valid value looks like |
| **Wrong if** | The failures that are specific to this field |

Three rules apply to every field and are not repeated in each entry:

- **A refusal is always one of the three §4 verdicts, spelled exactly.** `N/A`, `-`, `unknown`, `(blank)` and an empty string are not refusals. They are either a transcribed value or a defect.
- **No field is ever omitted.** A record with thirteen fields is a failed record, not a short one.
- **A transcribed value is never altered.** Every entry below assumes this; where a field is especially exposed to it, the entry says so.

---

## The fields

### 1. `intake_id`

**Is** — a label for this record within this run, so a reader can refer to one record without quoting it.
**Accepts** — `INTAKE-<run date>-<ordinal>`, ordinal from 001, assigned in input row order.
**Wrong if** — the ordinals are not contiguous from 001 (a record was dropped or the order was changed); two records share one; or the ordinal is treated as content. **It is a label. It carries no meaning and no ranking**, and a reader who sorts by it gets input row order back, which is the only order there is.

### 2. `test_id`

**Is** — the worksheet's own key for the row, and the only way back to the source.
**Accepts** — the cell, verbatim, including case and any prefix.
**Wrong if** — it is normalised, zero-padded, re-cased, or reconstructed from a pattern in the other IDs. A `test_id` that does not match the worksheet is worse than a missing one, because it resolves to the wrong row instead of to nothing.

### 3. `build`

**Is** — which version of the product the observation describes.
**Accepts** — the identifier supplied with the session, verbatim. Identical across every record in one run.
**Wrong if** — it differs between records in a run (the run should have stopped — see schema §6); it is inferred from a date; or it is filled with a refusal. **`build` cannot be refused.** If there is no build identifier, the run produces no records at all. A record with `build: NOT IN SOURCE` is a contradiction: it claims to be an observation about nothing in particular.

### 4. `date_tested`

**Is** — the date the tester wrote in the cell.
**Accepts** — whatever is written, in whatever form: `28/08`, `28 Aug`, `2026-08-28`, `Thursday`.
**Wrong if** — it is reformatted to a standard, given a year the cell does not have, or resolved from a relative reference. **This field is the brief's own named example of a disqualifying invention.** `retest next Tuesday` is `IN SOURCE, UNRESOLVABLE`, quoting those words. Resolving it requires a calendar, and a calendar is an outside fact.

### 5. `tester`

**Is** — who recorded the row.
**Accepts** — the cell, verbatim, in whatever form the engagement uses: initials, a role label, a name, a handle.
**Wrong if** — it is expanded, normalised across rows, or filled from the session rather than the cell. If four rows spell the same person three ways, the field carries three spellings across those rows. **The brief's named trap is "a name spelled the way it usually is instead of the way it appeared."**

### 6. `recorded_status`

**Is** — the verdict the tester recorded at the time.
**Accepts** — the cell, verbatim, as spelled. `fail` is not `Fail`.
**Wrong if** — the case is standardised, the value is mapped to a controlled vocabulary, or it is reconciled against any other record of the same row's status.

**This field is known to be stale on some rows and is copied anyway.** In the reference engagement the worksheet's status column was found to have drifted 19 rows out of step with the defect register, in both directions — five it called open were closed, four it called closed were open. **Correcting it here would be the right value in the wrong place.** `recorded_status` is a fact about what the cell says, not a claim about the world; the reconciliation belongs to whoever owns the register. Where a run can see both, the disagreements are reported as their own section rather than resolved silently.

### 7. `recorded_severity`

**Is** — a severity **only if the tester wrote one**.
**Accepts** — the cell verbatim, or `NOT IN SOURCE`.
**Wrong if** — it holds any value not in the cell. In the reference workbook this field is blank or `N/A` on 241 of 296 recorded rows, and that is correct rather than a gap: severity in this engagement is set by the analyst from evidence. **A high refusal count here is the field working.** A run in which this field is usually filled is a run in which something is inventing severities.

Note the boundary: a cell containing the literal text `N/A` is a **transcribed value** — the tester wrote it. An empty cell is `NOT IN SOURCE`. The two look alike in a report and are different claims.

### 8. `recorded_defect_id`

**Is** — a defect identifier the tester wrote in the cell.
**Accepts** — the cell verbatim, or a refusal.
**Wrong if** — an ID is matched from elsewhere, allocated, or inferred from a defect described in the prose. **A row can describe a defect in detail and carry no defect ID, and that is a complete record**, not an incomplete one. Filling it is the most plausible-looking invention in the schema.

### 9. `expected_result`

**Is** — the generator-owned statement of what should have happened, carried because an observation is unreadable without it.
**Accepts** — the cell, verbatim.
**Wrong if** — it is compared to `observed`, or trimmed to the part that seems relevant. **Comparing them is the analyst's job.** This field's only purpose is to spare a reader from opening the worksheet; it is context, not an assertion about the row.

### 10. `observed`

**Is** — the tester's own account of what they saw. **This is the payload of the record.**
**Accepts** — the whole cell, verbatim, whatever its length. In the reference workbook these run from 3 to 4,995 characters, median 189.
**Wrong if** — it is summarised, trimmed, tidied, spell-checked, re-punctuated, truncated with an ellipsis, or split across fields. Typos, fragments, mid-thought corrections and the tester's asides stay in.

**Every one of those edits is defensible in isolation and each one destroys evidence.** The engagement's guidance to its tester is to write down the parts that seem beside the point, because eleven apparently irrelevant words once corrected a test case. A translator that tidies is destroying the thing that guidance exists to protect.

### 11. `tester_notes`

**Is** — whatever is in the notes cell, which is frequently unrelated to the observation.
**Accepts** — the cell verbatim, or a refusal.
**Wrong if** — it is merged into `observed`, or dropped because it looks like housekeeping. The two cells are different columns and stay different fields. A note reading *"machine restarted between cases"* is not commentary; it is the reason two rows disagree.

### 12. `evidence_cited`

**Is** — every evidence reference named in the row, from **both** the evidence cell and the observation prose, each carrying one presence mark.
**Accepts** — a list. Each entry is the reference as written, plus `ON DISK`, `NOT FOUND` or `NOT CHECKED`. **When the list is empty, the field is `NOT IN SOURCE`** (`output-schema.md` §3.1) and nothing else.
**Wrong if** —

- a reference named only in the prose is missed. The tester routinely names screenshots inline while describing what they saw, and **that reference is frequently the more interesting one**;
- `NOT CHECKED` is written as `ON DISK`. *Not looked for* and *found* are different claims, and the first must never quietly become the second when the evidence folder was simply not supplied;
- a filename is corrected to the one that exists. A near-miss is `NOT FOUND`. Repairing it here hides a broken citation that a reader needs to see;
- the file was opened. **Presence is a fact about the filesystem. Contents are an observation this translator did not make.**

### 13. `observation_spans`

**Is** — an index of the distinct observations inside `observed`, so a downstream reader cannot act on the first one and lose the rest.
**Accepts** — one or more line ranges.
**Wrong if** —

- a span carries content. **Spans are indices.** A span says *lines 4 to 9*; it never says what lines 4 to 9 mean, and a span with a label attached is a summary wearing a number;
- any line of `observed` falls outside every span. Full coverage is the property that makes this field worth having;
- spans overlap, or a boundary is drawn where the subject did not change. **When the boundaries are genuinely unclear, one span covering the cell is the correct answer.** Under-splitting loses nothing; over-splitting invents a distinction the tester did not draw.

### 14. `source`

**Is** — sheet name (`reference/output-schema.md` §2.2), row number and column letter for every value **taken from the worksheet**, so any such field can be opened and checked there. Two fields have no worksheet cell and say so instead: `intake_id` is a label this run assigned, and `build` carries the session log entry it came from. When the input is a CSV export rather than the worksheet, the row number is `_source_row` and can be checked against the shipped file; the sheet name and column letters refer to the worksheet the export was taken from, and a reader holding only the export cannot check those two.
**Accepts** — one locator per field, including for fields carrying a refusal.
**Wrong if** — a refusal has no locator. **`NOT IN SOURCE` still names the cell that was empty** — otherwise a reader cannot tell a checked empty cell from a field nobody looked at. This field is what makes the rest of the record checkable rather than claimed.

---

## The coverage block

The coverage block is one per run, not per record. Its composition is in schema §5. Two definitions carry weight and belong here:

**`substantive_pass_rows`** — rows whose status is `Pass` and whose `Actual Result` is more than a bare confirmation. The working threshold is more than 40 characters, which in the reference workbook selects 129 of 296 recorded rows.

*Wrong if collapsed to a number.* Three findings that outranked most of the failures came out of `Pass` rows. **A count cannot be acted on; a list can.** The engagement's own generated backlog states the same rule independently, and it was written by a second party for a different purpose: *"Do not collapse this into a count. If you summarise, carry §1 and §2 as lists, with their IDs."*

**`rows_not_recorded`** — rows with an empty `Actual Result`. Listed by Test ID, never only counted, for the same reason: a reader who wants to know which cases were never run needs the IDs, and a number tells them only that they should go and look.

**`records_out` must equal `rows_recorded`.** That equality is the whole guarantee. It is arithmetic, it is checkable by a stranger with the worksheet open, and if it does not hold the run failed and publishes nothing.
