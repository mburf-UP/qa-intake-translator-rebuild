# qa-intake-translator — rebuild

Comp #15 (The Rebuild). This is my comp #13 entry, the Translator, rebuilt against the judges' feedback
file and tested old against new.

**The line that drove it** (`feedback.md:51`): *"A check that counts the records actually present, so a
dropped record fails in a minute, and the stop output's fields written into reference/ so a stop is a
fixed shape."*

**The result:** on the committed runs, the rebuild scored 1 on five of the six questions aimed at the
feedback, against an original that scored 0 on all six. The first independent re-run, the only complete one,
gave four, because one question flipped. The rebuild failed the sixth, on the stop output, and under the rule we committed first
that means it fails its main claim. We left the rule as committed. `results.md` has the detail,
including the three ties, two independent checks (in the first, Q2 flipped), and the known limits.

## What is here

| Path | What it is | Commit |
|---|---|---|
| `original/` | The judged entry, exported unchanged from `ed18d22` | A `ce531a7` |
| `feedback.md` | The judges' feedback file, verbatim, SHA-256 `ee07ac0bb9a8479c867dab84a39553f20ca2c27b43a1068734e80141aa4995b0`. The judges hold the file they sent; it cannot be checked from this repo | A |
| `questions.md` | Eight questions from the feedback, with expected answers, scoring, loss and exclusion rules | B `9e73239` |
| `harness/`, `fixtures/` | The runner, the scorer, the answer key and two test inputs | B |
| `run-original/` | Raw runs against `original/`, and its scores | C `4b0623c` |
| `rebuild/` | The rebuild: identity, rules, examples, reference/, README, and `check.py` | D `59fdac5` |
| `run-rebuild/` | Raw runs against `rebuild/`, the same questions and prompts. Not run in order: see `results.md` | E `15bdb23` |
| `results.md` | What changed, question by question, including what tied, what lost, and what was left alone | F |

`questions.md` was committed before `rebuild/` existed, and nothing in A to E has been edited since its
commit. To see that for yourself:

```sh
git log --format='%h %cI %s' --name-status --reverse
```

## Check it yourself

Needs Python 3.9 or later and git. Nothing to install. Before publishing, `key.py`, `score.py`, `make_fixtures.py --check` and
`check.py` were run on Python 3.9.25 and 3.14.8 on Linux; no log of the 3.9.25 run ships, and the
independent checks had only 3.14.8. Not tested on macOS.

**The original is the judged commit, unchanged.** These print the same hash twice,
`dbc68c319ce37056d2aa58ff1d591a6ea68fbecf`: the first from this repo, the second from the judged repo.

```sh
git rev-parse HEAD:original
git clone -q https://github.com/mburf-UP/qa-intake-translator /tmp/judged-original
git -C /tmp/judged-original rev-parse 'ed18d22^{tree}'
```

**The marks, from the committed runs** (seconds, no AI). `score.py` rewrites `run-*/scores.json`;
for the committed runs the result is byte-identical, so `git status` stays clean:

```sh
python3 harness/key.py
python3 harness/score.py original
python3 harness/score.py rebuild
```

**The rebuild's new check**, on a committed output and on the judges' own deleted-record test:

```sh
cd rebuild
python3 check.py ../run-rebuild/T2/r1/result.md inputs/input-2-2026-09-18
python3 ../harness/mutate.py delete ../run-rebuild/T2/r1/result.md /tmp/deleted.txt
python3 check.py /tmp/deleted.txt inputs/input-2-2026-09-18
```

The first prints `PASS`; the second prints `MISSING MD-DARK-011 ...` and `FAIL`. Then `cd ..` back to
the top of the repo.

**Re-run the AI arms.** Needs Claude Code; use a separate clone, because this moves the committed runs
aside and writes new ones. From the top of that clone:

```sh
mv run-original run-original.committed
python3 harness/run.py original all
python3 harness/score.py original
```

The same with `rebuild` in place of `original`. `harness/run.py` names the model, `claude-sonnet-5-5`,
and every flag. It sets no effort level, so Claude Code's default applies; the committed runs used
Claude Code 2.1.309. Each committed run records the exact command, prompt and hashes it used. The committed
marks reproduce exactly from the committed transcripts. A fresh AI run may not: two runs per arm cannot
show how much marks vary, and Q7 already varies between runs.

## What you cannot check from this repo

Each is in `results.md` under "Known limits":

- that `feedback.md` is the file the judges sent;
- that the workbook's sheet is called `Test Cases`, because only CSV exports ship;
- the engagement claims carried from the judged entry: its method's size, backlog figures, the owner's
  permission and the de-identification;
- that the answer key is right by a second route: it comes from the same CSVs both arms read;
- the two independent checks: their reports and fresh transcripts are not here;
- the Python 3.9.25 run above.
