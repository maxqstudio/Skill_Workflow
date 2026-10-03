<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Cross-language analyzer architecture

Skill Workflow separates analyzer mechanics from governance meaning. A language analyzer may contribute machine-observable facts, but the governance layer decides acceptance from explicit evidence and must never infer unsupported runtime behavior.

## Contract

Every structural analyzer exposes the same language-independent surface:

- a stable `analyzer_id`;
- the file extensions it claims;
- a declared semantic level;
- a proof status;
- optional normalized facts;
- optional sequence nodes and edges;
- parse failures and limitations;
- dynamic behavior status, which remains `NOT_PROVEN` for static analyzers.

The shared contract is implemented in `scripts/analyzer_contract.py`. Consumers should depend on the normalized result contract rather than a parser-specific implementation.

## Current analyzers

| Analyzer | Scope | Evidence strength |
| --- | --- | --- |
| `python_facts` | Python symbols, decorated HTTP routes, call tokens | Static AST evidence with explicit limitations |
| `python_sequence` | Python sequence participants and conservatively resolved project calls | Static AST evidence with explicit limitations |
| `js_ts_http_sequence` | JS/TS module-level literal `fetch` / `axios` HTTP edges | Static HTTP-module evidence only |
| `generic_inventory` | Source files not claimed by the active analyzer set | Inventory only; semantic structure remains `NOT_PROVEN` |

The Python fact and sequence adapters intentionally preserve the accepted pre-SW2-06 output contracts. SW2-06 adds a common interface; it does not silently redefine previously accepted evidence.

## Fail-safe fallback

Unsupported source files are not ignored. They are listed by `generic_inventory`, but that fallback is forbidden from emitting semantic symbols, routes, calls, sequence participants, or edges. If inventory-only code attempts to emit semantic evidence, the analyzer contract fails.

This makes the fallback useful for completeness without turning extension detection into false understanding.

## Dynamic behavior boundary

Static analysis does not prove:

- dynamic dispatch;
- dependency injection;
- reflection;
- callbacks or event wiring that cannot be resolved statically;
- framework magic not visible in source;
- runtime ordering;
- unresolved cross-language calls.

These remain `NOT_PROVEN` unless stronger runtime or semantic evidence is added. An analyzer is not allowed to promote dynamic behavior above `NOT_PROVEN` through the static contract.

## Adding another language

A new analyzer should:

1. implement the shared structural analyzer contract;
2. claim only extensions it actually understands;
3. emit only facts supported by deterministic evidence;
4. record parse failures and limitations explicitly;
5. add positive and negative regression fixtures;
6. preserve generic fallback for unsupported or unresolved behavior;
7. pass cross-platform governance acceptance before its claims can become authoritative.

Adding a parser is not, by itself, proof of runtime behavior. The evidence boundary must remain explicit.
