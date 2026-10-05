from pathlib import Path

ROOT = Path('.')
engine_path = ROOT / 'scripts/governance_engine.py'
test_path = ROOT / 'scripts/selftest_governance_engine.py'

engine = engine_path.read_text(encoding='utf-8')

insert_anchor = '\n\ndef git(root: Path, *args: str) -> str:\n'
if engine.count(insert_anchor) != 1:
    raise RuntimeError('ENGINE_INSERT_ANCHOR')

planner = r'''

NODE_ORDER = (
    "impact_only",
    "compile_scripts",
    "engine_regression",
    "sequence_regression",
    "cross_document_regression",
    "compiler_selftest",
    "strict_workflow_selftest",
    "sync_project_truth",
    "validate_project_docs",
    "validate_human_comprehension",
    "validate_sequence_sessions",
    "validate_handoff",
    "validate_cross_document_consistency",
    "validate_project_truth",
    "governed_state_clean",
)

DEVELOP_NODE_DEPENDENCIES = {
    "impact_only": (),
    "compile_scripts": (),
    "engine_regression": ("compile_scripts",),
    "sequence_regression": ("compile_scripts",),
    "cross_document_regression": ("compile_scripts",),
    "compiler_selftest": ("compile_scripts",),
    "sync_project_truth": (),
    "validate_cross_document_consistency": ("sync_project_truth",),
}

VERIFY_NODE_DEPENDENCIES = {
    "impact_only": (),
    "compile_scripts": (),
    "engine_regression": ("compile_scripts",),
    "sequence_regression": ("compile_scripts",),
    "cross_document_regression": ("compile_scripts",),
    "compiler_selftest": ("compile_scripts",),
    "validate_project_docs": (),
    "validate_human_comprehension": ("validate_project_docs",),
    "validate_sequence_sessions": (),
    "validate_handoff": ("validate_project_docs",),
    "validate_cross_document_consistency": (
        "validate_human_comprehension",
        "validate_handoff",
    ),
}


def _ordered_nodes(names: set[str]) -> tuple[str, ...]:
    unknown = names.difference(NODE_ORDER)
    if unknown:
        raise ValueError("UNKNOWN_PLANNED_NODE:" + ",".join(sorted(unknown)))
    return tuple(name for name in NODE_ORDER if name in names)


def prerequisite_closure(
    seeds: tuple[str, ...] | list[str] | set[str],
    dependency_map: dict[str, tuple[str, ...]],
) -> tuple[str, ...]:
    selected: set[str] = set()
    visiting: set[str] = set()

    def include(name: str) -> None:
        if name not in dependency_map:
            raise ValueError(f"UNKNOWN_PLANNER_NODE:{name}")
        if name in selected:
            return
        if name in visiting:
            raise ValueError(f"PLANNER_DEPENDENCY_CYCLE:{name}")
        visiting.add(name)
        for dependency in dependency_map[name]:
            if dependency not in dependency_map:
                raise ValueError(f"UNKNOWN_PLANNER_DEPENDENCY:{name}:{dependency}")
            include(dependency)
        visiting.remove(name)
        selected.add(name)

    for seed in seeds:
        include(seed)
    return _ordered_nodes(selected)


def affected_closure(
    seeds: tuple[str, ...] | list[str] | set[str],
    dependency_map: dict[str, tuple[str, ...]],
) -> tuple[str, ...]:
    selected = set(prerequisite_closure(seeds, dependency_map))
    reverse: dict[str, set[str]] = {name: set() for name in dependency_map}
    for name, dependencies in dependency_map.items():
        for dependency in dependencies:
            if dependency not in dependency_map:
                raise ValueError(f"UNKNOWN_PLANNER_DEPENDENCY:{name}:{dependency}")
            reverse[dependency].add(name)

    queue = list(selected)
    while queue:
        current = queue.pop()
        for dependent in sorted(reverse[current]):
            if dependent in selected:
                continue
            expanded = set(prerequisite_closure((dependent,), dependency_map))
            new_nodes = expanded.difference(selected)
            if new_nodes:
                selected.update(new_nodes)
                queue.extend(sorted(new_nodes))
    return _ordered_nodes(selected)


def verify_seed_node_names(
    paths: tuple[str, ...] | list[str],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    impact_set = set(impacts)
    if impact_set.intersection({"broad_source", "template", "ci"}):
        return VERIFY_NODE_NAMES

    seeds: set[str] = set()
    if "engine" in impact_set:
        seeds.add("engine_regression")
    if "sequence" in impact_set:
        seeds.update({"sequence_regression", "validate_sequence_sessions"})
    if "compiler" in impact_set:
        seeds.update({"compiler_selftest", "validate_project_docs"})
    if "cross_document" in impact_set:
        seeds.update({"cross_document_regression", "validate_cross_document_consistency"})
    if "governance" in impact_set:
        seeds.update({
            "validate_project_docs",
            "validate_human_comprehension",
            "validate_sequence_sessions",
            "validate_handoff",
            "validate_cross_document_consistency",
        })
    if "documentation" in impact_set or "source" in impact_set:
        seeds.update({
            "validate_project_docs",
            "validate_human_comprehension",
            "validate_handoff",
            "validate_cross_document_consistency",
        })
    for path, node_name in DEVELOP_TEST_MAP.items():
        if path in set(paths):
            seeds.add(node_name)
    if "benchmark" in impact_set and not seeds:
        seeds.add("impact_only")
    if not seeds:
        seeds.add("impact_only")
    return _ordered_nodes(seeds)
'''
engine = engine.replace(insert_anchor, planner + insert_anchor, 1)

