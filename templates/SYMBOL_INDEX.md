# SYMBOL INDEX

Authority SHA:
Generated/refreshed:
Status: CURRENT
Generated facts source: artifacts/SYMBOL_INDEX.generated.md

This is the semantic codebase table of contents.

Use machine-generated structural facts as input, then maintain responsibility,
authority, side effects, callers, and tests semantically.

Symbol name is the primary locator. Line numbers are navigation hints tied to the authority SHA above.

| File | Symbol | Kind | Lines@SHA | Responsibility | Reads/Writes | Called By | Tests |
|---|---|---|---|---|---|---|---|

## Refresh workflow

Run:

```bash
python scripts/generate_symbol_index.py
```

The generator prefers Universal Ctags for broad language coverage and falls back
to Python AST when Ctags is unavailable.

Generated output is structural evidence only. It must not invent semantic
responsibility or authority.

## Indexing rules
- Prioritize authority-bearing symbols.
- Include functions, classes, methods, API handlers, UI components, workers, state transitions, DB mutations, validators, and artifact readers/writers.
- Do not index every trivial helper.
- Bind line ranges to an exact SHA.
- Refresh structural facts after material source edits.
- Merge generated facts with human/agent-maintained semantic notes.
- Mark this file STALE if symbols or call ownership no longer match source.

## Example
| backend/promotion_service.py | promote_candidate | function | 120-240 | Candidate promotion authority | reads candidate, writes promotion | promotion API | test_promotion.py |
