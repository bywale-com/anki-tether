# COIS-1020H — Eight original, independent practice labs

These exercises are *new, ungraded self-study problems*, not Trent's official Lab 1–8 instructions, answers, or code to submit for credit. Use them only if permitted under the course's AI policy. They deliberately test the same underlying programming skills in different contexts. Each is to be written **without AI or example solutions**. Run the cases and record pass/fail. If the instructor's rule prohibits using AI-generated study materials, use only the official handouts and ask for clarification first.

## G1 — Console interface and debugging

**Brief:** From an empty C# Console App, build a small welcome screen for a fictitious library kiosk. Print two distinct lines, clear the console before printing, and accept one final input line before exiting. Locate the entry point and explain what your IDE debugger starts.

**Acceptance:** Starts cleanly via VS Code; output contains both lines in order; no unintended output after clearing; you can explain source-file name vs project name. **Evidence:** screenshot and independent explanation; no code template supplied.

## G2 — Variable typing, currency, fractional values

**Brief:** A bicycle-repair shop needs a quote: input customer name, fractional hours of work, hourly labor rate, and fixed parts cost. Print itemized labor, parts, subtotal, and a final total after a *user-entered* discount fraction from 0 to 1. Use currency formatting.

**Checks:** Name Sam, hours 2.5, rate 40.00, parts 15.00, discount 0.10 → labor 100.00, pre-discount 115.00, final 103.50. Also test 0 hours, 0 discount, 1 discount and a fractional hours input that would fail integer-only conversion. Explain type selection and validation assumptions.

## G3 — Branch recognition and exact boundaries

**Brief:** Compute entry fees for a museum based on age: ages below 12 are $5, ages 12 through 64 inclusive are $12, ages 65+ are $7; negative ages must be rejected. Add a flat $2 booking charge *only for valid purchases*. Output a currency-formatted fee.

**Checks:** ages -1,0,11,12,64,65,100 produce rejection, $7,$7,$14,$14,$9,$9. Identify exactly which comparison operators establish the boundaries.

## G4 — Sentinel loop and zero-count protection

**Brief:** Read nonnegative minute counts for exercise sessions until -1. Reject values under -1 or above 300 and reprompt without adding them. Report count, total, mean to two decimals, and counts above/below 30 minutes. Treat 30 as not above.

**Checks:** -1 → zero count, total 0, average 0.00; 10,40,30,-1 → count 3, total 80, mean 26.67, above 1, not-above 2; 301,20,-1 → exactly one accepted value. Explain how the sentinel avoids contaminating the sum.

## G5 — Method signatures, scope and return values

**Brief:** Implement a program with a method `ConvertScoreToBand(int score)` returning a character. Bands: 0–49 F, 50–59 D, 60–74 C, 75–84 B, 85–100 A. Reject score outside 0–100 *before calling* the method. Put the band logic only inside the method. Explain which variables are visible in the caller vs callee and trace the return value.

**Checks:** -1 invalid; 0 F; 49 F; 50 D; 59 D; 60 C; 74 C; 75 B; 84 B; 85 A; 100 A; 101 invalid. Also create a second experimental version using a `ref char` output parameter, then compare the calls and return types.

## G6 — Value, ref, validation, and a calculation pipeline

**Brief:** A freelancer invoices hours at an hourly rate. Write three methods: calculate ordinary gross as a return value, add a weekend premium for hours over 30, and calculate net into a `ref double` parameter after a user-supplied platform fee. Validate hours/rate nonnegative and fee between 0–1. Ensure premium is included before the fee deduction.

**Checks:** hours 30, rate $20, fee 0.10 → gross $600, net $540; hours 34, rate $20, fee 0.10 and premium half-rate on four excess hours → gross $720, net $648; hours 0 → gross/net 0. Explain why changing a non-`ref` numeric parameter does not update the caller's variable.

## G7 — Array filling, reverse output and search

**Brief:** Accept between 0 and 8 book titles into a fixed-capacity `string[]`. Implement separate methods to fill, print in insertion order, print in reverse using your own loop, and return the first matching title's index or -1. Do not use `Array.Reverse` or a built-in search method.

**Checks:** zero items → no entries printed and searching returns -1; four titles [A,B,C,D] → reverse D,C,B,A; search C → index 2; search Z → -1; invalid lengths -1 and 9 must be rejected and reprompted. State why capacity differs from populated count.

## G8 — Array aggregation with empty and negative inputs

**Brief:** Read 0–12 integer temperature readings and implement separate methods returning mean, minimum and maximum. No LINQ or built-in `Min`, `Max`, `Average`, or sorting. For zero readings return average/min/max of 0 by explicit design. Use a loop to compute statistics.

**Checks:** [3,-2,8,1] → mean 2.50, min -2, max 8; [-8,-4,-10] → mean -7.33, min -10, max -4; [0] → all zero; [] → all zero. Explain the common bug caused by initializing the maximum to 0 when all input values are negative.

## Evidence and self-marking

For each generated lab, save: (a) source file/project link; (b) a screenshot or console transcript of the supplied test cases; (c) pass/fail per case; (d) whether you wrote it from a blank project without hints; (e) a short explanation of methods/types/control flow; (f) the date/results of a later independent retry if you initially failed.

**Competency target:** 100% of specified cases pass without external guidance, and you can correctly explain each key choice and a failure mode. Use first-attempt and later-retest columns separately; do not inflate first-attempt scores through debugging help.

**Recommended ordering before Test 2:** G5–G8 first (methods, ref, arrays), then G4 and G3. G1 and G2 are foundational repair work.

**Submission boundary:** These are study-only exercises, not replacements for official labs or permitted content for graded submissions. A no-AI course rule takes precedence over this generated practice set.
