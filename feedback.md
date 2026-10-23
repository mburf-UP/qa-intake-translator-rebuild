# Mike Burford: qa-intake-translator

Comp #13: The Translator. We read your repo at the commit that was public when the clock stopped: [https://github.com/mburf-UP/qa-intake-translator](https://github.com/mburf-UP/qa-intake-translator) (`ed18d22`).

**What you built.** A translator from the recorded rows of a test-case worksheet to one fixed 14-field intake record per row, each value traced to its cell.

---

## The read

**Contract fidelity.** Fourteen fields, same order, all three runs. We blanked Actual Result on three rows and Date Tested, Tester and Evidence on others. The record count dropped as your contract says, and the three rows came back by Test ID under `rows_not_recorded 3, listed:`. We added two chatter columns and stapled a reply-all naming another build; the output was byte-identical to the clean run. The gap: the stop output's fields (`Condition:`, `Detail:`, `Remedy:`) exist only by example at `examples.md:154-166`, and reference/ never fixes the serialization.

**Traceability.** Content character for character, typos and double spaces kept. One string traces to nothing shipped: the sheet name in your `source` locator, `Test Cases!A96` (`examples.md:51`, `:123`, `:210`). `grep -rn "Test Cases"` finds it only in `examples.md`: in no input, no `session.md`, nowhere in reference/. `output-schema.md:87` already says the sheet name cannot come from the CSV. It is a locator, and the spec has a hole where its sheet name should be. Separately, build `a17e3d0` is attached to MD-SHELL-012, whose cell holds "Retest 20/9" inside the 2026-09-18 input.

**Methodology.** Each file has one job, and the no-source rule is explicit at `rules.md:30`. Your own two records for row 96 write an empty `evidence_cited` two ways: `(none cited)` at `examples.md:118`, `NOT IN SOURCE` at `examples.md:205`. The refusal count at `examples.md:250` agrees with the first. The repo ships no code: 14 files, all `.md`, `.csv` and `.gitignore`, while `output-schema.md:4` and `:125` refer to checkers.

**README and shipped input.** Three real de-identified inputs, one built to stop the run, and all five questions answered. We deleted the MD-DARK-011 record from an output and applied your one-minute check (`README.md:102-103`). It passed: `records_out=9`, `rows_recorded=9`, eight records present. Only the ordinal rule at `field-definitions.md:35` catches it, and nothing runs that rule.

---

## Your trace table

Five claims from your committed records for input 2 in `examples.md`, against `inputs/input-2-2026-09-18/cases.csv`.

| # | What we picked | Your output says | Where it is in the input | Holds |
|---|---|---|---|---|
| 1 | A date | `date_tested 2026-09-18` (`examples.md:30`) | `cases.csv:17`, Date Tested cell | Yes |
| 2 | A name | `MD-SHELL-012-Request-Count-18Sep NOT CHECKED` (`examples.md:40`) | `cases.csv:17`, Evidence cell | Yes. Capital R and C kept |
| 3 | An action item | `recorded_defect_id OBS-201, OBS-213, OBS-214, OBS-215, OBS-216` (`examples.md:34`) | `cases.csv:17` | Yes |
| 4 | The interpretive field | `substantive_pass_rows 3, listed:` at 437, 528 and 419 characters (`examples.md:231-233`) | Pass rows at `cases.csv` lines 21, 31, 37; rule at `field-definitions.md:136`, "more than 40 characters" | Yes. Reproduces exactly |
| 5 | The one that looks too clean | `source Test Cases!A96, K96, L96, ...` (`examples.md:210`) | Row 96 is `_source_row` at `cases.csv:21`; column letters from `output-schema.md:27-38`. The sheet name is in no input and not in reference/ | Stretch. A spec gap in the locator |

**Reverse checks.** The 567-character Notes cell on MD-SHELL-014 (`cases.csv:21`) is captured whole as `tester_notes`, apart from `observed` (`examples.md:204`). The prose-only evidence references: `examples.md:278-280` names input 1's two, and both check out against the CSV. Both pass.

---

## What worked

1. **Noise has nowhere to go.** With chatter columns and a stapled reply-all added, `diff` of the clean and noisy outputs returned nothing. `reference/output-schema.md:175-183` forbids analysis fields by name, so an "S1" opinion in an email cannot land.

2. **You built the input that should stop the translator, and it stops.** Input 3 stops on "Rows from more than one build in one input" with no records produced. `inputs/README.md:35-39` states the case against your own stop.

## Two fixes

1. **Put the sheet name in reference/.** Add `Test Cases` to `reference/output-schema.md`, next to the locator rule at `:87`, as the sheet name for this workbook's CSV exports. Then `Test Cases!A96` traces to a shipped file. For a workbook whose sheet name is unknown, the rule says `NOT IN SOURCE`.

2. **Pick one form for an empty `evidence_cited`.** Write it into `reference/output-schema.md`, fix whichever of `examples.md:118` and `:205` disagrees, and correct the refusal count at `:250`.

---

**What would have moved you up a tier.** A check that counts the records actually present, so a dropped record fails in a minute, and the stop output's fields written into reference/ so a stop is a fixed shape.
