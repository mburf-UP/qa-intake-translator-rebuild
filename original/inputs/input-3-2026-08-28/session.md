# Session record — 2026-08-28

The build identifier is not in the worksheet. It is recorded here, in the session log, and it must be
supplied with the rows. See `reference/output-schema.md` §2.

| Field | Value |
|---|---|
| **Build identifier** | **two: `b41c07e` and `c98f215`** |
| Date | 2026-08-28 |
| Session log rows | 18, 19 |
| Tester | TR1 |
| Browser | Chrome 151.0.4129.107 |
| Rows in `cases.csv` | 18 |

## This input stops the run, and that is why it is here

A new build landed mid-day and the same test range was re-run against it. The session log records two
sittings, **two different builds**, and the worksheet holds one row per test case — so the 18 rows in
`cases.csv` describe two different versions of the product with nothing in the row saying which.

`reference/output-schema.md` §6 names this exactly: *rows from more than one build in one input*. The
run produces **no records at all** and says which condition fired.

**This is not a defect in the input and it is not an edge case invented for the competition.** It is an
ordinary Friday in a live engagement, and the engagement's own method states that results from two
different builds cannot be compared. A record that cannot name its build is not evidence of anything.

The remedy is in the schema: split the input and run twice. Doing that needs a fact this translator does
not have — which sitting each row belongs to — so it is the operator's job, not the translator's.
