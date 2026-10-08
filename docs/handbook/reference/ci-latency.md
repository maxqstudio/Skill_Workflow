# CI Latency and Cost Evidence (SW2-24)

## Authority boundary

The permanent `Governance CI` workflow is still the acceptance authority. Its **six required contexts** remain unchanged:

1. Self Governance (Ubuntu)
2. Governance Selftest (Ubuntu)
3. Governance Selftest (Windows)
4. SW2 Sequence Evidence (Ubuntu), including a blocking Mermaid CLI render
5. Governance Engine Performance (Ubuntu)
6. Consumer Engine Performance (pinned max-grounding)

The final candidate, squash merge, and final `main` must all retain full exact-HEAD evidence. CI applicability can omit expensive benchmarking only for rigorously classified docs-only pull requests; non-PR/unknown changes fail closed to full testing. Caching, previously passed runs, or fast development mode **never** replace final acceptance.

## Measured starting baseline

The authoritative machine-readable run sample is `benchmarks/baselines/sw2-24-ci-latency.json`. It records six successful, completed GitHub runs bound to exact SHAs: `37430818483`, `37706618341`, `37708376562`, `37708565187`, `37708853965`, `37708986331`.

- Windows Governance Selftest durations: **87, 73, 79, 94, 56, 75 seconds**
- Baseline Windows median: **77 seconds**
- Median aggregate elapsed job-seconds (six contexts): **197 seconds**
- Windows was the slowest job in **all six observed runs**

These are hosted-runner observations, not an SLA, bill, or a causal comparison. Jobs overlap, so sum of job-seconds is not the same as a wall-clock workflow duration. Queue latency, hardware variation, package caches, runner minute pricing and platform multipliers cannot be inferred from these durations.

## Bounded independent regression execution

The seven original Windows regression **groups** still run, covering ten explicit commands:

- Consumer finalize negative-path
- Schema/toolchain migration and validation
- Cross-language analyzer
- Historical sequence freeze
- Public documentation, generated documentation presentation and validation
- Release preflight
- Project Truth Compiler self-test

Each group uses isolated temporary fixtures. The explicit inventory lives in `.github/scripts/ci_parallel_selftests.py` and is cross-checked against the **unchanged serial Ubuntu inventory** by `.github/scripts/validate_ci_parallel_contract.py`.

Only the Windows selftest job executes this inventory with a maximum of three concurrent workers. Each group runs its commands in sequence. Every group is dispatched regardless of a different group's failure. The runner returns non-zero on any failed, missing or incomplete gate and records the deterministic first failed gate plus individual outputs. It has no shell execution, dynamic test discovery, or success-result cache.

The existing Windows read-only verify and STRICT workflow self-test remain serial, after the parallel group. The main producer finalize, consumer source tests and complete consumer validation, Mermaid rendering, and engine performance are all unchanged.

## Required performance comparison

SW2-24 targets a **minimum 15% decrease** in median Windows selftest duration versus the above 77-second baseline, using at least three exact-candidate successful permanent CI runs. A single fast run is not evidence of stable speedup. Candidate observations must state when caches were warm or cold where this can be determined; otherwise cache state is `NOT_PROVEN`. They must also report job-seconds and any workload differences. If a material regression or unproven improvement remains, **do not label the optimization as accepted performance success**.

## Fail-closed recovery

If concurrency reveals fixture interference, non-deterministic results, or missing tests, the safe repair is to remove that group from parallel execution and restore its original serial Windows step **while retaining the test**. Never suppress the failed test, mark a required context not applicable, bypass the first failing gate, or silently promote source/runtime evidence.
