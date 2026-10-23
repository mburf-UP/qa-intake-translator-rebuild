# Rules — how the translation is made

The **shape** of the output is in `reference/output-schema.md`. That file is the contract and this one never restates it. This file is the procedure: the order of work, how each value is taken, and what must never be added.

---

## 1. Order of work

1. Read `reference/output-schema.md`. Confirm the input's columns match §2 — **by position** if the input is the worksheet, **by header name** if it is a CSV export (§2.1). **If they do not, stop** — §6.
2. Confirm a build identifier was supplied. **If it was not, stop** — §6.
3. Confirm every row in the input carries the same build. **If not, stop** — §6.
4. Count `rows_in` and `rows_recorded` **before** producing any record. The counts come from the input, never from the output.
5. Produce one record per recorded row, in input row order.
6. Produce the coverage block.
7. Check `records_out == rows_recorded`. **If they differ, the run failed** — say so, do not publish a partial result.

Step 4 before step 5 is deliberate. A count taken from the output can only ever agree with the output.

---

## 2. How a value is taken

**Every value is copied. Nothing is composed.** Open the cell, take what is there, put it in the field.

**Four things in a record are not copies of a cell, and none of them adds content.** `intake_id` is a label this run assigns. `build` is copied, but from the session log rather than the worksheet. `evidence_cited` extracts references already written in two cells. `observation_spans` indexes lines without reading them out, and `substantive_pass_rows` sorts rows by the rule in `reference/output-schema.md` §5. **Everything else is a copy**, and these are named here so that "copying" is not read as covering work it does not cover.

| Situation | Do this |
|---|---|
| The cell has a value | Copy it, character for character |
| The cell is empty | `NOT IN SOURCE` |
| The cell has a value this field cannot accept | `IN SOURCE, UNRESOLVABLE`, **quoting the raw text** |
| A numbered rule below puts the field out of scope | `NOT APPLICABLE`, naming the rule |

### 2.1 Copying means copying

- **Spelling is not corrected.** `fail` stays `fail`. It is not `Fail`.
- **Case is not standardised.** Not in status values, not in test IDs, not in names.
- **Dates are not reformatted.** `28/08` does not become `2026-08-28`.
- **Numbers are not normalised.** `40k` does not become `40,000`. `3.1:1` does not become `3.1`.
- **Prose is not tidied.** Typos, sentence fragments, mid-thought corrections and the tester's own asides are part of the observation. The longest cell in the reference workbook is a stream of consciousness naming three screenshots, and every word of it is evidence.
- **Nothing is trimmed for length.** `observed` is the whole cell.

The engagement's own guidance to its tester is *"keep writing what you saw, including the parts that seem beside the point"*, on the record because eleven apparently irrelevant words once corrected a test case and surfaced a pattern across three phases. A translator that tidies is destroying the thing that guidance exists to protect.

### 2.2 The same value written two ways

If one cell gives two values for the same field — two dates, two figures, an account spelled two ways — the field is `IN SOURCE, UNRESOLVABLE` and **both are quoted**.

**The translator does not choose between them.** Choosing is a judgement and this is not a judging tool. A conflict surfaced is useful; a conflict silently resolved is a fabricated fact with a plausible face.

### 2.3 Relative and anchored references

A date field accepts a date. It does not accept a reference that needs an outside fact to resolve:

| In the cell | Field value |
|---|---|
| `28 Aug` | `28 Aug` |
| `retest next Tuesday` | `IN SOURCE, UNRESOLVABLE` — *"retest next Tuesday"* |
| `same as above` | `IN SOURCE, UNRESOLVABLE` — *"same as above"* |
| *(empty)* | `NOT IN SOURCE` |

**"Next Tuesday" resolved to a calendar date is the single most likely way this translator fails.** It will not feel like invention at the moment it happens. It is the brief's first named example of a disqualifying fact.

---

## 3. Evidence references

Collect references from the `Evidence` column **and from the `Actual Result` prose**, because the tester routinely names screenshots inline while describing what they saw.

- A reference is any token matching an evidence filename pattern, with or without its extension.
- Mark each `ON DISK`, `NOT FOUND` or `NOT CHECKED` per the schema.
- **Never upgrade `NOT CHECKED` to `ON DISK`.** If the evidence folder was not supplied to the run, every reference is `NOT CHECKED` and the coverage block says so.
- A reference named in the prose but absent from the `Evidence` column is still collected. It is not an error, and it is frequently the more interesting one.

**Do not open an evidence file.** Its presence is a fact about the filesystem. Its contents are an observation this translator did not make.

---

## 4. Splitting a cell into observation spans

A cell often holds several distinct observations. `observation_spans` indexes them so a downstream reader cannot act on the first and lose the rest.

**A new span starts where the cell moves to a different subject** — a different screen, a different attempt, a different problem. In practice the tester's own paragraph breaks and numbered attempts mark them.

Three constraints:

1. **Spans are indices, not content.** A span says "lines 4 to 9", never what lines 4 to 9 mean.
2. **Spans cover the whole cell.** Every line belongs to exactly one span. If a line seems to belong to none, the span boundaries are wrong — widen one. **No line is ever outside every span.**
3. **When the boundaries are genuinely unclear, produce one span covering the cell.** Under-splitting loses nothing; over-splitting invents a distinction the tester did not draw.

---

## 5. What is never added

Nothing enters a record that did not come out of the input. In particular:

- **No cause.** Not "this is probably the caching layer", not "looks like the same root as the earlier one".
- **No code reference.** The translator does not open the product's source.
- **No proposed fix**, in any form — not a recommendation, not a "the smallest change would be", not a fix embedded in a description of the problem.
- **No severity the tester did not write.** Severity in this engagement is set by the analyst from evidence. A blank severity is `NOT IN SOURCE` and stays that way.
- **No priority, risk tier or impact.**
- **No summary of the run**, beyond the arithmetic in the coverage block.
- **No sentiment, tone or confidence.**

**There is nowhere in the schema for any of these**, which is the real guarantee. This section exists so that a reader knows the omission was chosen, not overlooked.

### 5.1 The disguised versions

The request will not usually arrive as "add a recommendation". It arrives as:

- *"Can you also flag which ones look most urgent?"* — that is severity.
- *"Group the similar ones together."* — that is a cause hypothesis wearing a layout.
- *"Just give me the ones that matter."* — that is the filter at intake that left thirty open findings out of every packet, eleven of them rated major.
- *"Tidy up the wording so it reads well for the developer."* — that is §2.1, and it is where invention enters most easily.

Each is refused by pointing at the schema, not by arguing.

---

## 6. When the run stops

The stop conditions are in the schema §6. Two things about them:

**A stopped run is a result.** It prints which condition fired and why, and it produces no records. It is not a failure to be retried with the check disabled.

**The build rule is not this translator's invention.** The engagement's method states that results from two different builds cannot be compared. A record that cannot name its build is not evidence of anything, and producing one would be the most expensive kind of invention: a true observation attached to the wrong world.

---

## 7. What this translator is not

It is not the analyst. The analysis step that follows — cause, code reference, proposed resolution, downstream impact, risk tier, severity — is the most valuable work in the engagement and **none of it is a translation.**

Separating the two is the entire point. When observation and analysis are produced in one pass, the analysis contaminates the observation: in this engagement that has already produced a test case written to chase a discrepancy that did not exist, a finding rewritten twice in one evening because it was drafted against a moving target, and a run order that told a first-view tester what the code said they should see.

This folder produces the record of what was seen. Someone else works out what it means.
