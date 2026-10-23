# The inputs

Three real inputs from a live software QA engagement, shipped so this translator can be run rather
than described. A fourth has been held back and is not in this repository — see below.

## What these are

Each folder is **one input**: the recorded rows of a test-case worksheet for one test session, plus the
session record that carries the build identifier. Both are needed. The worksheet does not hold the
build, and without it the run produces nothing (`reference/output-schema.md` §6).

| Folder | Rows | Build | What it exercises |
|---|---:|---|---|
| `input-1-2026-09-20/` | 30 | `e52b8c4` | The long one. Two sittings, one build, prose from 4 to 2,299 characters |
| `input-2-2026-09-18/` | 9 | `a17e3d0` | The short one. Easiest to check by hand end to end |
| `input-3-2026-08-28/` | 18 | `b41c07e` + `c98f215` | **Stops the run.** Two builds in one input |

`cases.csv` carries the ten worksheet columns this translator reads, with the header row naming each.
`_source_row` is the worksheet row number, kept so every value can be traced back to a cell.

## Two of these three produce records, and the third is supposed not to

**Say the obvious thing first: feed this translator the three inputs above and you get two outputs, not
three.** Inputs 1 and 2 run to completion and produce records of an identical shape. Input 3 stops at
`rules.md` §1 step 3 and produces nothing at all, because its session log names two builds and the
worksheet has no build column, so no row can be assigned to either one.

**That is the contract working, and here is the argument.** The engagement this came from holds that
results from two different builds cannot be compared. To emit records for input 3, the translator would
have to decide which build each row describes, and **that fact is not in the input** — so every one of
those 18 records would carry an invented value in a field that exists to make the record evidence. A
translator that guesses the build produces 18 records that look right and cannot be relied on. This one
produces nothing and says which step stopped it.

**The counter-argument, stated plainly rather than hidden:** a reader who wants three inputs to give
three same-shaped outputs receives two, and can reasonably call that shape not held. We think refusing
is the stronger answer, because the alternative is the one failure this competition disqualifies. **Both
readings are available to you and the evidence for each is in this folder** — run input 3 and watch
where it stops.

**If you want a third completed run**, input 1 and input 2 differ from each other far more than either
differs from a third session: 30 rows against 9, `Actual Result` prose running 4 to 2,299 characters
against 392 to 1,684, and 54 evidence references in the `Evidence` column plus two named only in the
prose, against 32. The shape holds across both.

## These are de-identified, and here is exactly how

The engagement is real, commercial and live, and it is not ours. Every input was rewritten before it
reached this repository:

- the product's name and its domain were replaced with a fictional name and a `.example` domain;
- the test-case prefix was changed;
- the tester is `TR1`; the test accounts are `acct-a` through `acct-pro`;
- the developer the findings are handed to is `DEV1`;
- the build identifiers were replaced with different strings of the same shape.

**The substitution is consistent across all files**, so a value in an input still traces to the same
value in an output, which is the property that matters for checking this translator's claims.

**Nothing else was touched.** The prose in `Actual Result` is the tester's own, including its typos,
fragments, mid-thought corrections and digressions, because those are the thing this translator exists
to preserve. If a sentence reads oddly, that is the source, not an artefact of de-identification.

## The held-back input

A fourth input — a 10-row session on a single build — exists and is deliberately **not** in this
repository. It was set aside before any of this folder was written, so that the translator could be
run once, cold, on rows nobody had designed against.
