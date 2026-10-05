from __future__ import annotations

import ast
import importlib
import importlib.util
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
GENERATOR = SCRIPTS / "generate_project_docs.py"
sys.path.insert(0, str(SCRIPTS))

GROUPS = {
    "project_truth_projection_state": [
        "render_system_overview", "render_project_manifest", "render_current_state",
        "render_roadmap", "render_authority", "render_architecture",
        "render_workflows", "render_sequence",
    ],
    "project_truth_projection_code": [
        "render_modules", "render_symbols", "render_flows", "render_acceptance",
    ],
    "project_truth_projection_governance": [
        "render_doc_sync", "render_truth", "render_decisions", "render_defects",
        "render_changelog", "render_glossary",
    ],
    "project_truth_projection_contracts": [
        "render_api", "render_data", "render_ui", "render_runbook",
    ],
}
COMMON = [
    "clean", "cell", "bullets", "normalize_markdown", "generated_header",
    "claim_backlink_comment", "auth_lookup", "wanted_doc_names",
]
DOC_MAP = {
    "SYSTEM_OVERVIEW.md": "render_system_overview",
    "PROJECT_MANIFEST.md": "render_project_manifest",
    "CURRENT_STATE.md": "render_current_state",
    "ROADMAP.md": "render_roadmap",
    "SOURCE_AUTHORITY_MAP.md": "render_authority",
    "ARCHITECTURE.md": "render_architecture",
    "WORKFLOW_STATE_MACHINE.md": "render_workflows",
    "SEQUENCE_CONTRACTS.md": "render_sequence",
    "MODULE_MAP.md": "render_modules",
    "SYMBOL_INDEX.md": "render_symbols",
    "FLOW_INDEX.md": "render_flows",
    "TEST_ACCEPTANCE_MATRIX.md": "render_acceptance",
    "DOC_SYNC_MATRIX.md": "render_doc_sync",
    "PROJECT_TRUTH_SYNC.md": "render_truth",
    "API_CONTRACTS.md": "render_api",
    "DATA_CONTRACTS.md": "render_data",
    "UI_INFORMATION_ARCHITECTURE.md": "render_ui",
    "RUNBOOK.md": "render_runbook",
    "DECISIONS.md": "render_decisions",
    "KNOWN_DEFECTS.md": "render_defects",
    "GLOSSARY.md": "render_glossary",
    "CHANGELOG.md": "render_changelog",
}
MODULE_PATHS = ["scripts/" + name + ".py" for name in [
    "project_truth_projection_common",
    "project_truth_projection_state",
    "project_truth_projection_code",
    "project_truth_projection_governance",
    "project_truth_projection_contracts",
]]


