"""Runs one AI step against one arm, and records everything about the run.

    python3 harness/run.py ARM STEP RUN      e.g.  python3 harness/run.py original T2 1
    python3 harness/run.py ARM all           every step in prompts.json, runs 1 and 2, in order
    python3 harness/run.py ARM STEP 1-retry  the one permitted re-run of a run that failed outside the
                                             folder (questions.md, Exclusions); the failed run is kept

ARM is `original` or `rebuild`. The step's prompt is taken from harness/prompts.json, unchanged.

The arm's folder is copied to a new temporary directory and the session runs there, so it cannot see
feedback.md, questions.md, the other arm or any earlier run. A fixture, if the step has one, is copied
to `test-input/<name>/` inside that copy. The session can read files and nothing else.
`--restricted` confines those file tools to the session's own folder and ignores every settings file;
`--strict-mcp-config` and `--safe-mode` load no MCP server, CLAUDE.md, skill, plugin or hook; and
`--permission-mode dontAsk` refuses anything that would need approval. Tested before commit B on Claude
Code 2.1.309: a read of a file outside the folder, and a listing outside it, were both refused.

Writes run-<ARM>/<STEP>/r<RUN>/ and refuses to overwrite one that exists: a run is never redone in place.
"""
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

from common import ROOT, sha256_bytes, tree_hashes

PROMPTS = json.loads((ROOT / "harness" / "prompts.json").read_text(encoding="utf-8"))
TIMEOUT = 1800


def command(prompt):
    return [
        "claude", "-p",
        "--restricted", "--strict-mcp-config", "--safe-mode", "--permission-mode", "dontAsk",
        "--model", PROMPTS["model"], "--tools", "Read,Glob,Grep",
        "--no-session-persistence", "--output-format", "json",
        prompt,
    ]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def claude_version():
    try:
        return subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    except OSError as exc:
        return "unavailable: %s" % exc


def run(arm, step, n):
    spec = PROMPTS["steps"][step]
    out = ROOT / ("run-" + arm) / step / ("r%s" % n)
    if out.exists():
        print("exists, not overwritten: %s" % out.relative_to(ROOT))
        return 0
    arm_dir = ROOT / arm
    if not arm_dir.is_dir():
        raise SystemExit("no such arm folder: %s" % arm)

    # Both arms must read the same input bytes as the judged original.
    orig_inputs = tree_hashes(ROOT / "original" / "inputs")
    arm_inputs = tree_hashes(arm_dir / "inputs")
    if orig_inputs != arm_inputs:
        raise SystemExit("%s/inputs differs from original/inputs; refusing to run" % arm)

    prompt = PROMPTS["preamble"] + "\n\n" + spec["prompt"]
    work = tempfile.mkdtemp(prefix="arm-")
    folder = shutil.copytree(arm_dir, work + "/folder")
    if spec["fixture"]:
        shutil.copytree(ROOT / "fixtures" / spec["fixture"], folder + "/test-input/" + spec["fixture"])
    given = tree_hashes(folder)

    argv = command(prompt)
    started = now()
    try:
        proc = subprocess.run(argv, cwd=folder, capture_output=True, text=True, timeout=TIMEOUT)
        code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        code, stdout, stderr = "timeout", exc.stdout or "", exc.stderr or ""
        stdout = stdout if isinstance(stdout, str) else stdout.decode("utf-8", "replace")
        stderr = stderr if isinstance(stderr, str) else stderr.decode("utf-8", "replace")
    finished = now()
    shutil.rmtree(work)

    try:
        data = json.loads(stdout)
    except ValueError:
        data = {}
    result = data.get("result") if isinstance(data, dict) else None

    out.mkdir(parents=True)
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")
    (out / "stdout.json").write_text(stdout, encoding="utf-8")
    (out / "stderr.txt").write_text(stderr, encoding="utf-8")
    (out / "result.md").write_text(result if isinstance(result, str) else "", encoding="utf-8")
    meta = {
        "arm": arm, "step": step, "run": n,
        "argv": argv, "cwd": "<temporary copy of %s/>" % arm,
        "started_utc": started, "finished_utc": finished, "exit_code": code,
        "claude_version": claude_version(), "requested_model": PROMPTS["model"],
        "models_used": sorted((data.get("modelUsage") or {}).keys()) if isinstance(data, dict) else [],
        "permission_denials": data.get("permission_denials") if isinstance(data, dict) else None,
        "is_error": data.get("is_error") if isinstance(data, dict) else None,
        "cost_usd": data.get("total_cost_usd") if isinstance(data, dict) else None,
        "python": platform.python_version(), "platform": platform.platform(),
        "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
        "files_given_sha256": given,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    ok = code == 0 and isinstance(result, str) and result.strip() and not meta["is_error"]
    print("%s %s r%s: %s" % (arm, step, n, "ok" if ok else "FAILED (kept; see %s)" % out.relative_to(ROOT)))
    return 0 if ok else 1


def main(argv):
    if len(argv) == 2 and argv[1] == "all":
        failed = 0
        for step in PROMPTS["steps"]:
            for n in (1, 2):
                failed += run(argv[0], step, n)
        return 1 if failed else 0
    if len(argv) == 3 and argv[1] in PROMPTS["steps"] and argv[2] in ("1", "2", "1-retry", "2-retry"):
        if argv[2].endswith("-retry"):
            first = ROOT / ("run-" + argv[0]) / argv[1] / ("r" + argv[2][0])
            if not (first / "meta.json").is_file():
                raise SystemExit("a retry needs the failed run it replaces")
            meta = json.loads((first / "meta.json").read_text(encoding="utf-8"))
            text = (first / "result.md").read_text(encoding="utf-8")
            if meta.get("exit_code") == 0 and not meta.get("is_error") and text.strip():
                raise SystemExit("that run succeeded; questions.md allows a retry only after a failure")
        return run(argv[0], argv[1], argv[2])
    print(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
