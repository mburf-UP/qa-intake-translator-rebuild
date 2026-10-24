RUN COMPLETE: 9 records produced, and `records_out` equals `rows_recorded`.

The stop checks all passed:
- **Columns:** the CSV header at `inputs/input-2-2026-09-18/cases.csv:1` names all ten required columns exactly as `reference/output-schema.md:27-38` lists them, and it carries `_source_row`.
- **Build:** `inputs/input-2-2026-09-18/session.md:8` gives one build, `a17e3d0`. `session.md:13` says the file holds 9 rows, and I count 9.

## Coverage block

```
build                    a17e3d0                      (session.md:8)
rows_in                  9
rows_recorded            9
rows_not_recorded        0  (none; every row has a non-empty Actual Result)
records_out              9          ✓ equals rows_recorded

substantive_pass_rows    3, listed (Status = Pass, Actual Result over 40 chars, field-definitions.md:136):
                           MD-SHELL-014
                           MD-DARK-011
                           MD-DARK-014

multi_observation_rows   all nine, 46 spans in total:
                           MD-SIGN-014    2 spans
                           MD-SHELL-012   6 spans
                           MD-SHELL-014   4 spans
                           MD-SIGN-015    3 spans
                           MD-DARK-011    6 spans
                           MD-DARK-014    6 spans
                           MD-SEC-002     6 spans
                           MD-SEC-006     9 spans
                           MD-PERF-002    4 spans

evidence_not_found       none established. The evidence folder was not supplied to this run,
                         so all 32 references across the 9 rows are NOT CHECKED

refusal_counts           NOT IN SOURCE            17   (Severity empty ×7, Notes empty ×8,
                                                        Defect ID empty ×1, Evidence empty ×1)
                         IN SOURCE, UNRESOLVABLE   0
                         NOT APPLICABLE            0
```

## Records

In `observed`, `␣␣` marks two trailing spaces, as `examples.md:92-93` does. Double spaces inside a line are real double spaces. The CSV's doubled quote marks are unescaped to single quotes.

### 1 of 9

```
intake_id            INTAKE-2026-10-24-001
test_id              MD-SIGN-014
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Blocked
recorded_severity    NOT IN SOURCE
recorded_defect_id   OBS-173, OBS-185
expected_result      WHAT QA EXPECTS, SAID PLAINLY SO YOU ARE NOT HUNTING. Expected at steps 4-5: you land on /onboarding and are shown a form asking for an organisation name (and an optional ABN). Expected at step 8: only after submitting does the form disappear and a message appear telling you the platform is invitation-only and pointing you at hello@meridian.example. THAT SEQUENCE IS THE FINDING (OBS-173) - the right words, one step too late. PASS = you are told BEFORE being asked for business details. FAIL = you are asked first and told afterwards. ALSO A VALID RESULT: if you are never told at all, or you are shown a generic error rather than the waitlist message, record exactly what you saw - that would be worse than what QA predicted. AND IF AN ORGANISATION IS ACTUALLY CREATED, stop and tell QA immediately: that would mean the gate is not working, which is a different and more serious finding than this one.
observed             I created a new account - acct-d@ - and went to sign in, but it is no longer an option, there is no way to 'register' an account, you have to request to "Join the waitlist" per MD-SIGN-014-no-register-option
                     Retest 18/09: See the update to MD-SEC-006, I followed the steps to set up a new account (acct-d) and ended up at /onboarding?error=waitlist_only per MD-SEC-006-invite-onboard-waitlist
tester_notes         NOT IN SOURCE
evidence_cited       MD-SIGN-014-no-register-option         NOT CHECKED
                     MD-SEC-006-invite-onboard-waitlist     NOT CHECKED
observation_spans    line 1
                     line 2
source               Test Cases!A75, K75, L75, M75, N75 (empty), O75, P75, Q75, R75, S75 (empty)
                     intake_id assigned by this run; build from session.md
```

### 2 of 9

