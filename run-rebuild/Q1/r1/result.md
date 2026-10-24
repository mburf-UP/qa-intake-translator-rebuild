`reference/output-schema.md` states it. Section 2.2, "The sheet name", says: "The sheet name for this workbook's CSV exports is `Test Cases`" (line 68). Lines 69–70 add that the inputs in `inputs/` are exports of that sheet, so their locators read `Test Cases!A96, K96, ...`.

Line 71 limits this to inputs whose session record names no other workbook. Lines 73–75 say that if a session record names a different workbook, the sheet name is `NOT IN SOURCE` unless that record also states it.

ANSWER: reference/output-schema.md:68