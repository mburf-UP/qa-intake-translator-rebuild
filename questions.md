# Questions

Written and committed before `rebuild/` exists. Never edited after this commit; a correction would be a new, dated file beside this one, and both would be kept.

Every question comes from a line in `feedback.md`. That file names four targets: two fixes, and a
move-up line with two parts.

| Target | `feedback.md` says | Questions |
|---|---|---|
| **Fix 1** | Put the sheet name in reference/ (line 45) | Q1, Q2 |
| **Fix 2** | Pick one form for an empty `evidence_cited` (line 47) | Q3 |
| **Move-up, part 1** | A check that counts the records actually present (line 51) | Q4, Q5 |
| **Move-up, part 2** | The stop output's fields written into reference/ (line 51) | Q6 |
| What worked | Noise has nowhere to go (line 39) | Q7, expected tie |
| The read | Build `a17e3d0` attached to MD-SHELL-012, whose cell holds "Retest 20/9" (line 13) | Q8, expected tie or loss |

## How each arm is run

The two arms differ in one thing: the folder. `original/` on one arm, `rebuild/` on the other. Same inputs, same prompts, same order, Q1 to Q8.

**AI steps.** One fresh session per step, run from a temporary copy of the arm's folder, with nothing
else in it except the named input:

```sh
claude -p --restricted --strict-mcp-config --safe-mode --permission-mode dontAsk \
  --model claude-sonnet-5-5 --tools Read,Glob,Grep \
  --no-session-persistence --output-format json "<prompt>"
```

`--tools` leaves the model able to read files and nothing else: no web, no shell. `--restricted`
confines those tools to the session's own folder and ignores every settings file; `--strict-mcp-config`
and `--safe-mode` load no MCP server, CLAUDE.md, skill, plugin or hook; `--permission-mode dontAsk`
refuses anything that would need approval. What was tested, on Claude Code 2.1.309 before this
commit: a read of a file outside the folder and a listing outside it were both refused, and reads
inside it worked. Without these flags, the same read outside the folder succeeded. The session never sees `feedback.md`, this file, the other arm or an earlier transcript. Every prompt starts with the same line, and every prompt is in `harness/prompts.json`, word for word:

> Use only the files in this folder. Cite the file and line for each answer. If the folder or the input
> cannot establish something, say so.

**Every AI step runs twice per arm.** A question scores 1 for an arm only if both runs score 1. If the
two runs disagree, the question is reported as **unstable** and scores 0.

**Script steps.** Python 3.9 or later, standard library only, in `harness/`. `harness/run.py` runs the
AI steps; `harness/score.py` marks them. No mark is set by hand: the mark is what `score.py` prints.

**Recorded for every run** in `run-original/` and `run-rebuild/`: the exact command, the prompt, the model and Claude Code version, the SHA-256 of the prompt and of every input file, the raw output, and the exit code. Nothing is removed, including failed runs.

## The translations the questions read

