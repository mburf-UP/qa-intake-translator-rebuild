```
RUN STOPPED — no records produced.

Condition:  Rows from more than one build in one input
Detail:     inputs/input-3-2026-08-28/session.md line 8 records two build identifiers, b41c07e and c98f215.
            inputs/input-3-2026-08-28/session.md line 10 lists two session log rows, 18 and 19.
            inputs/input-3-2026-08-28/session.md lines 17-19 say the same test range was re-run on a new build, and that no row says which sitting it belongs to.
            inputs/input-3-2026-08-28/cases.csv line 1 has no build column, so no row can be assigned to either build.
Remedy:     Split the input by sitting and run each part separately. This needs a fact the input does not give: which sitting each row belongs to.
rows_in     18
records_out 0
```

Where each point comes from:
- **Why it stops:** `rules.md:11` (step 3) says to stop when the rows do not all carry the same build. `reference/output-schema.md:181` lists "Rows from more than one build in one input" as a stop condition.
- **Output layout:** `reference/output-schema.md:188-212` fixes the six-line stop output and the code block.
- **Other stop checks:** The CSV header at `cases.csv:1` names all ten required columns, so the column check (`output-schema.md:57`) is not the cause. A build identifier was supplied, so the missing-build condition is not the cause either.
- **Row count:** `cases.csv` has 18 data rows, at lines 2–34 (some rows span several lines). Their `_source_row` values are 184–194, 196, 197 and 199–203. `session.md:13` also says 18.
- **Which sitting each row belongs to:** Neither the CSV nor the folder establishes this.