```
intake_id            INTAKE-2026-10-24-002
test_id              MD-SHELL-012
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Fail
recorded_severity    S2 Major
recorded_defect_id   OBS-201, OBS-213, OBS-214, OBS-215, OBS-216
expected_result      THIS CASE NOW ASKS TWO SEPARATE QUESTIONS AND WANTS BOTH ANSWERS RECORDED.

                     PART A PASSES if the strip under the search box is honest about what is happening and does not sit there saying nothing while results fail to arrive.

                     PART B IS THE ONE THAT MATTERS. Somewhere around the 30th Resend the status should turn 429 — that is the cap working, and it is GOOD. The finding is what the SEARCH PANEL says afterwards. It should tell you, in plain words, that you are searching too fast and to wait a moment. PASS = the panel says so. FAIL = the panel shows an empty result, a generic "could not search", or nothing — because that is a user being refused and not told, which is the whole reason this case exists.

                     IF THE STATUS NEVER TURNS 429 EVEN AFTER 40 RESENDS, that is a real and separate result — record it and stop. Do not keep clicking.

                     DO NOT record a Fail because the cap exists. The cap is the protection working.
observed             I did as many searches as I could - 48 searches - but never hit a cap.  I don't know how long that took, I was doing them quickly and immediately one after the other.  Fail based on no cap encountered.  I don't think I could test any faster than I did.
                     Restest 14/9: Completed 116 searches per the bar along the bottom of the screenshot, no limits kicked in: MD-SHELL-012-searches-no-limit.  Unless you can make sense of what is required here and what is a Pass vs a Fail I will mark this as a Pass.
                     Retest 20/9: on first test Part A got the words “some results may be missing” per MD-SHELL-012-some-docs-missing-20Sep. Typed “town” and got four instances of “Town Planning” per MD-SHELL-012-repeated-selections-20Sep, is that as intended?
                     Search on “build” returned results separated into “Documents” and “Actions” so that functionality looks to work well, 2 x “Projects” returned, how does the user know which one to select …? As for the 4 x Town Planning instances above, there’s no indication of where the results are indicating the search term was located.  MD-SHELL-012-docs-actions-20Sep
                     IMPORTANT: search results under a Free account are returning links to “Projects” and “Town Planning” which the test account, acct-b does not have access to, they are both Upgrade options. Search should only return what is accessible to the user, upgrading severity on this as it’s a bad user experience to search for something and be returned a reference that they don’t have access to.
                     Part B: the 429 and new search panel string looks to have worked as required “Could not search right now. Showing quick actions” (except it includes “Projects” still) per MD-SHELL-012-resend-limit-20Sep
tester_notes         NOT IN SOURCE
evidence_cited       MD-SHELL-012-searches-no-limit           NOT CHECKED
                     MD-SHELL-012-Request-Count-18Sep         NOT CHECKED   (Evidence column only)
                     MD-SHELL-012-some-docs-missing-20Sep     NOT CHECKED
                     MD-SHELL-012-repeated-selections-20Sep   NOT CHECKED
                     MD-SHELL-012-docs-actions-20Sep          NOT CHECKED
                     MD-SHELL-012-resend-limit-20Sep          NOT CHECKED
observation_spans    line 1
                     line 2
                     line 3
                     line 4
                     line 5
                     line 6
source               Test Cases!A94, K94, L94, M94, N94, O94, P94, Q94, R94, S94 (empty)
                     intake_id assigned by this run; build from session.md
```

### 3 of 9

```
intake_id            INTAKE-2026-10-24-003
test_id              MD-SHELL-014
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Pass
recorded_severity    S3 Minor
recorded_defect_id   NOT IN SOURCE
expected_result      PASS = you find NOTHING. No guide panel, no guide switch, no "md-guide" cookie. If ANY of the three turns up, record Fail and screenshot it: it means an unfinished feature has leaked into production, which is the single most serious class of problem this phase hunts for.
observed             Clicking on the user icon at the top right provides a "Help & support" option which when selected opens the "Support" page.␣␣
                     At the bottom right of each page is an "Ask" button which enables questions to be asked and provides answers/guidance.
                     There is nothing labelled "guide" or "guidance" though and nothing in the cookies with those words.
                     Marking as Partial as the Test has failed but the functionality in the website seems correct
tester_notes         QA note, 2026-09-18 (session 30): the Pass is correct and the sentence above it is older than it. This case is deliberately back-to-front - it asks you to confirm something is ABSENT, so finding nothing IS the pass. You found no guide panel, no guide switch and no "md-guide" cookie, which is all three. The "Marking as Partial" line dates from 15 August, when the case read as though finding a help surface was a failure; Help & support and the Ask button are separate features and were never what this case hunts for. Nothing of yours has been changed or re-graded.
evidence_cited       NOT IN SOURCE
observation_spans    line 1
                     line 2
                     line 3
                     line 4
source               Test Cases!A96, K96, L96, M96, N96, O96 (empty), P96 (empty), Q96, R96, S96
                     intake_id assigned by this run; build from session.md
```

### 4 of 9

