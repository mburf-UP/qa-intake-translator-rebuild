RUN STOPPED — no records produced.

**Condition:** Rows from more than one build in one input (`reference/output-schema.md:168`, §6; `rules.md:9-11`, §1 step 3).

**Detail:**
- `inputs/input-3-2026-08-28/session.md:8` gives the build identifier as "two: `b41c07e` and `c98f215`".
- `session.md:10` says the session log has two rows, 18 and 19. `session.md:17-19` says a new build landed mid-day and the same range was re-run.
- `cases.csv:1` has no build column. Its header is Test ID, Expected Result, Actual Result, Status, Severity, Defect ID, Evidence, Tester, Date Tested, Notes, `_source_row`. No row says which sitting it belongs to.
- Several rows do describe a change partway through. For example, `cases.csv:10` says "something has changed since earlier testing", and `cases.csv:15` says "just a couple of hours ago". I did not use those remarks to assign rows to builds, because assigning a build is an inference. `rules.md:95` forbids adding anything the input does not state, and `session.md:28-30` says the missing fact is the operator's to supply.

**Remedy:** Split the input by sitting and run twice (`output-schema.md:168`). Nothing in this folder says which sitting each row belongs to (`session.md:28-30`). If you tell me which rows belong to which build, I can translate each part.

**Counts:** `rows_in` is 18 and `records_out` is 0.
- 18 data rows are in `cases.csv` lines 2-34 (`_source_row` 184-203). `session.md:13` also says 18.
- Some `_source_row` values are missing (195 and 198). I'm only reporting the gap and haven't speculated about it.
- No coverage block or records are printed, because `output-schema.md:163` says a stopped run produces no records.

This is the intended result for this input (`examples.md:150-179`, `inputs/README.md:21-33`). Producing 18 records would have meant guessing the build. `rules.md:124` says a stopped run isn't to be retried with the check disabled.