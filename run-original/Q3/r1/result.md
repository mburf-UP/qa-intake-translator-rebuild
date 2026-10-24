`reference/` doesn't give one literal value for this case. It only says the field takes a list that can be empty.

- `reference/field-definitions.md:106` says `evidence_cited` "Accepts — a list, possibly empty. Each entry is the reference as written, plus `ON DISK`, `NOT FOUND` or `NOT CHECKED`."
- `reference/output-schema.md:85` and `:91-99` say the field collects references from both the Evidence cell and the Actual Result prose, and each reference gets one presence mark. They don't say what to write when neither cell names any evidence.
- The refusal verdicts in `reference/output-schema.md` §4 (starting at line 123) are for fields with no usable source. I only read the table's first row, `NOT IN SOURCE`, so I can't say whether it or another verdict is meant to apply here. A list field that is simply empty isn't clearly covered.
- `examples.md:118` shows `(none cited)` for an empty column P, and `examples.md:205` shows `NOT IN SOURCE`. Those two examples disagree, and they are outside `reference/`, so I didn't treat either as the rule.

ANSWER: NONE