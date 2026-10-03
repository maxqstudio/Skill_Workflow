# Skill Workflow

Strict, deterministic project handoff and governance for long-running software work across humans and coding agents.

Skill Workflow gives a repository an explicit map of authority, current phase, architecture, workflows, code ownership, evidence, and legal next actions. It reduces context loss **without turning documentation into a second source of truth**.

## Why Skill Workflow

Use it when a new room, agent, or developer should not have to reconstruct a project from old chats and a blind source scan.

It provides:

- explicit project and roadmap authority;
- LITE, STANDARD, and STRICT governance profiles;
- deterministic Project Truth documentation for STANDARD/STRICT projects;
- exact tested-SHA and fail-closed acceptance rules;
- develop / verify / finalize execution modes;
- machine-backed sequence evidence plus bounded human sequence views;
- cross-document, handoff, and Human Comprehension gates;
- project-local vendored governance tools for portability.

## Quick start

Install with the open `skills` CLI:

```bash
npx skills add maxqstudio/Skill_Workflow
```

For a specific agent, for example Codex:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -y
```

See the [installation guide](docs/handbook/getting-started/installation.md) for global installs, multiple agents, and supported agent examples. Then use the [adoption guide](docs/handbook/getting-started/adoption.md) to add Project Truth governance to a repository.

## How it works

```text
PROJECT_PROFILE.yaml
+ .workflow/*.json
+ source facts
+ tests/runtime evidence
        ↓
deterministic compiler + validators
        ↓
generated Project Truth + acceptance evidence
        ↓
final exact-head acceptance
```

Generated Markdown is a projection. Source code, structured project authority, and test/runtime evidence remain the underlying truth.

## Documentation

Start at the [public documentation index](docs/README.md) or the [handbook](docs/handbook/README.md).

- [Getting started](docs/handbook/getting-started/adoption.md)
- [Governance model](docs/handbook/concepts/governance-model.md)
- [Troubleshooting](docs/handbook/guides/troubleshooting.md)
- [Command reference](docs/handbook/reference/commands.md)
- [Validation architecture](docs/handbook/architecture/validation-engine.md)
- [Sequence contracts and Sequence V2](docs/handbook/sequence/README.md)

## Supported agents

The `skills` CLI can target Codex, Claude Code, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Qwen Code, Roo Code, Windsurf, Cline, and other supported agents. Agent-specific examples live in the [installation guide](docs/handbook/getting-started/installation.md).

## Project state and governance

This repository dogfoods Skill Workflow. Maintainers and auditors can inspect the generated [current state](docs/CURRENT_STATE.md), [roadmap](docs/ROADMAP.md), and [Project Truth ledger](docs/PROJECT_TRUTH_SYNC.md).

Those generated governance files are evidence/navigation for this repository; the public handbook above is the product documentation entry point.

## Support

If Skill Workflow is useful for your projects, optional support is available through [Saweria](https://saweria.co/maxq) or [PayPal](https://paypal.me/JacksonJackson1501). Access to the public repository and its features is not affected by support.
