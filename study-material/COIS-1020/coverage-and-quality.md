# COIS-1020H — Source-to-study coverage register

**Prepared from original source material:** eight instructor lecture PDFs (P1–P8) and eight lab instruction PDFs (Lab 1–8). PDF text extracts are generated in the adjacent `lectures/` and `labs/` directories with explicit **PDF page labels**. Code copied from slides or instructions may be visually clipped in extracted text; consult the original PDF for exact syntax and diagrams. Source links below point to committed files; they are not externally verified proof of assessment coverage.

## Course lecture → flashcard mapping

| Lecture PDF | Topic covered by this seed bank | Authored cards | Deck |
| --- | --- | ---: | --- |
| P1 Introduction | program/software, compiler, debugger, C# method and entry point, comments, identifiers | 13 | `COIS-1020::Introduction` |
| P2 Variables | data types and conversions, declaration, constants, formatting, IO, numeric operators | 16 | `COIS-1020::Variables and IO` |
| P3 Selection statements | pseudocode, if/else, nesting, Boolean AND/OR, short circuit, ranges, multi-alternative decisions | 14 | `COIS-1020::Selection` |
| P4 Loops | while/for/do, counted/sentinel loops, iteration boundaries, validation, integer division | 14 | `COIS-1020::Loops` |
| P5 Methods | signatures, arguments, local scope, return values, static/void and reuse | 14 | `COIS-1020::Methods` |
| P6 Advanced methods | value/ref/out parameters, recursion, method overloading, optional parameters | 15 | `COIS-1020::Advanced Methods` |
| P7 Arrays | indexing/length, traversal, linear and binary search, passing/returning arrays | 17 | `COIS-1020::Arrays` |
| P8 Classes and objects | classes/fields/objects, constructors, getters/setters, data hiding, this, arrays of objects | 20 | `COIS-1020::Classes and Objects` |
| **Total** | **Eight distinct source-based decks** | **123** |  |

Each JSON card has: stable `id`, short `front` and `back`, `course`/`deck`, topic/type tags, and a `source_ref` naming the exact lecture PDF and **PDF page**. The batch is reviewed automatically by the GitHub Authored cards workflow for schema and formatting; schema validation alone does **not** guarantee mathematical/semantic or visual fidelity.

## What *translation* means here

There are three separate outputs, each with a distinct completeness claim:

1. **Source transcription:** all eight lecture PDFs and Lab 1–8 PDFs transcribed into page-labelled Markdown for future source auditing. ✅
2. **Durable knowledge cards:** a deliberately selective 123-card seed covers core definitions/rules/recognition from all eight lecture PDFs. This is **not** a claim that every slide or anecdote should become a flashcard. ✅ Seed created; publication to production must be verified separately.
3. **Procedural competence:** the independent Lab 1–8 checklist and eight new practice scenarios define exact pass/fail evidence. Student execution is still outstanding. ✅ Specifications created; proficiency not yet established.

## Precision and remaining audit

- Every card's source reference should be checked against the original PDF **page image** (especially complex code examples and tables) before declaring a source-perfect final edition. Automated text extraction can omit diagrams, clip long code lines, or reorder columns.
- Some instructor slide examples contain syntax/typographical mistakes and older C# conventions. Never silently treat a questionable example as canonical production code; cross-check intended conceptual rule and avoid copying broken syntax into cards.
- Flashcards intentionally exclude graded lab solutions, assignment-specific completion code, and long multi-step implementation tasks. Those belong in independent programming practice.
- The 123-card set does not cover every fine-grained example or potential assessment question. A separate audit would be needed to assert exhaustive coverage (one row per slide/learning outcome with confirmed card or deliberate exclusion).
- Lab 9 and Lab 10 official handouts are not yet in the source directory and are **not** asserted covered.
- Syllabus Test 2 date: **Nov 24, 2026**. Verify the exact assessed topics from instructor announcements; do not presume everything in P8 is tested.

## Learning-mode metric

**Anki retention:** first-attempt recall target >=95% over at least 20 distinct recent reviews in a seven-day window, computed per the app's current metric. This is a *target*, not achieved just because cards were created.

**C# competence:** independently recreate Lab 1–8 and/or G1–G8 from a blank project, pass all supplied test cases, correctly explain scope/control flow/edge cases, and record independent later retests. A flashcard score does not prove programming mastery.

## Due-date-first sequence

- **Nov 22:** review cards from methods, advanced methods, loops, arrays; independently attempt at least one representative method and one array lab.
- **Nov 23:** independently reproduce prioritized Lab 5–8 methods/arrays and run G5–G8 where permitted; record any unsupported subjects and failed cases.
- **Nov 24:** complete timed mock, check last minute Test 2 announcements, and revisit only errors and due cards.
- **Nov 25 onward:** close the rest of Lab 1–8 coverage, continue spaced recall and source-image audit without manufacturing review-history success.

These are suggested self-study execution checkpoints, not instructor-assigned deadlines.
