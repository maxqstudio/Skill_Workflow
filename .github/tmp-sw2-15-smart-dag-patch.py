from pathlib import Path

engine = Path("scripts/governance_engine.py")
text = engine.read_text(encoding="utf-8")

marker = "\n\ndef git(root: Path, *args: str) -> str:\n"
if text.count(marker) != 1:
    raise RuntimeError("SMART_DAG_INSERT_ANCHOR")
addition = r'''

DEVELOP_NODE_ORDER = (
    "compile_scripts",
    "engine_regression",
    "sequence_regression",
    "cross_document_regression",
    "compiler_selftest",
    "sync_project_truth",
    "validate_project_docs",
    "validate_cross_document_consistency",
    "impact_only",
)
DEVELOP_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "compile_scripts": (),
    "engine_regression": ("compile_scripts",),
    "sequence_regression": ("compile_scripts",),
    "cross_document_regression": ("compile_scripts",),
    "compiler_selftest": ("compile_scripts",),
    "sync_project_truth": (),
    "validate_project_docs": (),
    "validate_cross_document_consistency": ("sync_project_truth",),
    "impact_only": (),
}
VERIFY_NODE_ORDER = VERIFY_NODE_NAMES + ("impact_only",)
VERIFY_DEPENDENCIES: dict[str, tuple[str, ...]] = {
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
    "impact_only": (),
}
VERIFY_BROAD_IMPACTS = frozenset({"broad_source", "template", "ci"})
VERIFY_IMPACT_NODE_SEEDS: dict[str, tuple[str, ...]] = {
    "engine": ("engine_regression", "validate_cross_document_consistency"),
    "sequence": (
        "sequence_regression",
        "validate_sequence_sessions",
        "validate_cross_document_consistency",
    ),
    "compiler": ("compiler_selftest", "validate_cross_document_consistency"),
    "cross_document": (
        "cross_document_regression",
        "validate_cross_document_consistency",
    ),
    "governance": (
        "validate_sequence_sessions",
        "validate_cross_document_consistency",
    ),
    "documentation": ("validate_cross_document_consistency",),
    "source": (
        "validate_sequence_sessions",
        "validate_cross_document_consistency",
    ),
    "benchmark": (),
}


def dependency_closure(
    seed_names: tuple[str, ...] | list[str],
    dependencies: dict[str, tuple[str, ...]],
    order: tuple[str, ...],
) -> tuple[str, ...]:
    selected: set[str] = set()
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in selected:
            return
        if name in visiting:
            raise ValueError(f"PLANNER_DAG_CYCLE:{name}")
        if name not in dependencies:
            raise ValueError(f"UNKNOWN_PLANNER_NODE:{name}")
        visiting.add(name)
        for dependency in dependencies[name]:
            if dependency not in dependencies:
                raise ValueError(f"UNKNOWN_PLANNER_DEPENDENCY:{name}:{dependency}")
            visit(dependency)
        visiting.remove(name)
        selected.add(name)

    for seed in seed_names:
        visit(seed)

    missing_order = selected.difference(order)
    if missing_order:
        raise ValueError("PLANNER_ORDER_MISSING:" + ",".join(sorted(missing_order)))
    return tuple(name for name in order if name in selected)


def verify_seed_node_names(
    paths: tuple[str, ...] | list[str],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    impact_set = set(impacts)
    if impact_set.intersection(VERIFY_BROAD_IMPACTS):
        return VERIFY_NODE_NAMES
    if "unknown" in impact_set:
        raise ValueError("VERIFY_UNKNOWN_IMPACT_REQUIRES_FINALIZE")

    seeds: set[str] = set()
    handled = set(VERIFY_IMPACT_NODE_SEEDS) | {"targeted_test"}
    unhandled = impact_set.difference(handled)
    if unhandled:
        raise ValueError("UNMAPPED_VERIFY_IMPACT:" + ",".join(sorted(unhandled)))

    for impact in sorted(impact_set):
        seeds.update(VERIFY_IMPACT_NODE_SEEDS.get(impact, ()))

    if "targeted_test" in impact_set:
        mapped = {
            node_name
            for path, node_name in DEVELOP_TEST_MAP.items()
            if path in set(paths)
        }
        if not mapped:
            raise ValueError("TARGETED_TEST_WITHOUT_VERIFY_NODE")
        seeds.update(mapped)
        seeds.add("validate_cross_document_consistency")

    if not seeds:
        seeds.add("impact_only")
    return tuple(name for name in VERIFY_NODE_ORDER if name in seeds)


def verify_node_names(
    paths: tuple[str, ...] | list[str],
    impacts: tuple[str, ...],
) -> tuple[str, ...]:
    seeds = verify_seed_node_names(paths, impacts)
    return dependency_closure(seeds, VERIFY_DEPENDENCIES, VERIFY_NODE_ORDER)
'''
text = text.replace(marker, addition + marker, 1)