```
intake_id            INTAKE-2026-10-24-004
test_id              MD-SIGN-015
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Partial
recorded_severity    NOT IN SOURCE
recorded_defect_id   NOT IN SOURCE
expected_result      PASS = every public entry point offers the waitlist and none of them offers account creation, so the door is shut consistently and honestly. FAIL = at least one surface still says "Sign up", "Create account" or "Get started" in a way that implies you can register - that is a dead end pointed at a stranger, and it is the same class of problem as OBS-181 (a link pointing at the old door). ALREADY KNOWN AND NOT A NEW FINDING: /signup itself IS the waitlist by design, and /send/signup redirecting is deliberate. WHAT QA WANTS FROM STEP 6: just where you land, because the redirect is documented as keeping its query string and that detail matters for OBS-181.
observed             5. For the "homepage" test, screenshotted both the top and bottom of the page as both have Sign In options.  Noticed that there's no heading to the second section on homepage about Meridian - see MD-SIGN-015-homepage-top-URL above the text "Meridian is where an Australian job lives..."  Set to Partial so that you wouldn't miss this extra result.
                     6. Redirected to /signup
                     (blank line)
                     Update 18/9: Checked arrow graphics, now fixed per MD-SIGN-015-Arrows-Fixed
tester_notes         NOT IN SOURCE
evidence_cited       MD-SIGN-015-signup-URL            NOT CHECKED   (Evidence column only)
                     MD-SIGN-015-signin-URL            NOT CHECKED   (Evidence column only)
                     MD-SIGN-015-pricing-URL           NOT CHECKED   (Evidence column only)
                     MD-SIGN-015-homepage-top-URL      NOT CHECKED
                     MD-SIGN-015-homepage-bottom-URL   NOT CHECKED   (Evidence column only)
                     MD-SIGN-015-Arrows-Fixed          NOT CHECKED
observation_spans    lines 1-1
                     lines 2-3
                     lines 4-4
source               Test Cases!A260, K260, L260, M260, N260 (empty), O260 (empty), P260, Q260, R260, S260 (empty)
                     intake_id assigned by this run; build from session.md
```

In record 4, `observed` line 3 is an empty line in the cell. The "(blank line)" text above only stands in for it.

### 5 of 9

```
intake_id            INTAKE-2026-10-24-005
test_id              MD-DARK-011
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Pass
recorded_severity    NOT IN SOURCE
recorded_defect_id   OBS-011, OBS-193
expected_result      All five refuse cleanly. None reveals whether the token format was close, and none renders partial content. Token-guessing feedback is an information leak.
observed             1. and 2. invalid link
                     3. 404
                     4. You have been invited page with "Create your account", the link which leads to "be ready for your next move" page per MD-DARK-011-invite.  Seems counterintuitive with an invite then a page that advises "we'll email you when access opens or *when you are invited*".  Also , the arrow graphics on the page seem overly large.
                     -- Update 14/9: the arrow graphics no longer appear on the page
                     -- Update 18/9: now presents  “Join your team   This invitation is no longer open …” page.  Will Pass
                     5. 404
tester_notes         NOT IN SOURCE
evidence_cited       MD-DARK-011-invite     NOT CHECKED
observation_spans    line 1
                     line 2
                     line 3
                     line 4
                     line 5
                     line 6
source               Test Cases!A282, K282, L282, M282, N282 (empty), O282, P282, Q282, R282, S282 (empty)
                     intake_id assigned by this run; build from session.md
```

### 6 of 9

```
intake_id            INTAKE-2026-10-24-006
test_id              MD-DARK-014
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Pass
recorded_severity    NOT IN SOURCE
recorded_defect_id   OBS-005, OBS-196
expected_result      PostHog requests ARE expected — that is now the correct baseline, not a defect. What must be true: the payload carries no personal information and no tokens (the source claims cookieless with a code-enforced no-PII schema), and PostHog is disclosed in the effective Privacy Policy. Anything identifying in a payload is S1. See MD-SEND-032 for the token-specific check, which is where the audit found a real problem.
observed             3. Not clear what you mean by "authed page" (marked as Partial accordingly) so logged in and went to Town Planning and a saved record.  Posthog result per MD-DARK-014-posthog
                     --Retest 18/09: see MD-DARK-014-posthog-18Sep
                     4. Intercom results per MD-DARK-014-intercom
                     --Retest 18/09: nothing for Intercom
                     5. nothing seen per MD-DARK-014-posthog-privacy
                     6. See MD-DARK-014-privacy-posthog1 and MD-DARK-014-privacy-posthog2
tester_notes         NOT IN SOURCE
evidence_cited       MD-DARK-014-posthog           NOT CHECKED
                     MD-DARK-014-intercom          NOT CHECKED
                     MD-DARK-014-posthog-privacy   NOT CHECKED
                     MD-DARK-014-privacy-posthog1  NOT CHECKED
                     MD-DARK-014-privacy-posthog2  NOT CHECKED
                     MD-DARK-014-posthog-18Sep     NOT CHECKED
observation_spans    line 1
                     line 2
                     line 3
                     line 4
                     line 5
                     line 6
source               Test Cases!A285, K285, L285, M285, N285 (empty), O285, P285, Q285, R285, S285 (empty)
                     intake_id assigned by this run; build from session.md
```

