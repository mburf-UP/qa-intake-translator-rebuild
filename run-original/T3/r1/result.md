**RUN STOPPED. No records produced.**

```
Condition:  Rows from more than one build in one input
            (reference/output-schema.md:169, rules.md:11)
Detail:     inputs/input-3-2026-08-28/session.md:8 gives the build identifier as two
            values, b41c07e and c98f215. It lists session log rows 18 and 19 (line 10).
            Line 17 says the 18 rows describe two different versions of the product
            "with nothing in the row saying which".
            cases.csv:1 has no build column, and no row carries a build identifier.
            No row can be assigned to either build.
Remedy:     Split the input by sitting and run twice (session.md:28-29,
            output-schema.md:169). That needs to know which sitting each row belongs to.
            Neither the folder nor the input establishes that.
rows_in     18   (cases.csv:2-34 holds 18 data rows, worksheet rows 184-203 with 195 and 198 absent)
records_out 0
```

**Why this is the correct output**
- `rules.md:11` (step 3) says to confirm every row carries the same build, and to stop if not.
- `rules.md:124` says a stopped run is a result, and that the check is not to be disabled and the run retried.
- `rules.md:126` and `output-schema.md:167` give the reason: a record that can't name its build isn't evidence.
- `field-definitions.md:47` says `build` can't be refused, inferred or left empty. Without a single build, no record can be written.

**What I checked before stopping**
- The `cases.csv` header (line 1) names all ten required columns plus `_source_row`. The column check in `output-schema.md:57` passes, so it isn't what stopped the run.
- Some cells hint at a retest. For example, `cases.csv:12` says "retested after uploading initial test results and something has changed", and `cases.csv:15` says "just a couple of hours ago". None of them name a build, and the rules don't allow me to infer one from prose or dates (`output-schema.md:47`, `rules.md:95`). So I did not use them to assign rows to either build.

**What the folder can't establish**
- Which of the 18 rows belong to the `b41c07e` sitting and which to `c98f215`. `session.md:29` says this is the operator's job.

If you tell me which rows belong to which sitting, I can run each group separately. That would be your assignment, not something the folder establishes. I'd cite it as your input.