old = '''    ordered = [
        name
        for name in (
            "compile_scripts",
            "engine_regression",
            "sequence_regression",
            "cross_document_regression",
            "compiler_selftest",
            "sync_project_truth",
            "validate_project_docs",
            "validate_cross_document_consistency",
            "impact_only",
        )
        if name in names
    ]
    return tuple(ordered)
'''
new = '''    ordered = [name for name in DEVELOP_NODE_ORDER if name in names]
    return dependency_closure(
        tuple(ordered),
        DEVELOP_DEPENDENCIES,
        DEVELOP_NODE_ORDER,
    )
'''
if text.count(old) != 1:
    raise RuntimeError("SMART_DAG_DEVELOP_ANCHOR")
text = text.replace(old, new, 1)

old = '''    if effective == "verify":
        return VERIFY_NODE_NAMES
    return develop_node_names(paths, impacts)
'''
new = '''    if effective == "verify":
        return verify_node_names(paths, impacts)
    return develop_node_names(paths, impacts)
'''
if text.count(old) != 1:
    raise RuntimeError("SMART_DAG_VERIFY_PLAN_ANCHOR")
text = text.replace(old, new, 1)

old = '''        if not failures:
            impacts = classify_changed_paths(changed_paths)
            selected_mode = effective_mode(args.mode, impacts)
            if selected_mode == "finalize" and not expected_head:
                failures.append("FINALIZE_EXPECTED_HEAD_REQUIRED")
            else:
                selected_nodes = planned_node_names(
                    args.mode,
                    selected_mode,
                    changed_paths,
                    impacts,
                )
'''
new = '''        if not failures:
            try:
                impacts = classify_changed_paths(changed_paths)
                selected_mode = effective_mode(args.mode, impacts)
                if selected_mode == "finalize" and not expected_head:
                    failures.append("FINALIZE_EXPECTED_HEAD_REQUIRED")
                else:
                    selected_nodes = planned_node_names(
                        args.mode,
                        selected_mode,
                        changed_paths,
                        impacts,
                    )
            except ValueError as exc:
                failures.append(str(exc))
'''
if text.count(old) != 1:
    raise RuntimeError("SMART_DAG_FAIL_CLOSED_ANCHOR")
text = text.replace(old, new, 1)
engine.write_text(text, encoding="utf-8", newline="\n")

test = Path("scripts/selftest_governance_engine.py")
text = test.read_text(encoding="utf-8")
old = '''    classify_changed_paths,
    collect_changed_paths,
    develop_node_names,
    effective_mode,
    planned_node_names,
)'''
new = '''    classify_changed_paths,
    collect_changed_paths,
    dependency_closure,
    develop_node_names,
    effective_mode,
    planned_node_names,
)'''
if text.count(old) != 1:
    raise RuntimeError("SMART_DAG_SELFTEST_IMPORT_ANCHOR")
text = text.replace(old, new, 1)

marker = "\n\ndef changed_path_collection_contract() -> None:\n"
if text.count(marker) != 1:
    raise RuntimeError("SMART_DAG_SELFTEST_INSERT_ANCHOR")
