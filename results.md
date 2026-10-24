# Results

**By the rule this repo committed before the rebuild existed, the rebuild failed its main claim.** On the
committed runs it scored 1 on Q1 to Q5, against an original that scored 0 on every one of them. On an
independent re-run its clear wins were four, because Q2 flipped. It failed Q6: the scorer's citation check
missed by one line, and one of its two committed stop outputs breaks the stop layout the rebuild itself
defines. Q7 and Q8 tied, as `questions.md` predicted.

`questions.md` says the rebuild fails its main claim if it scores 0 on any of Q1, Q3, Q4 or Q6. It
scored 0 on Q6. **We have not changed the rule, re-run the question or overridden the mark.** What
happened is set out below, so you can decide what it means.

## An independent re-run, after this file was first written

After the repo went public, a fresh Codex session that had no part in building this entry cloned it and
re-ran all 32 AI steps from the committed prompts, using Claude Code 2.1.310. Its report is not in this
repo; what it found is below, and none of it changes the committed marks.

- **The original scored the same:** 0 on Q1–Q7, 1 on Q8.
- **The rebuild scored 1, 0, 1, 1, 1, 0, 0, 1**, against the committed 1, 1, 1, 1, 1, 0, 0, 1. **Q2 flipped:**
  one of its two fresh runs listed the right cells in a different order from the committed answer, so Q2
  is not stable. **On a re-run, the rebuild's clear wins are four (Q1, Q3, Q4, Q5), not five.**
- **One committed stop output fails the rebuild's own `check.py`.** `run-rebuild/T3/r2/result.md` prints
  the six stop lines correctly and then a list of where each came from. §6.1 says "nothing else", so
  `check.py` rejects it, although `score.py`'s narrower Q6 check passed it. The fresh run's second stop
  output failed `check.py` too. *Our reading, not proven:* every prompt asks the model to "cite the file
  and line for each answer", and that pulls commentary into the output.
- **A missing-build input**, removing `session.md`, stopped correctly in both fresh rebuild runs, and
  one of the two again added prose around the stop.

## Question by question

Marks are what `python3 harness/score.py original` and `python3 harness/score.py rebuild` print, from the
raw runs in `run-original/` and `run-rebuild/`. Each question scores 1 only if every part holds in both
runs.

| # | Feedback target | Original | Rebuild | Result |
|---|---|:-:|:-:|---|
| Q1 | Fix 1: sheet name in reference/ | 0 | 1 | **Win** |
| Q2 | Fix 1: unknown sheet gives `NOT IN SOURCE` | 0 | 1 | **Win on the committed runs; flipped to 0 on the independent re-run.** The original also refused to guess (below) |
| Q3 | Fix 2: one form for an empty `evidence_cited` | 0 | 1 | **Win** |
| Q4 | Move-up: a deleted record is caught | 0 | 1 | **Win** |
| Q5 | Move-up: a swapped record is caught | 0 | 1 | **Win** |
| Q6 | Move-up: the stop output fixed in reference/ | 0 | **0** | **Tie at 0. The rebuild failed it**, and so failed its main claim: the scorer's citation check missed by one line, and one committed stop output fails `check.py` |
| Q7 | What worked: noise has nowhere to go | 0 | 0 | **Tie at 0.** No noise reached a record in either arm; run-to-run variation is a possible cause, with one exception (below) |
| Q8 | The read: does input 2 prove the build of later retests? | 1 | 1 | **Tie.** Both arms said no, correctly |

## Q6: what the 0 is

Q6 has three parts: a definition in `reference/`, a stop run that matches it, and an AI answer citing it.

- **The definition:** passes. `rebuild/reference/output-schema.md` §6.1 defines the six lines in order,
  each with a rule.
- **Both stop runs:** pass `score.py`'s Q6 check. Each printed the six lines in order, the two-build condition, both builds,
  `rows_in 18`, `records_out 0`, and a remedy that assigns no row to a build. The original's first run
  passed these parts; its second printed the counts as a sentence, which is the gap the judges named.
- **The citation:** fails. Both rebuild runs answered `reference/output-schema.md:188`, the line that
  opens §6.1: *"A stopped run prints these six lines, in this order, and nothing else."* The scorer
  accepts a citation only if `RUN STOPPED` sits within three lines of it, and the table's first row is
  line 192, one line outside. Both answers also named the table at lines 192–197 in their text. It is
  the rule we committed, so it is a 0.
- **Not scored, and worse than the citation:** `score.py` checks only that the six lines appear in order.
  The second committed stop output, `run-rebuild/T3/r2/result.md`, follows them with a list of sources,
  so it fails the rebuild's own `check.py` and the "nothing else" in §6.1. The fix's stop shape held in
  one committed run of two.

## Q2: the original did not guess either

