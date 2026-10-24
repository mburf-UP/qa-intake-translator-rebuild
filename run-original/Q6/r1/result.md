`reference/` doesn't define the exact fields of the stop output or their order.

- `reference/output-schema.md:161-171` (§6, "What stops a run") covers stopping. Line 163 says the run "produces **no records at all**, and says which of these fired." The table at lines 165-169 lists three stop conditions: no build identifier, rows from more than one build in one input, and input columns that don't match §2.
- That section only requires the output to say which condition fired. It names no fields and gives no order for that output.
- `reference/field-definitions.md:47` also says a run with no build identifier produces no records. It doesn't describe the stop output either.
- A search of `reference/` for "halt", "stopped", "fired" and "reason" found nothing else that defines stop-output fields.

I only read `reference/`, as the question asks. I didn't check `rules.md`, `examples.md` or the other files in the folder.

ANSWER: NONE