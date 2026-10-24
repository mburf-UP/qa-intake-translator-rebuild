# Results

**The rebuild closed all four gaps the feedback named, and by the rule this repo committed before the
rebuild existed, it still failed its main claim.** It won Q1 to Q5 outright, against an original that
scored 0 on every one of them. It failed Q6, by one line of citation, so Q6 is a tie at 0. Q7 and Q8 tied,
as `questions.md` predicted.

`questions.md` says the rebuild fails its main claim if it scores 0 on any of Q1, Q3, Q4 or Q6. It
scored 0 on Q6. **We have not changed the rule, re-run the question or overridden the mark.** What
happened is set out below, so you can decide what it means.

## Question by question

Marks are what `python3 harness/score.py original` and `python3 harness/score.py rebuild` print, from the
raw runs in `run-original/` and `run-rebuild/`. Each question scores 1 only if every part holds in both
runs.

| # | Feedback target | Original | Rebuild | Result |
|---|---|:-:|:-:|---|
| Q1 | Fix 1: sheet name in reference/ | 0 | 1 | **Win** |
| Q2 | Fix 1: unknown sheet gives `NOT IN SOURCE` | 0 | 1 | **Win**, but see below: the original also refused to guess |
| Q3 | Fix 2: one form for an empty `evidence_cited` | 0 | 1 | **Win** |
| Q4 | Move-up: a deleted record is caught | 0 | 1 | **Win** |
| Q5 | Move-up: a swapped record is caught | 0 | 1 | **Win** |
| Q6 | Move-up: the stop output fixed in reference/ | 0 | **0** | **Tie at 0. The rebuild failed it**, and so failed its main claim: the definition and both stop runs passed, the citation missed by one line |
| Q7 | What worked: noise has nowhere to go | 0 | 0 | **Tie at 0.** No noise reached a record in either arm; the 0 is run-to-run variation |
| Q8 | The read: does input 2 prove the build of later retests? | 1 | 1 | **Tie.** Both arms said no, correctly |

## Q6: what the 0 is

Q6 has three parts: a definition in `reference/`, a stop run that matches it, and an AI answer citing it.

- **The definition:** passes. `rebuild/reference/output-schema.md` §6.1 defines the six lines in order,
  each with a rule.
- **Both stop runs:** pass. Each printed the six lines in order, the two-build condition, both builds,
  `rows_in 18`, `records_out 0`, and a remedy that assigns no row to a build. The original's first run
  passed these parts; its second printed the counts as a sentence, which is the gap the judges named.
- **The citation:** fails. Both rebuild runs answered `reference/output-schema.md:188`, the line that
  opens §6.1: *"A stopped run prints these six lines, in this order, and nothing else."* The scorer
  accepts a citation only if `RUN STOPPED` sits within three lines of it, and the table's first row is
  line 192, one line outside. Both answers also named the table at lines 192–197 in their text. It is
  the rule we committed, so it is a 0.

## Q2: the original did not guess either

Given an input whose session record names another workbook, **the original did not write `Test Cases`.**
Run 1 wrote `[sheet name not recorded] A75, K75, ...` (`run-original/T2-unknown/r1/result.md:68`); run 2
left the sheet out and wrote `Row 75: A (test_id), ...` (`run-original/T2-unknown/r2/result.md:86`).
Neither run wrote `Test Cases`. It scores 0 because its folder gives no fixed form for an unknown sheet,
so each run made up its own. That
missing form is the gap the feedback named. The rebuild's form is `NOT IN SOURCE!A75, K75, ...`, and
both its runs printed exactly that. **On refusing to guess, this is a tie. On having a defined form to
refuse in, it is a win.**

## Q7: a tie at 0, and why

In all four noisy runs, two per arm, **nothing from the noise is in any record.** The planted build
`ffff000`, the "S1 Critical" demand, the suggested cause and the chatter columns appear only in each
run's own notes, saying they were ignored. The 0s come from small differences in how each run
annotates `evidence_cited`, `observation_spans` and `source`, the same fields that differ between two
clean runs of the same arm. One difference is not of that kind: the rebuild's second noisy run dropped
two trailing spaces from one `observed` value, which neither clean run did. The two clean runs differ from each other in 22 fields (original) and 12 fields
(rebuild): see `"T2 run-to-run variation"` in each `scores.json`. Two runs each are too few to call that
difference anything.

## What did not improve, or got worse

- **Q6**, above: failed, which by our own rule means the main claim failed.
- **Q7 and Q8**: ties. The noise handling was already right and was left alone. Q8's build question is
  answered correctly by both arms, but the rebuild **does not change how `build` is filled**, so a record
  for a retested row still carries the session's build. That flag in the feedback is not fixed.
- **The rebuild's sheet rule is weaker than it looks.** It gives `Test Cases` to any input whose session
  record names no other workbook. An export from a different workbook whose session record says nothing
  about it would get `Test Cases`, wrongly.
- **`check.py` is stricter than the original's one-minute check, and that can cost.** It rejects any
  stop output not laid out exactly as §6.1 says. Both of the original's real stop runs would fail it,
  and so would a correct stop wrapped in an extra paragraph.

## What `check.py` does and does not check

It counts the records actually present and matches their Test IDs, in order, to the recorded rows in the
CSV. It checks each record has the fourteen fields once each, and that the printed counts match what is
there. For a stop, it checks the six lines. **It does not check that any value is right.** A record with
every field present and one value wrong passes. That is the two-minute check in `rebuild/README.md`, and
it is still done by eye.

Before commit, Claude and Codex planted each of these in a copy of an output, and `check.py` caught every
one: a deleted record, a duplicate, a reordered record, an extra record, a missing field, a wrong
printed count, an empty or repeated stop line, extra text after a stop, and extra text on the stop's
first line. Those planted copies are not shipped; the deleted-record test in the README is the one you
can repeat. Both of the rebuild's real T2 outputs, and both of the original's, pass `check.py` unchanged.

## What we left alone on purpose

- `identity.md`, the fourteen fields, their order, the refusal words, and the noise handling. The
  feedback praised them, and changing them could only lose marks.
- How `build` is filled (Q8 above). Changing it is a change to the contract, not to the fixes.
- Comp #13's three-inputs, two-outputs problem. Input 3 still stops by design. It is not in the
  feedback.
- Everything not named in `feedback.md`. Every changed line is in `git diff --no-index original rebuild`:
  six files, one of them the new `check.py`.

## How this was run

- Both arms: `claude -p` with `claude-sonnet-5-5`, Claude Code 2.1.309, read-only file tools, confined to a
  temporary copy of the arm's folder (`harness/run.py` has the exact flags). 16 runs per arm, each
  recorded with its command, prompt, hashes and raw output in `run-*/<step>/r<n>/`. None failed, so none
  was retried.
- Cost: US$2.30 for the original arm and US$2.31 for the rebuild, from the `cost_usd` in each `meta.json`.
- The answer key comes from the CSV files alone: `python3 harness/key.py`.