def load_generator(alias: str):
    spec = importlib.util.spec_from_file_location(alias, GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("GENERATOR_IMPORT_SPEC:" + alias)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def renderer_args(module, profile, specs, workflows, facts, sequence_required, name):
    values = {
        "profile": profile,
        "specs": specs,
        "workflows": workflows,
        "facts": facts,
        "sequence_required": sequence_required,
    }
    args = []
    for parameter in inspect.signature(getattr(module, name)).parameters.values():
        if parameter.name not in values:
            raise RuntimeError("UNMAPPED_RENDERER_PARAMETER:" + name + ":" + parameter.name)
        args.append(values[parameter.name])
    return args


def main() -> None:
    source = GENERATOR.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    old = load_generator("sw2_17_old_generator")

    profile_path = ROOT / "PROJECT_PROFILE.yaml"
    profile_data = old.parse_profile(profile_path)
    profile = old.normalized_profile(profile_data)
    required = old.required_docs(profile_data)
    contracts = old.contract_settings(profile_data)
    sequence = old.sequence_settings(profile_data)
    documentation = old.documentation_settings(profile_data)
    spec_root = ROOT / str(documentation.get("spec_root", ".workflow"))
    specs, workflows = old.read_specs(spec_root)
    facts = json.loads((ROOT / ".workflow/generated/code_facts.json").read_text(encoding="utf-8"))
    sequence_required = bool(sequence.get("required", False))

    leaf = [name for names in GROUPS.values() for name in names]
    if len(leaf) != 22 or len(set(leaf)) != 22:
        raise RuntimeError("PROJECTION_RENDERER_CARDINALITY")
    before_leaf = {
        name: getattr(old, name)(*renderer_args(old, profile, specs, workflows, facts, sequence_required, name))
        for name in leaf
    }
    before_pack = old.render_all(
        profile, specs, workflows, facts, required, contracts, sequence,
        "SW2-17-PARITY-DIGEST",
    )

    tree = ast.parse(source)
    funcs = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    required_functions = set(COMMON + leaf + ["render_all"])
    missing = sorted(required_functions - set(funcs))
    if missing:
        raise RuntimeError("MISSING_FUNCTIONS:" + ",".join(missing))
    for name in leaf:
        cross = sorted({
            node.id for node in ast.walk(funcs[name])
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
            and node.id.startswith("render_") and node.id != name
        })
        if cross:
            raise RuntimeError("CROSS_RENDERER_DEPENDENCY:" + name + ":" + ",".join(cross))

    def function_text(name: str) -> str:
        node = funcs[name]
        return "".join(lines[node.lineno - 1:node.end_lineno]).rstrip() + "\n"

    common_text = (
        '"""Shared deterministic helpers for Project Truth projections."""\n\n'
        "from __future__ import annotations\n\n"
        "from pathlib import Path\n"
        "from typing import Any\n\n"
        + "\n\n".join(function_text(name).rstrip() for name in COMMON)
        + "\n"
    )
    (SCRIPTS / "project_truth_projection_common.py").write_text(common_text, encoding="utf-8", newline="\n")

    common_set = set(COMMON)
    for module_name, names in GROUPS.items():
        used_common = set()
        for name in names:
            for node in ast.walk(funcs[name]):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in common_set:
                    used_common.add(node.id)
        import_block = ""
        if used_common:
            import_block = (
                "from project_truth_projection_common import (\n"
                + "".join("    " + name + ",\n" for name in sorted(used_common))
                + ")\n\n"
            )
        text = (
            '"""Deterministic Project Truth projection renderers.\n\n'
            "Extracted verbatim from generate_project_docs.py; no format semantics live here.\n"
            '"""\n\n'
            "from __future__ import annotations\n\n"
            + import_block
            + "\n\n".join(function_text(name).rstrip() for name in names)
            + "\n"
        )
        (SCRIPTS / (module_name + ".py")).write_text(text, encoding="utf-8", newline="\n")

    remove_lines = set()
    for name in COMMON + leaf:
        node = funcs[name]
        remove_lines.update(range(node.lineno - 1, node.end_lineno))
    remaining = "".join(line for index, line in enumerate(lines) if index not in remove_lines)

    import_block = '''from project_truth_projection_common import (\n    auth_lookup,\n    bullets,\n    cell,\n    claim_backlink_comment,\n    clean,\n    generated_header,\n    normalize_markdown,\n    wanted_doc_names,\n)\nfrom project_truth_projection_state import (\n    render_architecture,\n    render_authority,\n    render_current_state,\n    render_project_manifest,\n    render_roadmap,\n    render_sequence,\n    render_system_overview,\n    render_workflows,\n)\nfrom project_truth_projection_code import (\n    render_acceptance,\n    render_flows,\n    render_modules,\n    render_symbols,\n)\nfrom project_truth_projection_governance import (\n    render_changelog,\n    render_decisions,\n    render_defects,\n    render_doc_sync,\n    render_glossary,\n    render_truth,\n)\nfrom project_truth_projection_contracts import (\n    render_api,\n    render_data,\n    render_runbook,\n    render_ui,\n)\n\n'''
    marker = "\nSPEC_FILES = ["
    if remaining.count(marker) != 1:
        raise RuntimeError("GENERATOR_IMPORT_INSERTION_MARKER")
    GENERATOR.write_text(remaining.replace(marker, "\n" + import_block + "SPEC_FILES = [", 1), encoding="utf-8", newline="\n")

    engine_path = SCRIPTS / "governance_engine.py"
    engine = engine_path.read_text(encoding="utf-8")
    anchor = '    "scripts/project_truth_impact.py",\n}'
    replacement = '    "scripts/project_truth_impact.py",\n' + "".join('    "' + path + '",\n' for path in MODULE_PATHS) + '}'
    if engine.count(anchor) != 1:
        raise RuntimeError("GOVERNANCE_COMPILER_FILES_ANCHOR")
    engine_path.write_text(engine.replace(anchor, replacement, 1), encoding="utf-8", newline="\n")

    impact_path = SCRIPTS / "project_truth_impact.py"
    impact = impact_path.read_text(encoding="utf-8")
    anchor = '    "scripts/project_profile.py",\n    "scripts/schema_contract.py",\n}'
    replacement = '    "scripts/project_profile.py",\n    "scripts/schema_contract.py",\n' + "".join('    "' + path + '",\n' for path in MODULE_PATHS) + '}'
    if impact.count(anchor) != 1:
        raise RuntimeError("IMPACT_BROAD_TOOL_ANCHOR")
    impact_path.write_text(impact.replace(anchor, replacement, 1), encoding="utf-8", newline="\n")

    selftest_path = SCRIPTS / "selftest_project_truth_compiler.py"
    selftest = selftest_path.read_text(encoding="utf-8")
    contract = '''\n\ndef test_projection_module_contract(skill_root: Path) -> None:\n    import ast\n    import importlib\n    import inspect\n\n    scripts = skill_root / "scripts"\n    inserted = False\n    if str(scripts) not in sys.path:\n        sys.path.insert(0, str(scripts))\n        inserted = True\n    try:\n        generator = importlib.import_module("generate_project_docs")\n        expected_modules = {\n            "project_truth_projection_state": {"render_system_overview", "render_project_manifest", "render_current_state", "render_roadmap", "render_authority", "render_architecture", "render_workflows", "render_sequence"},\n            "project_truth_projection_code": {"render_modules", "render_symbols", "render_flows", "render_acceptance"},\n            "project_truth_projection_governance": {"render_doc_sync", "render_truth", "render_decisions", "render_defects", "render_changelog", "render_glossary"},\n            "project_truth_projection_contracts": {"render_api", "render_data", "render_ui", "render_runbook"},\n        }\n        expected_map = ''' + repr(DOC_MAP) + '''\n        source = (scripts / "generate_project_docs.py").read_text(encoding="utf-8")\n        tree = ast.parse(source)\n        top_renderers = {node.name for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith("render_")}\n        if top_renderers != {"render_all"}:\n            raise RuntimeError("PROJECTION_MONOLITH_RENDERERS_REMAIN:" + ",".join(sorted(top_renderers)))\n        render_all = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "render_all")\n        observed_map = {}\n        for node in ast.walk(render_all):\n            if not isinstance(node, ast.Assign) or not any(isinstance(t, ast.Name) and t.id == "renderers" for t in node.targets):\n                continue\n            if not isinstance(node.value, ast.Dict):\n                continue\n            for key, value in zip(node.value.keys, node.value.values):\n                if isinstance(key, ast.Constant) and isinstance(key.value, str) and isinstance(value, ast.Lambda) and isinstance(value.body, ast.Call) and isinstance(value.body.func, ast.Name):\n                    observed_map[key.value] = value.body.func.id\n        if observed_map != expected_map:\n            raise RuntimeError("PROJECTION_RENDERER_MAP_MISMATCH")\n        profile_data = generator.parse_profile(skill_root / "PROJECT_PROFILE.yaml")\n        profile = generator.normalized_profile(profile_data)\n        documentation = generator.documentation_settings(profile_data)\n        specs, workflows = generator.read_specs(skill_root / str(documentation.get("spec_root", ".workflow")))\n        facts = json.loads((skill_root / ".workflow/generated/code_facts.json").read_text(encoding="utf-8"))\n        sequence = generator.sequence_settings(profile_data)\n        values = {"profile": profile, "specs": specs, "workflows": workflows, "facts": facts, "sequence_required": bool(sequence.get("required", False))}\n        seen = set()\n        for module_name, names in expected_modules.items():\n            module = importlib.import_module(module_name)\n            for name in names:\n                fn = getattr(module, name, None)\n                if not callable(fn):\n                    raise RuntimeError("PROJECTION_RENDERER_MISSING:" + module_name + ":" + name)\n                if getattr(generator, name).__module__ != module_name:\n                    raise RuntimeError("PROJECTION_REEXPORT_MISMATCH:" + name)\n                args = []\n                for parameter in inspect.signature(fn).parameters.values():\n                    if parameter.name not in values:\n                        raise RuntimeError("PROJECTION_PARAMETER_UNMAPPED:" + name + ":" + parameter.name)\n                    args.append(values[parameter.name])\n                if not isinstance(fn(*args), str):\n                    raise RuntimeError("PROJECTION_RENDERER_NON_TEXT:" + name)\n                seen.add(name)\n        if seen != set(expected_map.values()):\n            raise RuntimeError("PROJECTION_DIRECT_COVERAGE_INCOMPLETE")\n    finally:\n        if inserted and sys.path and sys.path[0] == str(scripts):\n            sys.path.pop(0)\n'''
    marker = "\ndef main() -> int:\n"
    if selftest.count(marker) != 1:
        raise RuntimeError("SELFTEST_MAIN_MARKER")
    selftest = selftest.replace(marker, contract + marker, 1)
    call_marker = '    test_gitignored_source_files_are_excluded()\n    print("GITIGNORED_SOURCE_EXCLUSION=PASS")\n'
    call = call_marker + '    test_projection_module_contract(skill_root)\n    print("PROJECTION_MODULE_CONTRACT=PASS modules=4 renderers=22")\n'
    if selftest.count(call_marker) != 1:
        raise RuntimeError("SELFTEST_CALL_MARKER")
    selftest_path.write_text(selftest.replace(call_marker, call, 1), encoding="utf-8", newline="\n")

    for name in ["generate_project_docs", "project_truth_projection_common"] + list(GROUPS):
        sys.modules.pop(name, None)
    importlib.invalidate_caches()
    new = load_generator("sw2_17_new_generator")
    after_leaf = {
        name: getattr(new, name)(*renderer_args(new, profile, specs, workflows, facts, sequence_required, name))
        for name in leaf
    }
    after_pack = new.render_all(
        profile, specs, workflows, facts, required, contracts, sequence,
        "SW2-17-PARITY-DIGEST",
    )
    if before_leaf != after_leaf:
        bad = sorted(name for name in leaf if before_leaf[name] != after_leaf[name])
        raise RuntimeError("PROJECTION_LEAF_PARITY_MISMATCH:" + ",".join(bad))
    if before_pack != after_pack:
        bad = sorted(name for name in set(before_pack) | set(after_pack) if before_pack.get(name) != after_pack.get(name))
        raise RuntimeError("PROJECTION_PACK_PARITY_MISMATCH:" + ",".join(bad))
    print("SW2_17_RENDERER_PARITY=PASS renderers=22 modules=4")


if __name__ == "__main__":
    main()
