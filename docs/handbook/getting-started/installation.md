<!-- PUBLIC PRODUCT DOCUMENTATION - SOURCE-AUTHORED -->

# Installation

Skill Workflow is distributed through the open `skills` CLI.

## Default project-local install

```bash
npx skills add maxqstudio/Skill_Workflow
```

A project-local install is the safest default when the skill should travel with one repository.

## Agent-specific install

Use `-a` to select an agent:

```bash
npx skills add maxqstudio/Skill_Workflow -a codex -y
npx skills add maxqstudio/Skill_Workflow -a claude-code -y
npx skills add maxqstudio/Skill_Workflow -a cursor -y
npx skills add maxqstudio/Skill_Workflow -a gemini-cli -y
npx skills add maxqstudio/Skill_Workflow -a github-copilot -y
npx skills add maxqstudio/Skill_Workflow -a opencode -y
npx skills add maxqstudio/Skill_Workflow -a qwen-code -y
npx skills add maxqstudio/Skill_Workflow -a roo-code -y
npx skills add maxqstudio/Skill_Workflow -a windsurf -y
npx skills add maxqstudio/Skill_Workflow -a cline -y
```

Use `-g` for a global install. Multiple `-a` flags can install the skill for several agents in one command.

## Multi-agent example

```bash
npx skills add maxqstudio/Skill_Workflow \
  -a codex \
  -a claude-code \
  -a cursor \
  -a gemini-cli \
  -a github-copilot \
  -a opencode \
  -y
```

To install all skills in this repository for all supported/detected agents:

```bash
npx skills add maxqstudio/Skill_Workflow --all
```

Update installed skills later with:

```bash
npx skills update
```

## What is canonical

`SKILL.md` is the canonical eager skill contract. Detailed normative operating rules are bundled under root `references/` and are loaded through deterministic one-level links from `SKILL.md`; public handbook pages are explanatory and do not replace those bundled references. Project-local Project Truth tools are vendored into `.workflow/tools/` when the initializer is used, so governed projects do not depend on a particular agent's global installation path.

Continue with [repository adoption](adoption.md).
