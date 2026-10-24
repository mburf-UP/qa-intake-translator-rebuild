# Output schema — the observation intake record

**This file is the contract.** If the translator's output disagrees with this file, the output is wrong.
There is exactly one copy of this schema. Nothing else in this folder restates it. `check.py`, beside the README, checks an output against §5 and §6.1.

**Version 1.1 · 2026-10-24** (1.0, 2026-09-20, is the judged version in `original/`)

---

## 1. What one run produces

A run takes **one test session's recorded rows** and produces:

1. **One intake record per recorded row** — no filtering, no exceptions. See §3.
2. **One coverage block** for the run — See §5.

A row is *recorded* when its `Actual Result` cell is non-empty. Rows with an empty `Actual Result` are not recorded, are not given a record, and are counted in the coverage block.

**Records appear in input row order.** The order is not a ranking and must not be changed.

---

## 2. Where the input comes from

The input is the operator-owned block of a test-case worksheet. These column positions are fixed by the workbook's own generator configuration and are not this translator's to choose.

| Column | Field | Owned by |
|---:|---|---|
| 1 | Test ID | generator (the key) |
| 11 | Expected Result | generator |
| **12** | **Actual Result** | **tester** |
| **13** | **Status** | **tester** |
| **14** | **Severity** | **tester** |
| **15** | **Defect ID** | **tester** |
| **16** | **Evidence** | **tester** |
| **17** | **Tester** | **tester** |
| **18** | **Date Tested** | **tester** |
| **19** | **Notes** | **tester** |

Plus one value that is not in the worksheet and must be supplied with the session:

| Value | Where it comes from |
|---|---|
| **Build identifier** | The session log entry for the session being translated |

**Without a build identifier the run produces no records.** See §6.

### 2.1 Two forms of the same input, and how each is checked

The input arrives either as the worksheet itself or as a CSV export of the ten columns above. The
column check in `rules.md` §1 step 1 is satisfied differently in each, and the reason is the same one
in both: a value must never be taken from a place it was not written.

| Form | How the column check is satisfied |
|---|---|
| **The worksheet** | **By position.** The columns must sit at 1, 11 and 12–19 exactly as above |
| **A CSV export** | **By header name.** The first row must name all ten columns above, spelled exactly as above, and `_source_row` must carry the worksheet row number so every value still traces to a cell |

**A CSV export whose header is missing one of the ten columns, or renames one, stops the run** — for
the same reason a shifted worksheet column does.

**The inputs shipped in `inputs/` are CSV exports**: the ten named columns plus `_source_row`. The
worksheet itself belongs to a live commercial engagement and cannot travel, which is why the export
form exists and is part of the contract rather than a convenience.

### 2.2 The sheet name

**The sheet name for this workbook's CSV exports is `Test Cases`.** The reference workbook's test cases
are on the sheet named `Test Cases`, and the inputs in `inputs/` are exports of it, so their locators read
`Test Cases!A96, K96, ...`. The CSV cannot show this, because an export carries no sheet name; this line
is where it comes from. It applies to an input whose session record names no other workbook.

**If the session record names a different workbook, the sheet name is `NOT IN SOURCE`** unless that
record also states the sheet name. The locator then reads `NOT IN SOURCE!A96, K96, ...`: the row and the
columns are still known, the sheet is not, and no name is guessed.

---

## 3. The intake record

Every record has these fourteen fields, in this order, always. A field is never omitted. A field with no source carries a refusal from §4.

| # | Field | Source | Rule |
|---:|---|---|---|
| 1 | `intake_id` | assigned | `INTAKE-<run date>-<ordinal>`, ordinal in input row order from 001. A label, not content |
| 2 | `test_id` | col 1 | Verbatim |
| 3 | `build` | session log | Verbatim. Identical for every record in one run |
| 4 | `date_tested` | col 18 | Verbatim, **as written**. Never reformatted, never resolved |
| 5 | `tester` | col 17 | Verbatim |
| 6 | `recorded_status` | col 13 | Verbatim, **as spelled**. `fail` is not `Fail` |
| 7 | `recorded_severity` | col 14 | Verbatim, or a refusal |
| 8 | `recorded_defect_id` | col 15 | Verbatim, or a refusal |
| 9 | `expected_result` | col 11 | Verbatim. Carried as context because an observation is unreadable without it |
| 10 | `observed` | col 12 | **The whole cell, verbatim.** Never summarised, never trimmed, never tidied |
| 11 | `tester_notes` | col 19 | Verbatim, or a refusal |
| 12 | `evidence_cited` | cols 16 **and 12** | Every evidence reference named in either cell, each with a presence mark. See §3.1 |
| 13 | `observation_spans` | col 12 | Line index of each distinct observation inside `observed`. See §3.2 |
| 14 | `source` | — | Sheet name (§2.2), row number and column letter for every value **taken from the worksheet**. `intake_id` is named as assigned by the run and `build` as coming from the session log, because neither has a cell. From a CSV export the row number is `_source_row`; the sheet name and column letters describe the worksheet the export came from and cannot be re-derived from the CSV alone (§2.1) |

### 3.1 `evidence_cited`

Evidence is named in the `Evidence` column **and often inline in the `Actual Result` prose**. Both are collected.

**When neither cell names any evidence, `evidence_cited` is empty and is written `NOT IN SOURCE`**, like any other empty field (§4), and counted with them. It has no other form: never a note such as "none cited", never `none`, never blank.

Each reference carries one presence mark:

| Mark | Meaning |
|---|---|
| `ON DISK` | A file of that name was found in the evidence folder |
| `NOT FOUND` | Named in the source, no such file |
| `NOT CHECKED` | The evidence folder was not made available to this run |