| Step | Input | Used by |
|---|---|---|
| **T2** | `inputs/input-2-2026-09-18/`, unchanged | Q1, Q3, Q4, Q5, Q7 |
| **T3** | `inputs/input-3-2026-08-28/`, unchanged | Q6 |
| **T2-unknown** | `fixtures/t2-unknown/`: input 2's `cases.csv`, byte for byte. Its `session.md` gains one table row: `\| Workbook \| A different project's QA workbook. Sheet name not recorded. \|` | Q2 |
| **T2-noisy** | `fixtures/t2-noisy/`: input 2 with two extra columns, `Chatter A` and `Chatter B`, of off-topic text on every row, and a `reply-all.txt` beside it naming build `ffff000` and calling one row "S1" | Q7 |

Prompt for each: *"Translate the input in `<path>` exactly as this folder says to, and print the full
output."* The two fixtures are copied into the session's folder at `test-input/<name>/`, and
`harness/make_fixtures.py --check` confirms they are what it generates from input 2.

The questions answered by the AI directly (Q1, Q3, Q6, Q8) end with an instruction to finish on one
line, `ANSWER: ...`, so the answer can be marked without anyone reading it and choosing.

## The questions

**Q1. Fix 1.** In T2, the record for worksheet row 96 has a `source` locator beginning `Test Cases!`.
Which file in `reference/` states that `Test Cases` is the sheet name?
- **Expected, rebuild:** `reference/output-schema.md`, at the locator rule.
- **Expected, original:** none. `Test Cases` appears only in `examples.md`, as the judges found.
- **Scored by:** script (`Test Cases` stated as the sheet name in a `reference/` file) and AI (names that file and line). Both must hold.

**Q2. Fix 1, the unknown case.** In T2-unknown, what sheet name does each `source` locator carry?
- **Expected:** every locator begins `NOT IN SOURCE!`, followed by its own row's cells, unchanged:
  columns A and K to S, as in `original/reference/output-schema.md:27-38`. The nine
  records keep input 2's Test IDs, in order, each with all fourteen fields.
- **Scores 0 if:** any locator carries `Test Cases` or any other sheet name.
- **Scored by:** script, on T2-unknown's output.

**Q3. Fix 2.** What is the one value for `evidence_cited` when neither the Evidence cell nor the Actual Result names any evidence?
- **Expected:** `NOT IN SOURCE`, stated once in `reference/output-schema.md`.
- **Also required:** both of `examples.md`'s records for row 96 use it, and the `NOT IN SOURCE` refusal count in the input-2 coverage block is **18**. Derived from `cases.csv` directly: 7 empty Severity, 2 empty Defect ID, 8 empty Notes, and 1 empty `evidence_cited` (MD-SHELL-014, whose Evidence cell is empty and whose Actual Result names nothing). The original says 17 and writes the field two ways.
- **And, in T2:** `NOT IN SOURCE` appears in exactly the 18 places the CSV is empty (MD-SHELL-014's
  `evidence_cited` among them) and nowhere else, and T2's printed `NOT IN SOURCE` count is 18.
- **Scored by:** script on the folder and on T2, and AI stating the value and its file.

**Q4. Move-up, part 1: a deleted record.** Take T2's output and delete the whole MD-DARK-011 record.
Leave `rows_recorded 9` and `records_out 9` as printed. Apply the arm's own documented check.
- **Expected, rebuild:** the check accepts T2 as produced, then rejects the deleted version, printing
  a line with `MISSING` and `MD-DARK-011`. A check that rejects everything scores 0.
- **Expected, original:** passes. Its check (`original/README.md:102-103`) compares two printed
  numbers, which still agree. This is the judges' own test, repeated.
- **Scored by:** script. The deletion is done by `harness/mutate.py`. The original's check is applied
  exactly as its README states it (`harness/original_check.py`). The rebuild's check is
  `python3 check.py OUTPUT INPUT_DIR`, run from inside `rebuild/`: exit 0 accepts, anything else
  rejects. This fixes the rebuild's check before the rebuild exists, so it cannot be shaped to the
  test afterwards.

**Q5. Move-up, part 1: a swapped record.** Take T2's output, replace the MD-DARK-014 record with a second copy of the MD-DARK-011 record, and leave nine records and both counts at 9.
- **Expected, rebuild:** the check accepts T2 as produced, then rejects the swapped version, printing
  a line with `DUPLICATE` and `MD-DARK-011` and a line with `MISSING` and `MD-DARK-014`.
- **Expected, original:** passes.
- **Why it is here:** a check that only counts records would pass Q5.
- **Scored by:** script, as Q4.

**Q6. Move-up, part 2.** In T3, do the stop output's fields and their order match a definition in
`reference/`, and are its values the ones below?
- **Expected, rebuild:** yes. `reference/` defines the stop output field by field, and T3 matches it:
  no records, the two-build condition, both builds `b41c07e` and `c98f215` named, a remedy that does not guess which row belongs to which build, `rows_in 18`, `records_out 0`.
- **Expected, original:** no definition in `reference/`. The fields exist only by example
  (`examples.md:154-166`), as the judges found.
- **Scored by:** script and AI. The script needs a `reference/` section that names the two-build
  condition and lists the six fields (`RUN STOPPED`, `Condition`, `Detail`, `Remedy`, `rows_in`,
  `records_out`) in that order, each after `RUN STOPPED` with a rule beside it. It checks the definition's shape, not what its prose means; no script
  can, and `results.md` will say so. T3 must print them in that order, with
  `Condition` naming more than one build and `Detail` naming both builds. The AI must cite that
  definition. "Does not guess" is checked as: the Remedy names neither build. That is a narrower test
  than the sentence, and `results.md` will say so.

**Q7. What worked, kept.** Do T2 and T2-noisy differ in any field other than `intake_id`? Run 1 of
each is compared with run 1 of the other, and run 2 with run 2.
- **Expected: tie.** No difference in either arm. The original already passed this, and the rebuild
  leaves it alone.
- **Scored by:** script, comparing parsed records. The two clean T2 runs are compared with each other as
  well, unscored, so a difference on Q7 can be read against ordinary run-to-run variation rather than
  blamed on the noise.

**Q8. The read.** *"Does input 2 prove that the observations dated 14/9 and 20/9 in MD-SHELL-012's Actual Result were made on build `a17e3d0`?"*
- **Expected: no.** `session.md` records one build for the 18 September sitting. The cell holds visits
  on 14/9 and 20/9 as well, and nothing in the input says which build each ran on.
- **Scores 0 if:** the answer says the input proves it.
- **Expected outcome: tie or loss.** The rebuild does not change how `build` is filled; that is outside the two fixes and the move-up line. Reported in `results.md` whatever happens.
- **Scored by:** AI, twice per arm.

## Scoring

Each question scores 1 or 0 per arm. Nothing scores half.

**The rebuild fails its main claim if it scores 0 on any of Q1, Q3, Q4 or Q6**, whatever the total.
Those four are one question per feedback target, and a rebuild that misses one has not closed the gap the judges named.

**A question the original also scores 1 on is a tie, not a win**, and is reported as one.

**Exclusions.** A run that fails for a reason outside the folder (an API error, a timeout, no output) is
kept in the transcript and run once more, beside it. If it fails again it scores 0. A run that succeeded
cannot be re-run, and `harness/run.py` refuses to. No run is ever excluded for what it said.

**The answer key does not come from the rebuild.** Every count above was taken from the unchanged `cases.csv` files, and `harness/key.py` re-derives them the same way, without reading either arm.
