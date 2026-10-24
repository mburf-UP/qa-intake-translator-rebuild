The stop output is defined in `reference/output-schema.md`, §6.1 "The stop output".

- **Line 188** says a stopped run prints "these six lines, in this order, and nothing else", with no records and no coverage block.
- **Lines 192–197** give the six lines in order:
  1. `RUN STOPPED — no records produced.`
  2. `Condition:`
  3. `Detail:`
  4. `Remedy:`
  5. `rows_in`
  6. `records_out`, which is always `0`.
- **Lines 203–212** show the exact layout in a code block.

Line 184 only says a stopped run is "the schema refusing to produce something untrue". It does not define any fields.

ANSWER: reference/output-schema.md:188