Given an input whose session record names another workbook, **the original did not write `Test Cases`.**
Run 1 wrote `[sheet name not recorded] A75, K75, ...` (`run-original/T2-unknown/r1/result.md:68`); run 2
left the sheet out and wrote `Row 75: A (test_id), ...` (`run-original/T2-unknown/r2/result.md:86`).
Neither run wrote `Test Cases`. It scores 0 because its folder gives no fixed form for an unknown sheet,
so each run made up its own. That
missing form is the gap the feedback named. The rebuild's form is `NOT IN SOURCE!A75, K75, ...`, and
both its runs printed exactly that. **On refusing to guess, this is a tie. On having a defined form to
refuse in, it is a win on the committed runs**, and it did not hold on the independent re-run.

## Q7: a tie at 0, and why

In all four noisy runs, two per arm, **nothing from the noise is in any record.** The planted build
`ffff000`, the "S1 Critical" demand, the suggested cause and the chatter columns appear only in each
run's own notes, saying they were ignored. A possible cause of the 0s is small differences in how each run
annotates `evidence_cited`, `observation_spans` and `source`, the same fields that differ between two
clean runs of the same arm. One difference is not of that kind: the rebuild's second noisy run dropped
two trailing spaces from one `observed` value, which neither clean run did. The two clean runs differ from each other in 22 fields (original) and 12 fields
(rebuild): see `"T2 run-to-run variation"` in each `scores.json`. Two runs each are too few to call that
difference anything.

## What did not improve, or got worse

- **Q6**, above: failed, which by our own rule means the main claim failed, and one stop output breaks
  the rebuild's own §6.1.
- **Q2** flipped on the independent re-run (above).
- **Q7 and Q8**: ties. The noise handling was already right and was left alone. Q8's build question is
  answered correctly by both arms, but the rebuild **does not change how `build` is filled**. The
  committed record for MD-SHELL-012 (`run-rebuild/T2/r1/result.md:60`) gives build `a17e3d0`, the 18
  September sitting's, to a cell that also describes retests on 14 and 20 September, with no evidence of
  which build those ran on. That flag in the feedback is not fixed.
- **The rebuild's sheet rule is weaker than it looks.** It gives `Test Cases` to any input whose session
  record names no other workbook. An export from a different workbook whose session record says nothing
  about it would get `Test Cases`, wrongly.
- **`check.py` is stricter than the original's one-minute check, and that can cost.** It rejects any
  stop output not laid out exactly as §6.1 says. Both of the original's real stop runs would fail it,
  and so would a correct stop wrapped in an extra paragraph.

## What `check.py` does and does not check

`rebuild/reference/output-schema.md:4` says `check.py` checks an output against §5 and §6.1. **That
overstates it.** For §5 it checks only the counts, not the lists: a `substantive_pass_rows` of 99 passes.
It counts the records actually present and matches their Test IDs, in order, to the recorded rows in the
CSV. It checks each record has the fourteen fields once each, and that the printed counts match what is
there. For a stop, it checks the six lines. **It does not check that any value is right, or that any
citation points where it should.** The independent check planted six faults it does not catch, and each
printed `PASS`: a changed date, a true value moved to the wrong field, a citation shifted to a real
neighbouring line, an invented sentence among correct values, and an empty field written blank or as
`(none cited)`. It also passed `substantive_pass_rows 99`. That is the two-minute check in `rebuild/README.md`, and
it is still done by eye.

Before commit, Claude and Codex planted each of these in a copy of an output, and `check.py` caught every
one: a deleted record, a duplicate, a reordered record, an extra record, a missing field, a wrong
printed count, an empty or repeated stop line, extra text after a stop, and extra text on the stop's
first line. Those planted copies are not shipped; the deleted-record test in the README is the one you
can repeat. Both of the rebuild's real T2 outputs, and both of the original's, pass `check.py` unchanged.

## Known limits

- **AI results vary.** Two runs per arm are too few to show how much. Q2 flipped on a re-run, Q7 differs
  between any two runs, and stop outputs sometimes carry commentary. No effort setting was fixed:
  `harness/run.py` uses Claude Code's default. The committed runs record version 2.1.309; the independent
  re-run used 2.1.310.
- **No independent unseen input was tested.** The independent check also ran two rows held back from
  input 1, but those rows ship in this repo, so they are not inputs the folder has never seen.
- **Noise reaches the prose around the records.** In both rebuild noisy runs, the reply-all's `ffff000`
  and "S1 Critical" are quoted in the run's notes saying they were ignored, though in no record. The
  schema gives that material no field.
- **`observed` shows two trailing spaces as `␣␣`**, a notation inherited from the original's examples,
  so a byte-for-byte comparison with the CSV fails on two rows (MD-SHELL-014 and MD-SEC-006).
- **The sheet name `Test Cases` cannot be checked from this repo.** The workbook is a live commercial
  engagement and does not ship; `rebuild/reference/output-schema.md` §2.2 declares the name, and that
  declaration is the source.
- **The answer key comes from the same CSV files both arms read.** It does not read either arm, but the
  CSVs are the only source there is; there is no second path to it.
- **Claims about the engagement in `original/` and `rebuild/` cannot be checked from here**: the size of
  its method, its backlog figures, the 4,995-character cell, the owner's permission and the
  de-identification. They are carried unchanged from the judged entry.
- **The AI arms need Claude Code.** A machine with only Python and git can check the pin, the key, the
  marks from the committed runs and `check.py`, but cannot re-run the AI.

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