start = engine.index('def develop_node_names(')
end = engine.index('\n\ndef governed_status(', start)
replacement = r'''def develop_seed_node_names(
    paths: tuple[str, ...] | list[str],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    seeds: set[str] = set()
    path_set = set(paths)
    if path_set.intersection(ENGINE_DEVELOP_FILES):
        seeds.add("engine_regression")
    if path_set.intersection(SEQUENCE_DEVELOP_FILES) or any(
        path.startswith("docs/sequence/") for path in path_set
    ):
        seeds.add("sequence_regression")
    if path_set.intersection(COMPILER_DEVELOP_FILES):
        seeds.add("compiler_selftest")
    if path_set.intersection(CROSSDOC_DEVELOP_FILES):
        seeds.add("cross_document_regression")
    for path, node_name in DEVELOP_TEST_MAP.items():
        if path in path_set:
            seeds.add(node_name)
    impact_set = set(impacts)
    if impact_set.intersection({"governance", "documentation", "source"}):
        seeds.add("sync_project_truth")
    if "documentation" in impact_set:
        seeds.add("validate_cross_document_consistency")
    if "benchmark" in impact_set and not seeds:
        seeds.add("impact_only")
    if not seeds:
        seeds.add("impact_only")
    return _ordered_nodes(seeds)


def develop_node_names(
    paths: tuple[str, ...] | list[str],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    return prerequisite_closure(
        develop_seed_node_names(paths, impacts),
        DEVELOP_NODE_DEPENDENCIES,
    )


def verify_node_names(
    paths: tuple[str, ...] | list[str],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    seeds = verify_seed_node_names(paths, impacts)
    if set(seeds) == set(VERIFY_NODE_NAMES):
        return VERIFY_NODE_NAMES
    return affected_closure(seeds, VERIFY_NODE_DEPENDENCIES)


def planned_node_names(
    requested: str,
    effective: str,
    paths: tuple[str, ...],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    if effective == "finalize":
        return FINALIZE_NODE_NAMES
    if effective == "verify":
        return verify_node_names(paths, impacts)
    return develop_node_names(paths, impacts)
'''
engine = engine[:start] + replacement + engine[end:]

old_doc = 'SW2-02 adds develop, verify, and finalize modes without changing standalone\nvalidator behavior. Fast modes may reduce intermediate work only when impact is\nknown. Unknown impact escalates. Finalize remains the only complete acceptance\nmode and requires an exact expected HEAD.'
new_doc = 'SW2-02 adds develop, verify, and finalize modes without changing standalone\nvalidator behavior. SW2-15 makes intermediate planning dependency-aware: develop\nselects impacted checks plus prerequisites, verify expands the affected semantic\nclosure, and unknown impact still broadens fail-closed. Finalize remains the only\ncomplete acceptance mode and requires an exact expected HEAD.'
if engine.count(old_doc) != 1:
    raise RuntimeError('ENGINE_DOCSTRING_ANCHOR')
engine = engine.replace(old_doc, new_doc, 1)
engine_path.write_text(engine, encoding='utf-8', newline='\n')

