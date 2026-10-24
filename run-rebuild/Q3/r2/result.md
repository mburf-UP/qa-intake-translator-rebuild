When neither the Evidence cell nor the Actual Result names any evidence, `evidence_cited` must be `NOT IN SOURCE`.

- `reference/output-schema.md:104` says that when neither cell names any evidence, the field is empty and "is written `NOT IN SOURCE`". It adds that this is the only form allowed: never a note such as "none cited", never `none`, never blank.
- `reference/field-definitions.md:106` agrees: "When the list is empty, the field is `NOT IN SOURCE`" and nothing else.
- The worked examples match. `examples.md:118` and `examples.md:205` both show `evidence_cited NOT IN SOURCE`.
- `examples.md:266` calls MD-SHELL-014's empty `evidence_cited` a "refusal". That wording is only in the examples file, and it conflicts with the reference files, which say to write `NOT IN SOURCE`. I went with the reference files.

ANSWER: NOT IN SOURCE | reference/output-schema.md:104