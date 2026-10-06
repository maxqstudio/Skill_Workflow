# Skill Workflow

Strict, deterministic project governance and handoff for long-running software work across humans and coding agents.

**Stable release:** `v2.1.0`
**License:** MIT

Skill Workflow keeps project authority, current phase, architecture, workflows, evidence, and legal next actions explicit inside the repository. Generated documentation is a projection of governed sources—not a second source of truth.

## Why Skill Workflow

Use Skill Workflow when a new developer or coding agent should be able to continue a project without reconstructing intent from old chats.

It provides:

- LITE, STANDARD, and STRICT governance profiles;
- deterministic Project Truth for STANDARD/STRICT projects;
- exact tested-SHA acceptance and fail-closed evidence rules;
- `develop`, `verify`, and `finalize` execution modes;
- machine-backed sequence evidence with bounded human views;
- cross-document, handoff, and Human Comprehension gates;
- project-local vendored governance tools for portable execution.

## Quick start

Install with the open `skills` CLI:

```bash
npx skills add maxqstudio/Skill_Workflow
```

For a specific agent, for example Codex:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -y
```

Then follow [Installation](docs/handbook/getting-started/installation.md) and [Repository adoption](docs/handbook/getting-started/adoption.md). Every governed project also keeps a mandatory source-authored [`AGENTS.md`](AGENTS.md) at repository root as the coding-agent operating contract.

## How it works

```text
PROJECT_PROFILE.yaml + .workflow/*.json + source + tests/runtime evidence
                            |
                            v
              deterministic compiler/validators
                            |
                            v
             generated Project Truth + evidence
                            |
                            v
                 exact-head final acceptance
```

Source code owns implementation facts. `.workflow/*.json` owns declared governance/semantic intent. Tests and runtime evidence own behavioral proof. Generated Markdown makes those facts readable and traceable.

## Documentation

| Goal | Start here |
| --- | --- |
| Install the skill | [Installation](docs/handbook/getting-started/installation.md) |
| Adopt it in a repository | [Repository adoption](docs/handbook/getting-started/adoption.md) |
| Understand the governance model | [Governance model](docs/handbook/concepts/governance-model.md) |
| Understand the documentation layers | [Documentation system](docs/handbook/reference/documentation-system.md) |
| Diagnose failures | [Troubleshooting](docs/handbook/guides/troubleshooting.md) |
| Use commands directly | [Command reference](docs/handbook/reference/commands.md) |
| Inspect release behavior | [Release process](docs/handbook/reference/release-process.md) |

The full entry points are the [documentation index](docs/README.md) and [handbook](docs/handbook/README.md).

## Supported agents

The `skills` CLI can target Codex, Claude Code, Cursor, Gemini CLI, GitHub Copilot, OpenCode, Qwen Code, Roo Code, Windsurf, Cline, and other supported agents. Agent-specific examples live in the [installation guide](docs/handbook/getting-started/installation.md).

## Project state and governance

This repository dogfoods Skill Workflow. The accepted stable V2.1 release is `v2.1.0`; subsequent governance work continues through explicit roadmap/acceptance boundaries.

Maintainers can inspect the generated [system overview](docs/SYSTEM_OVERVIEW.md), [current state](docs/CURRENT_STATE.md), [roadmap](docs/ROADMAP.md), [project manifest](docs/PROJECT_MANIFEST.md), and [Project Truth ledger](docs/PROJECT_TRUTH_SYNC.md). Those files are generated evidence/navigation for this repository, not the public product manual.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Skill Workflow is distributed under the [MIT License](LICENSE).

## Support

Optional support is available through [Saweria](https://saweria.co/maxq) or [PayPal](https://paypal.me/JacksonJackson1501). Support does not change access to the public repository or its features.