test = test_path.read_text(encoding='utf-8')
old_import = '''    ValidationDAG,\n    ValidationNode,\n    classify_changed_paths,\n    collect_changed_paths,\n    develop_node_names,\n    effective_mode,\n    planned_node_names,\n)'''
new_import = '''    ValidationDAG,\n    ValidationNode,\n    affected_closure,\n    classify_changed_paths,\n    collect_changed_paths,\n    develop_node_names,\n    effective_mode,\n    planned_node_names,\n    prerequisite_closure,\n    verify_node_names,\n)'''
if test.count(old_import) != 1:
    raise RuntimeError('SELFTEST_IMPORT_ANCHOR')
test = test.replace(old_import, new_import, 1)

insert_test_anchor = '\n\ndef changed_path_collection_contract() -> None:\n'
if test.count(insert_test_anchor) != 1:
    raise RuntimeError('SELFTEST_FUNCTION_ANCHOR')
smart_test = r'''


def smart_validation_dag_contract() -> None:
    engine_paths = ("scripts/governance_engine.py",)
    engine_impacts = classify_changed_paths(engine_paths)
    engine_verify = verify_node_names(engine_paths, engine_impacts)
    require(
        engine_verify == ("compile_scripts", "engine_regression"),
        f"engine verify repeated unrelated validation: {engine_verify}",
    )

    compiler_paths = ("scripts/generate_project_docs.py",)
    compiler_impacts = classify_changed_paths(compiler_paths)
    compiler_verify = set(verify_node_names(compiler_paths, compiler_impacts))
    for required in (
        "compile_scripts",
        "compiler_selftest",
        "validate_project_docs",
        "validate_human_comprehension",
        "validate_handoff",
        "validate_cross_document_consistency",
    ):
        require(required in compiler_verify, f"compiler verify missed {required}")
    require(
        "sequence_regression" not in compiler_verify,
        f"compiler verify pulled unrelated sequence regression: {sorted(compiler_verify)}",
    )

    sequence_paths = ("scripts/validate_sequence_sessions.py",)
    sequence_impacts = classify_changed_paths(sequence_paths)
    sequence_verify = verify_node_names(sequence_paths, sequence_impacts)
    require(
        sequence_verify == (
            "compile_scripts",
            "sequence_regression",
            "validate_sequence_sessions",
        ),
        f"sequence verify closure drifted: {sequence_verify}",
    )

    broad_paths = ("scripts/future_validator.py",)
    broad_impacts = classify_changed_paths(broad_paths)
    require(
        verify_node_names(broad_paths, broad_impacts) == VERIFY_NODE_NAMES,
        "broad source verify did not broaden fail-closed",
    )

    local_graph = {
        "required": (),
        "dependent": ("required",),
    }
    require(
        prerequisite_closure(("dependent",), local_graph)
        == ("required", "dependent"),
        "mandatory prerequisite was skipped",
    )
    require(
        affected_closure(("required",), local_graph)
        == ("required", "dependent"),
        "affected dependent closure was incomplete",
    )
    try:
        prerequisite_closure(("dependent",), {"dependent": ("missing",)})
    except ValueError as exc:
        require("UNKNOWN_PLANNER_DEPENDENCY" in str(exc), f"wrong planner error: {exc}")
    else:
        raise AssertionError("missing planner dependency produced a false PASS")

    calls = {"required": 0, "dependent": 0}

    def required_fail() -> tuple[int, str]:
        calls["required"] += 1
        return 1, "EXPECTED_REQUIRED_FAILURE\\n"

    def dependent_pass() -> tuple[int, str]:
        calls["dependent"] += 1
        return 0, "UNEXPECTED_DEPENDENT_PASS\\n"

    selected = prerequisite_closure(("dependent",), local_graph)
    actions = {
        "required": required_fail,
        "dependent": dependent_pass,
    }
    results = ValidationDAG([
        ValidationNode(name, local_graph[name], actions[name])
        for name in selected
    ]).run()
    require(results["required"].status == "FAIL", "required failure was hidden")
    require(results["dependent"].status == "BLOCKED", "dependent was not blocked")
    require(calls == {"required": 1, "dependent": 0}, f"false-PASS execution: {calls}")
    print("SMART_VALIDATION_DAG=PASS")
'''
test = test.replace(insert_test_anchor, smart_test + insert_test_anchor, 1)

call_anchor = '    changed_path_collection_contract()\n'
if test.count(call_anchor) != 1:
    raise RuntimeError('SELFTEST_CALL_ANCHOR')
test = test.replace(call_anchor, '    smart_validation_dag_contract()\n' + call_anchor, 1)
test_path.write_text(test, encoding='utf-8', newline='\n')

print('SW2_15_PATCH_APPLIED=PASS')
