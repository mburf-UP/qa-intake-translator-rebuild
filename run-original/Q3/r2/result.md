`reference/` doesn't give one value for this case. It only says the field is a list that can be empty.

- `reference/field-definitions.md:106` says `evidence_cited` "Accepts — a list, possibly empty." It gives no literal token for the empty case.
- `reference/output-schema.md:85` and `:89-101` define the presence marks (`ON DISK`, `NOT FOUND`, `NOT CHECKED`). Each mark attaches to a reference that is named, so none of them applies when nothing is named.
- `reference/field-definitions.md:127-128` and `reference/output-schema.md:123+` define the refusal verdicts, which are values for fields with no usable source. They are not tied to `evidence_cited`, and `reference/` doesn't say that an empty list should become one of them.
- `examples.md:118` shows `(none cited)` for an empty case. That file is outside `reference/`, so it doesn't count. It also shows `NOT IN SOURCE` for `evidence_cited` at `examples.md:205`, so the examples are not consistent with each other.

ANSWER: NONE