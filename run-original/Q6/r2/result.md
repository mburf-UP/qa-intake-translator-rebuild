`reference/` doesn't define the exact fields of the stop output or their order.

- `reference/output-schema.md:161-163` (§6, "What stops a run") says a stopped run "produces **no records at all**, and says which of these fired."
- The table at `reference/output-schema.md:165-169` lists three stop conditions: no build identifier, rows from more than one build, and columns that don't match §2. It gives no field list or ordering for the stop message.
- `reference/output-schema.md:171` says only that a stopped run is not an error to work around.
- `reference/field-definitions.md:47` and `reference/output-schema.md:46` say that a missing build identifier produces no records. Neither describes the stop output's shape.

A stop message is shown in `examples.md:155` ("RUN STOPPED — no records produced."). That file is outside `reference/`, so I didn't count it. `rules.md:124` also says the stop prints which condition fired and why, and that's outside `reference/` too.

ANSWER: NONE