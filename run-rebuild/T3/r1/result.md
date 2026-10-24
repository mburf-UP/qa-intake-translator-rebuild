```
RUN STOPPED — no records produced.

Condition:  Rows from more than one build in one input
Detail:     inputs/input-3-2026-08-28/session.md:8 names two build identifiers, b41c07e and c98f215.
            inputs/input-3-2026-08-28/session.md:10 gives the session log rows as 18, 19. Lines 17-19 say two sittings, two builds, one worksheet row per test case.
            inputs/input-3-2026-08-28/cases.csv:1 has a header with no build column. The 18 rows (_source_row 184-203) carry no per-row build, so no row can be assigned to either build.
Remedy:     Split the input by sitting and run each part separately. This needs to know which sitting each row belongs to, and nothing in this input says.
rows_in     18
records_out 0
```