### 7 of 9

```
intake_id            INTAKE-2026-10-24-007
test_id              MD-SEC-002
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Partial
recorded_severity    NOT IN SOURCE
recorded_defect_id   OBS-189, OBS-191
expected_result      PASS = all ten routes clean. A violation means either the policy is too strict and something the page needs is being blocked, or something is loading that should not be - and the line names which. RECORD ALL TEN EVEN IF EVERY ONE IS CLEAN: a list of ten "clean" entries is the evidence; "no problems found" is not.
observed             The only one seen was "blocking" in Tracking Prevention per MD-SEC-002-tracking-prevention
                     5. no MFA on login for acct-pro@ or acct-main@
                     (blank line)
                     ALL CLEAN aside from the tracking prevention mentioned above.
                     (blank line)
                     Note: when testing the Properties page noted the Maps API error per MD-SEC-002-maps-api-error
                     Note: when testing the acct-main@ login noted the Intercom alert in Console per MD-SEC-002-acct-main-intercom-error
                     (blank line)
                     Update 18/09: Still no MFA prompt for either acct-main@ or acct-e@ per MD-SEC-002-no-mfa-18Sep, however also per the screenshot, no Intercom error any more.
tester_notes         NOT IN SOURCE
evidence_cited       MD-SEC-002-tracking-prevention          NOT CHECKED
                     MD-SEC-002-maps-api-error               NOT CHECKED
                     MD-SEC-002-acct-main-intercom-error     NOT CHECKED
                     MD-SEC-002-no-mfa-18Sep                 NOT CHECKED
observation_spans    lines 1-1
                     lines 2-3
                     lines 4-5
                     lines 6-6
                     lines 7-8
                     lines 9-9
source               Test Cases!A290, K290, L290, M290, N290 (empty), O290, P290, Q290, R290, S290 (empty)
                     intake_id assigned by this run; build from session.md
```

In record 7, `observed` is nine lines, and lines 3, 5 and 8 are empty lines in the cell. The "(blank line)" text above only stands in for them.

### 8 of 9

```
intake_id            INTAKE-2026-10-24-008
test_id              MD-SEC-006
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Partial
recorded_severity    NOT IN SOURCE
recorded_defect_id   OBS-190, OBS-192, OBS-194, OBS-200
expected_result      PASS = each of the five gives a human sentence and no programmer detail: no stack trace, no framework error page, no internal file path, no database table name. A branded "this link is not valid" page is a good answer. TWO EXPECTED RESULTS SO YOU DO NOT RAISE THEM AS NEW: (c) and (d) are known to return a branded "invalid link" page at a normal 200 status, which is deliberate. And (e) returning raw text saying something like invalid-input is acceptable for an address a customer would never type - what matters is that it names nothing internal.
observed             a. see MD-SEC-006-not-an-id
                     -- Update 14/9: now working correctly, the user receives the message: “Projects needs an upgrade  Your plan doesn't currently include Projects. Upgrade to create a project, lay out its tasks and payment milestones, and run the build from here.”
                     b. 404
                     c. This link isn't available
                     d. Join your team  This invitation is no longer open. It may have expired, been withdrawn, or already been used. Ask your team to send a new one if you still need access.␣␣
                     -- Update 14/9: first page the link lands on is as per MD-SEC-006-link-result, second is per MD-SEC-006-link-landing, still not a sign-in
                     -- Update 18/9: Create Your Account links to /signin which has at the bottom “New to Meridian? Create your account (as a link)” went through the process and created a new account (acct-d) successfully, and then ended up back on a list per MD-SEC-006-invite-onboard-waitlist so still not able to create an account.
                     e. on a free account: {"error":"forbidden","message":"an active paid or comped plan is required to view marketplace jobs"}, on acct-pro@ got a long string per MD-SEC-006-notanumber -- will mark Partial as not sure if this is expected or not.
                     -- Update 14/9: marketplace “notanumber” generated the JSON error: MD-SEC-006-marketplace-error
tester_notes         NOT IN SOURCE
evidence_cited       MD-SEC-006-not-an-id                 NOT CHECKED
                     MD-SEC-006-notanumber                NOT CHECKED
                     MD-SEC-006-link-result               NOT CHECKED
                     MD-SEC-006-link-landing              NOT CHECKED
                     MD-SEC-006-marketplace-error         NOT CHECKED   (no space after the comma before it in the Evidence cell)
                     MD-SEC-006-invite-onboard-waitlist   NOT CHECKED
observation_spans    line 1
                     line 2
                     line 3
                     line 4
                     line 5
                     line 6
                     line 7
                     line 8
                     line 9
source               Test Cases!A294, K294, L294, M294, N294 (empty), O294, P294, Q294, R294, S294 (empty)
                     intake_id assigned by this run; build from session.md
```

