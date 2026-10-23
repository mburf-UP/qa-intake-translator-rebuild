# QA intake translator

**Converts:** the recorded rows of a software test-case worksheet, for one test session
**Into:** one observation intake record per recorded row — fixed fields, fixed order, every value
traced to a named cell, nothing inferred, every row accounted for

Drop this folder into a Claude project. Claude becomes the translator. Loading the folder does not
start a translation on its own — you give it one prompt per session, and the exact wording to paste
is under *How to use it* below.

---

## The 60-second version

A tester runs a session and types what they saw into the `Actual Result` cell of each test case. Someone
then has to turn those cells into structured records a developer can act on.

Today that is done by an AI assistant in an ordinary chat session, working from a 784-line method
document, with no fixed output shape and nothing checking it. **It drops things.** In the engagement
this was built from, the backlog generated from the register on 2026-09-21 showed 228 findings recorded
all time, 184 still open, and **thirty of those open findings had never appeared in any delivered
packet** — eleven of them rated major.

They were not lost at the end. They were lost at the start, by a filter: only rows marked `Fail`,
`Partial` or `Blocked` entered the pipeline, so a `Pass` row with four lines of real observation in it
was never picked up at all.

**This translator gives every recorded row a record, unconditionally, and then proves it with one
equality: `records_out` must equal `rows_recorded`.**

It does one more thing, and it is the design decision worth arguing with: **it produces only the half of
the record that traces to the tester's words.** Cause, code reference, proposed fix, downstream impact,
risk tier and assessed severity are all derived by reading the product's source — so under a fidelity
contract every one of them would be invented. There is no field for any of them, and that absence is the
guarantee. An instruction not to add analysis is a request. A schema with nowhere to put analysis is a fact.

---

## How to use it

### 1. Load the folder

Create a Claude project (or any assistant that reads a folder) and add these files:

```
identity.md                      what this is, and the four things it refuses
rules.md                         the procedure: order of work, how a value is taken
reference/output-schema.md       THE CONTRACT — the shape of the output
reference/field-definitions.md   per field: what would make a value wrong
examples.md                      three worked examples and a full coverage block
```

Claude reads `identity.md` and `rules.md` to know what to do, and `reference/output-schema.md` to know
what to produce. **If the output ever disagrees with the schema, the schema is right and the output is
wrong.**

### 2. Feed it one session

An input is **two things**, and it will not run with only the first:

| | What | Why |
|---|---|---|
| 1 | The recorded rows — `cases.csv` | The observations |
| 2 | The build identifier — `session.md` | Not in the worksheet. Without it the run produces nothing |

Three real inputs are in `inputs/`. To try one, paste this:

```
Translate inputs/input-2-2026-09-18/cases.csv using the build identifier in
inputs/input-2-2026-09-18/session.md. Follow reference/output-schema.md exactly.
The evidence folder is not available to this run.
```

Start with **input 2**. It is nine rows, which is small enough to check by hand end to end.
**`examples.md` has one record with nothing left out** — the section called *One record with nothing
left out*, where all fourteen fields carry their whole value so you can compare it against row 96 of
input 2 character for character. The two worked examples before it abbreviate their long fields on
purpose, to keep the point of each visible, and say where they do. There is also a full coverage block
for all nine rows.

**Input 3 produces no records, on purpose.** Its session log names two builds and the worksheet has no
build column, so no row can be assigned to either; the run stops at `rules.md` §1 step 3. That means
three inputs give **two** completed outputs, not three. The reasoning, and the argument against it, are
in `inputs/README.md` — stated there rather than left for you to discover.

### 3. Read what comes back

- **One coverage block** for the run — the arithmetic, plus four things listed by Test ID rather than
  counted.
- **One record per recorded row**, in input row order, each with the same fourteen fields in the same
  order, every one present.

Fields with no source carry one of exactly three refusals — `NOT IN SOURCE`, `IN SOURCE, UNRESOLVABLE`,
`NOT APPLICABLE` — and the middle one always quotes the raw text it could not resolve.

---

## How to check it kept its promise

You do not have to take any of this on trust. In rough order of speed:

**The one-minute check.** Open the coverage block. Does `records_out` equal `rows_recorded`? Count the
data rows in the CSV. That equality is the whole guarantee and it is arithmetic.

**The two-minute check.** Pick any record. Every field carries a `source` locator — sheet, row, column.
Open `cases.csv` at that row and compare. Look especially at `observed`: it should be the whole cell,
including the typos, the fragments and the digressions. **If it reads better than the cell, it is wrong.**

**The invention check — the one the brief cares about.** Take any claim in any record and find it in the
input. There is nowhere for an invented fact to hide, because there is no field that is not a copy of a
named cell. The two places to press hardest:

- a date. `date_tested` must read as the cell reads. A cell saying *"retest next Tuesday"* must come back
  `IN SOURCE, UNRESOLVABLE` quoting those words, never a calendar date;
- a severity. **52 of the 57 shipped rows have an empty `Severity` cell**, so `NOT IN SOURCE` should be
  common. **A run that fills this field is a run that is inventing.** One row carries the literal text
  `N/A`, which is a transcribed value and not a refusal — the tester wrote it. The two look alike in a
  report and are different claims.

**The refusal check.** `inputs/input-3-2026-08-28/` must produce **no records at all**. It is a real day
on which a new build landed mid-session, and the schema stops rather than attach true observations to the
wrong version. If you get 18 records out of it, the translator has failed.

**The it-holds-across-inputs check.** Run inputs 1 and 2. The field list, the field order and the refusal
vocabulary are identical in both, and neither is shaped by what its rows happened to contain.

---

## What is in this folder

| Path | What it is |
|---|---|
| `identity.md` | What it converts, what it refuses, and what it is protecting |
| `rules.md` | The procedure — order of work, how a value is taken, what is never added |
| `examples.md` | Three worked examples, plus one full coverage block with measured figures |
| `reference/output-schema.md` | **The contract.** Fields, order, refusals, coverage block, stop conditions |
| `reference/field-definitions.md` | Per field: what it is, what it accepts, what would make it wrong |
| `inputs/` | Three real de-identified inputs, one of which stops the run. See `inputs/README.md` |

There is exactly one copy of the schema. No other file restates it.

---

## About the inputs

They are real, from a live commercial QA engagement, used with the owner's permission and **de-identified
before they reached this repository** — product name, domain, test-case prefix, tester, test accounts and
build identifiers all replaced, consistently, so a value in an input still traces to the same value in an
output.

**The prose was not touched.** Typos, sentence fragments, mid-thought corrections and the tester's asides
are the tester's own, because they are the thing this translator exists to preserve. If a sentence reads
oddly, that is the source.

`inputs/README.md` states exactly what was substituted.

---

## What this translator is not

It is not the analyst. The step that follows — cause, code reference, proposed resolution, downstream
impact, risk tier, severity — is the most valuable work in the engagement, and **none of it is a
translation.**

Separating the two is the entire point. When observation and analysis are produced in one pass, the
analysis contaminates the observation. In the engagement this came from, that has already produced a test
case written to chase a discrepancy that did not exist, and a run order that told a first-view tester
what the code said they should see.

This folder produces the record of what was seen. Someone else works out what it means.
