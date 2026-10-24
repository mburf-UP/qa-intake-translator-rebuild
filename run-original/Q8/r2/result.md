**No. Input 2 doesn't prove the 14/9 and 20/9 observations were made on `a17e3d0`.**

- **What the build covers:** `inputs/input-2-2026-09-18/session.md:8` gives the build identifier as `a17e3d0`. The same file gives the date as 2026-09-18 (`session.md:9`) and describes "One short sitting, one build" (`session.md:15`). So the build is tied to the 18/9 sitting only.
- **Where the dates appear:** The MD-SHELL-012 Actual Result has "Restest 14/9" at `cases.csv:13` and "Retest 20/9" at `cases.csv:14`. Part B at `cases.csv:17` also seems to belong to the 20/9 retest. The row's Date Tested is 2026-09-18 (`cases.csv:17`).
- **14/9:** This is four days before the session. Nothing in the folder says which build was live then.
- **20/9:** This is two days after the session date, so the 18/9 build record can't cover it. Nothing in the folder says which build was live on that date either.
- **`examples.md`:** It states "Build: `a17e3d0`" for this row (`examples.md:20`). It is a derived document that takes the build from `session.md`, so it adds no evidence for the other dates.

The folder doesn't say what build was running on 14/9 or 20/9. The worksheet has no build column (`session.md:3`).

ANSWER: NO