**`NOT CHECKED` is never written as `ON DISK`.** An unchecked reference and a present one are different claims.

### 3.2 `observation_spans`

One `Actual Result` cell frequently contains several distinct observations. The longest cell in the reference workbook runs 4,995 characters and names three separate evidence files.

`observation_spans` lists the line ranges within `observed` that each carry a distinct observation. It does **not** summarise them, rename them or rank them — it indexes them, so that a downstream reader cannot act on the first one and lose the rest.

**What decides a boundary.** A new observation begins where the cell changes its subject: a new
enumerated item the tester wrote (`1.`, `2b.`, `a.`), a dated retest or update, a new `Part`, or a
plainly separate finding written on its own line. Blank lines belong to the observation above them.

**Where the reading is genuinely uncertain, one span covering the cell is the correct answer**
(`rules.md` §4 constraint 3). Under-splitting loses nothing a reader cannot see for themselves;
over-splitting asserts a distinction the tester did not draw, and that is an invented fact. **This is
why the field is line numbers and not prose**: a reader who disagrees with a boundary can see exactly
what was grouped and regroup it from the unchanged text.

Where a cell carries a single observation, the list has one entry covering the whole cell.

---

## 4. Refusals — the three verdicts

A field with no usable source carries exactly one of these. They are values, not prose, and a checker counts them.

| Verdict | Means | Example |
|---|---|---|
| `NOT IN SOURCE` | The cell is empty | Severity blank, because severity is the analyst's call and the tester left it |
| `IN SOURCE, UNRESOLVABLE` | Present, but not in a form this field accepts | A date written as "retest next Tuesday"; two different values for the same field in one cell |
| `NOT APPLICABLE` | Excluded by a numbered rule in `rules.md` | A field the row's own status puts out of scope |

**`IN SOURCE, UNRESOLVABLE` always names what was found.** A reader must be able to see the raw text that could not be resolved. A refusal that hides its own evidence is a shrug.

**No fourth verdict exists.** A value that is none of the above is a real value, transcribed.

---

## 5. The coverage block

One per run, at the head of the output. This is the part that makes "nothing got dropped" checkable rather than promised.

| Field | Rule |
|---|---|
| `build` | As §3 field 3 |
| `rows_in` | Every row on the worksheet |
| `rows_recorded` | Rows with a non-empty `Actual Result` |
| `rows_not_recorded` | `rows_in` − `rows_recorded`, **listed by Test ID**, never only counted |
| `records_out` | Must equal `rows_recorded`. If it does not, the run failed |
| `substantive_pass_rows` | Rows with status `Pass` whose `Actual Result` is more than a bare confirmation — **listed individually by Test ID, never collapsed to a count** |
| `multi_observation_rows` | Rows whose `observation_spans` has more than one entry, listed by Test ID |
| `evidence_not_found` | Every `NOT FOUND` reference, listed |
| `refusal_counts` | How many of each §4 verdict the run produced |

**`records_out` must equal `rows_recorded`.** That single equality is the guarantee this translator exists to make: a recorded row cannot leave the intake stage without a record.

**Why `substantive_pass_rows` is listed and not counted.** In the reference engagement, three findings that outranked most of the failures came out of rows the tester had marked `Pass` — including a spam guard silently discarding real enquiries behind a success page. A count cannot be acted on. A list can.

---

## 6. What stops a run

The run produces **no records at all**, and says which of these fired:

| Condition | Why |
|---|---|
| **No build identifier supplied** | The engagement's method states that results from two different builds cannot be compared. A record that cannot say which build it describes is not evidence |
| **Rows from more than one build in one input** | Same reason. Split the input and run twice |
| **The input's columns do not match §2** | Positions in a worksheet, header names in a CSV export (§2.1). A shifted or renamed column silently reassigns every value |

A stopped run is not an error to be worked around. It is the schema refusing to produce something untrue.

### 6.1 The stop output

A stopped run prints these six lines, in this order, and nothing else. No records and no coverage block.

| Line | Rule |
|---|---|
| `RUN STOPPED — no records produced.` | Always the first line, exactly as written here |
| `Condition:` | The §6 condition that fired, in its words from the table above, for example `Rows from more than one build in one input` |
| `Detail:` | The facts in the input that made it fire, each with the file it is in: for two builds, both build identifiers and where the session record names them |
| `Remedy:` | What the operator must do before the input can run. It never assigns a row to a build, or supplies any value the input lacks |
| `rows_in` | The number of rows in the input, counted from the input, followed by the number |
| `records_out` | Always `0` for a stopped run, followed by the number |

Print it in exactly this layout, inside one code block: each label at the start of its line, its value
on the same line, and any further lines of `Detail:` or `Remedy:` indented under the value. Counts are
lines of their own, never a sentence.

```
RUN STOPPED — no records produced.

Condition:  <the §6 condition, in its words>
Detail:     <each fact, with the file it is in>
            <further facts, indented like this>
Remedy:     <what the operator must do>
rows_in     <the number of rows in the input>
records_out 0
```

`examples.md` Example 3 is a real stop printed in this shape.

---

## 7. What this schema does not contain, and will not

There is **no field** for any of the following, and adding one is a change to this contract rather than a change to a rule:

`suspected_cause` · `code_reference` · `proposed_resolution` · `downstream_impact` · `risk_tier` · `assessed_severity` · `confidence` · `priority` · `recommendation` · `summary` · `sentiment` · `next_steps`

Every one of those is derived by reading the product's source code, not by reading the tester's cell. They are the most valuable part of what the developer eventually receives, and **not one of them is a translation.** They belong to the analysis step that follows this one.

The omission is structural on purpose. An instruction not to add analysis is a request. A schema with nowhere to put analysis is a fact.
