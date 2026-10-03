#!/usr/bin/env python3
"""Regression tests for bounded generated engineering-document presentation."""

from __future__ import annotations

from generate_project_docs import render_symbols


def main() -> int:
    facts = {
        "source_digest": "fixture-digest",
        "python_symbols": [
            {"file": "scripts/a.py", "symbol": "Alpha", "kind": "class", "line_start": 10, "line_end": 20},
            {"file": "scripts/a.py", "symbol": "Alpha.run", "kind": "method", "line_start": 12, "line_end": 18},
            {"file": "scripts/b.py", "symbol": "main", "kind": "function", "line_start": 3, "line_end": 8},
        ],
        "coverage": {"limitations": ["fixture limitation"]},
    }
    rendered = render_symbols(facts)

    assert "## File summary" in rendered
    assert "## Detailed symbols" in rendered
    assert "| scripts/a.py | 2 | 1 | 0 | 1 |" in rendered
    assert "| scripts/b.py | 1 | 0 | 1 | 0 |" in rendered
    assert rendered.count("<details>") == 2
    assert rendered.count("</details>") == 2
    for symbol in ("Alpha", "Alpha.run", "main"):
        assert symbol in rendered
    assert "Observed Python symbol" not in rendered
    assert "| Responsibility | Reads/Writes | Called By | Tests |" not in rendered
    assert "fixture limitation" in rendered

    print("SYMBOL_SUMMARY_PRESENT=PASS")
    print("SYMBOL_DETAIL_RETENTION=PASS")
    print("SYMBOL_COLLAPSIBLE_PRESENTATION=PASS")
    print("EMPTY_SEMANTIC_COLUMNS_REMOVED=PASS")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
