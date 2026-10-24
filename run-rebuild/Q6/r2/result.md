The stop output is defined in `reference/output-schema.md`, in §6.1 "The stop output", which starts at line 186.

- **Fields and order:** The table at `reference/output-schema.md:190-197` lists the six lines in order. They are the fixed first line `RUN STOPPED — no records produced.` (line 192), then `Condition:` (193), `Detail:` (194), `Remedy:` (195), `rows_in` (196) and `records_out` (197).
- **Order and exclusions:** Line 188 says the six lines print "in this order, and nothing else", with no records and no coverage block.
- **Layout:** The exact layout block is at lines 203-212. `records_out` is always `0`.
- **Which conditions stop a run:** §6 (lines 176-182) lists them. They are no build identifier, rows from more than one build, and columns that don't match §2.

`rules.md:122-124` only points back to schema §6.1 and does not define the fields itself. That file is outside `reference/`.

ANSWER: reference/output-schema.md:188