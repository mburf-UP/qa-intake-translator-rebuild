# Session record — 2026-09-20

The build identifier is not in the worksheet. It is recorded here, in the session log, and it must be
supplied with the rows. See `reference/output-schema.md` §2.

| Field | Value |
|---|---|
| **Build identifier** | `e52b8c4` |
| Date | 2026-09-20 |
| Session log rows | 33, 34 |
| Tester | TR1 |
| Browser | Firefox 155.0.1 (64-bit); Chromium 152.0.7977.82 |
| Rows in `cases.csv` | 30 |

**Two sittings, one build.** The day ran as two separate sittings in two browsers, and the build under
test did not move between them. Because every row carries the same build, they are **one input** and the
run proceeds. Had the build moved, this would be input 3's situation — see `reference/output-schema.md` §6.
