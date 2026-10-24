`reference/output-schema.md` states it. Line 68 reads: "The sheet name for this workbook's CSV exports is `Test Cases`." Lines 68–70 add that the reference workbook's test cases are on that sheet, and that the inputs in `inputs/` are exports of it, so their locators read `Test Cases!A96, K96, ...`.

Line 71 limits this to an input whose session record names no other workbook. Lines 73–75 say that if the session record names a different workbook, the sheet name is `NOT IN SOURCE` unless that record also states it.

ANSWER: reference/output-schema.md:68