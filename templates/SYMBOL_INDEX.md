# SYMBOL INDEX

Authority SHA:
Generated/refreshed:
Status: CURRENT

This is the codebase table of contents.

Symbol name is the primary locator. Line numbers are navigation hints tied to the authority SHA above.

| File | Symbol | Kind | Lines@SHA | Responsibility | Reads/Writes | Called By | Tests |
|---|---|---|---|---|---|---|---|

## Indexing rules
- Prioritize authority-bearing symbols.
- Include functions, classes, methods, API handlers, UI components, workers, state transitions, DB mutations, validators, and artifact readers/writers.
- Do not index every trivial helper.
- Bind line ranges to an exact SHA.
- Refresh ranges after material source edits.
- Prefer machine-generated structure plus human-maintained semantic notes.
- Mark this file STALE if symbols or call ownership no longer match source.

## Example
| backend/promotion_service.py | promote_candidate | function | 120-240 | Candidate promotion authority | reads candidate, writes promotion | promotion API | test_promotion.py |