addition = r'''


def smart_validation_dag_contract() -> None:
    sequence_paths = ("docs/sequence/sessions/SW2-15-GOVERNANCE.json",)
    sequence_impacts = classify_changed_paths(sequence_paths)
    sequence_develop = planned_node_names(
        "develop", "develop", sequence_paths, sequence_impacts
    )
    require(
        sequence_develop == ("compile_scripts", "sequence_regression"),
        f"develop prerequisite closure drifted: {sequence_develop}",
    )
    print("SMART_DEVELOP_IMPACT_SELECTION=PASS")

    doc_paths = ("references/governance-and-project-truth.md",)
    doc_impacts = classify_changed_paths(doc_paths)
    doc_verify = planned_node_names("verify", "verify", doc_paths, doc_impacts)
    expected_doc_verify = {
        "validate_project_docs",
        "validate_human_comprehension",
        "validate_handoff",
        "validate_cross_document_consistency",
    }
    require(
        set(doc_verify) == expected_doc_verify,
        f"verify documentation closure drifted: {doc_verify}",
    )
    require(
        set(doc_verify).isdisjoint(
            {
                "engine_regression",
                "sequence_regression",
                "cross_document_regression",
                "compiler_selftest",
            }
        ),
        f"verify retained unrelated regressions: {doc_verify}",
    )

    engine_paths = ("scripts/governance_engine.py",)
    engine_impacts = classify_changed_paths(engine_paths)
    engine_verify = set(
        planned_node_names("verify", "verify", engine_paths, engine_impacts)
    )
    require(
        {
            "compile_scripts",
            "engine_regression",
            "validate_project_docs",
            "validate_human_comprehension",
            "validate_handoff",
            "validate_cross_document_consistency",
        }.issubset(engine_verify),
        f"engine verify closure incomplete: {engine_verify}",
    )

    source_paths = ("src/example.py",)
    source_impacts = classify_changed_paths(source_paths)
    source_verify = set(
        planned_node_names("verify", "verify", source_paths, source_impacts)
    )
    require(
        {
            "validate_project_docs",
            "validate_human_comprehension",
            "validate_sequence_sessions",
            "validate_handoff",
            "validate_cross_document_consistency",
        }.issubset(source_verify),
        f"source verify closure incomplete: {source_verify}",
    )
    require(
        len(doc_verify) < len(VERIFY_NODE_NAMES),
        "smart verify did not reduce known documentation work",
    )
    print("SMART_VERIFY_DEPENDENCY_CLOSURE=PASS")

    broad_paths = ("scripts/new_future_validator.py",)
    broad_impacts = classify_changed_paths(broad_paths)
    broad_verify = planned_node_names("develop", "verify", broad_paths, broad_impacts)
    require(
        broad_verify == VERIFY_NODE_NAMES,
        f"broad impact was narrowed unsafely: {broad_verify}",
    )

    adversarial = (
        (
            ("child",),
            {"child": ("missing",)},
            ("child",),
            "UNKNOWN_PLANNER_DEPENDENCY",
        ),
        (
            ("a",),
            {"a": ("b",), "b": ("a",)},
            ("a", "b"),
            "PLANNER_DAG_CYCLE",
        ),
        (
            ("ghost",),
            {"known": ()},
            ("known",),
            "UNKNOWN_PLANNER_NODE",
        ),
    )
    for seeds, dependencies, order, marker_text in adversarial:
        try:
            dependency_closure(seeds, dependencies, order)
        except ValueError as exc:
            require(marker_text in str(exc), f"wrong planner failure: {exc}")
        else:
            raise AssertionError(marker_text + " did not fail closed")
    print("SMART_PLANNER_FAIL_CLOSED=PASS")

    finalize_nodes = planned_node_names(
        "finalize",
        "finalize",
        ("scripts/governance_engine.py",),
        ("engine",),
    )
    require(
        finalize_nodes == FINALIZE_NODE_NAMES,
        f"finalize authoritative DAG was narrowed: {finalize_nodes}",
    )
    print("SMART_FINALIZE_EXHAUSTIVE=PASS")
'''
text = text.replace(marker, addition + marker, 1)

old = '''    mode_planning_contract()
    changed_path_collection_contract()
'''
new = '''    mode_planning_contract()
    smart_validation_dag_contract()
    changed_path_collection_contract()
'''
if text.count(old) != 1:
    raise RuntimeError("SMART_DAG_SELFTEST_MAIN_ANCHOR")
text = text.replace(old, new, 1)
test.write_text(text, encoding="utf-8", newline="\n")