### 9 of 9

```
intake_id            INTAKE-2026-10-24-009
test_id              MD-PERF-002
build                a17e3d0
date_tested          2026-09-18
tester               TR1
recorded_status      Partial
recorded_severity    NOT IN SOURCE
recorded_defect_id   OBS-184, OBS-203
expected_result      PASS = no repeated error, and no warning appearing more than about five times. THE OUTPUT THAT MATTERS IS THE LIST OF DISTINCT MESSAGES, not a verdict - QA can judge which are harmless, and cannot judge a message it has not been shown. So err towards writing them all down. Already known and not new: OBS-018 (the legal-page preload warning) and the Intercom launcher line.
observed             2. The main error message prior to logging in was: POST
                     https://meridian.example/api/telemetry/collect
                     [HTTP/2 401  58ms], once logged in it stopped and XHR GET
                     https://meridian.example/api/marketplace/jobs
                     [HTTP/2 403  475ms] started reporting instead.
                     2b. Not reached
                     3. No counters seen and don’t know how to enable them (Firefox in Omarchy), have provided Requests output per MD-PERF-002-console-requests
                     (blank line)
                     I’m not sure if I have completed this properly, please advise
tester_notes         NOT IN SOURCE
evidence_cited       MD-PERF-002-console-requests   NOT CHECKED
observation_spans    lines 1-5
                     lines 6-6
                     lines 7-8
                     lines 9-9
source               Test Cases!A303, K303, L303, M303, N303 (empty), O303, P303, Q303, R303, S303 (empty)
                     intake_id assigned by this run; build from session.md
```

In record 9, `observed` is nine lines, and line 8 is an empty line in the cell. The "(blank line)" text above only stands in for it.

## What the folder or input cannot establish

- **Run date:** `intake_id` uses today's date, 2026-10-24, because `reference/output-schema.md:74` says `<run date>` and no file fixes one. The examples use 2026-09-26 (`examples.md:27`), which was their authoring date. The ordinals are the only part that matters for tracing.
- **Sheet name:** "Test Cases" comes from `examples.md:51`. The CSV can't confirm it (`reference/output-schema.md:87`).
- **Span boundaries:**
  - **Where my splits come from:** I split at the tester's own lines, dated updates and numbered items, per `reference/output-schema.md:109-111`. Blank lines stay with the line above.
  - **Where it's a judgement:** MD-SHELL-012 line 4 could be read as part of the 20/9 retest in line 3. `examples.md:54-56` treats it as separate and I followed that. If you disagree, merge lines 3-4.
- **Evidence presence:** nothing was looked up on disk, so every reference is `NOT CHECKED`. Test IDs in prose such as `MD-SEC-006` (row 75) and `MD-SEND-032` (row 285) are not evidence filenames and are not listed.
- **Discrepancy in `examples.md`:** line 264-265 attributes two of the 17 refusals to an empty Defect ID. The CSV has one empty Defect ID (row 96) and one empty Evidence cell (row 96). The total of 17 still matches my count.

## Where each answer comes from

| Answer | Source |
|---|---|
| Procedure and stop checks | `rules.md:7-17`, `reference/output-schema.md:161-169` |
| Record fields and refusals | `reference/output-schema.md:68-87`, `reference/output-schema.md:123-135` |
| Coverage block | `reference/output-schema.md:139-155` |
| Build `a17e3d0` | `inputs/input-2-2026-09-18/session.md:8` |
| Row data | `inputs/input-2-2026-09-18/cases.csv` lines 2-3 (row 75), 4-17 (94), 18-21 (96), 22-25 (260), 26-31 (282), 32-37 (285), 38-46 (290), 47-55 (294), 56-64 (303) |