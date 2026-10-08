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

The first seven Windows regression **groups** retain their ten explicit commands:

- Consumer finalize negative-path
- Schema/toolchain migration and validation
- Cross-language analyzer
- Historical sequence freeze
- Public documentation, generated documentation presentation and validation
- Release preflight
- Project Truth Compiler self-test

An additional eight independently audited fixture regression groups now enter the same bounded worker pool: Governance Engine V2, sequence call-resolution, sequence squash provenance, sequence human-view, repository health, ruleset policy, cross-document regression, and LITE/STANDARD adoption fixtures. The final explicit parallel inventory comprises **15 groups and 19 commands**; Ubuntu's original serial steps remain present for all 19 commands.

Each group uses isolated temporary fixtures. The explicit inventory lives in `.github/scripts/ci_parallel_selftests.py` and is cross-checked against the **unchanged serial Ubuntu inventory** by `.github/scripts/validate_ci_parallel_contract.py`.

Only the Windows selftest job executes this inventory with a maximum of three concurrent workers. Each group runs its commands in sequence. Every group is dispatched regardless of a different group's failure. The runner returns non-zero on any failed, missing or incomplete gate and records the deterministic first failed gate plus individual outputs. It has no shell execution, dynamic test discovery, or success-result cache.

**The producer read-only verify and STRICT workflow self-test remain complete, independently blocking acceptance gates.** On Windows, a second bounded two-worker group runs those full commands concurrently only after source identity and worktree cleanliness have been verified. The STRICT regression uses isolated temporary fixtures; verify is required to stay read-only. Both commands always execute, are never cancelled when the other fails, and the runner rejects any changed HEAD, dirty governed worktree, missing command, or failed gate. Ubuntu retains the original two serial steps as an independent fallback. The static CI validator and negative regression prohibit replacement with a cached PASS. The main producer finalization, consumer source tests and complete consumer validation, Mermaid rendering, and engine performance are unchanged.

## Required performance comparison

SW2-24 targets a **minimum 15% decrease** in median Windows selftest duration versus the above 77-second baseline, using at least three exact-candidate successful permanent CI runs. A single fast run is not evidence of stable speedup. Candidate observations must state when caches were warm or cold where this can be determined; otherwise cache state is `NOT_PROVEN`. They must also report job-seconds and any workload differences. If a material regression or unproven improvement remains, **do not label the optimization as accepted performance success**.

## Fail-closed recovery

If concurrency reveals fixture interference, non-deterministic results, or missing tests, the safe repair is to remove that group from parallel execution and restore its original serial Windows step **while retaining the test**. Never suppress the failed test, mark a required context not applicable, bypass the first failing gate, or silently promote source/runtime evidence.

## Initial candidate observation and corrective action

The first exact candidate `2a12cee1873851c422664e07468bf5863a7299db` completed three full six-context Governance CI attempts (run `37710214509`). Their Windows job durations were **73, 48 and 80 seconds**; median **73 seconds**, or only about **5.2% below** the historical 77-second median. This **failed the 15% optimization objective**. The failure is retained in `benchmarks/baselines/sw2-24-initial-attempts.json`, not silently discarded.

The additional full STRICT/read-only VERIFY overlap is a subsequent implementation change requiring its own exact-head three-run measurement. Before that new evidence exists, any further speedup remains **NOT_PROVEN**.

## Second candidate observation and expanded independent inventory

The full-STRICT/read-only-VERIFY overlap candidate `8c4889ade0465a294f09a8ac8b15c35e5b744bd3` completed three exact-SHA all-six-context runs (run `37710902468`). Windows job durations were **55, 69, and 79 seconds**, median **69 seconds**, a **10.4% decrease** relative to the historical 77-second median. The 15% target still failed. Every result, including the slowest, is retained in `benchmarks/baselines/sw2-24-overlap-attempts.json`.

The expanded 19-command fixture inventory is a subsequent implementation change and must be assessed on a new clean exact SHA across at least three complete six-context attempts. Until accepted samples demonstrate the locked performance target, R4 remains **NOT_PROVEN**.

## Third candidate and combined critical-path trial

The expanded 15-group/19-command design with a separate final-gate overlap ran three successful exact-SHA six-context attempts at `c21cd1188d0044f40eb30f6ef3451ffc6d3e2144`, run `37711580993`. Windows durations were **64, 68 and 78 seconds**, median **68 seconds** (11.7% better than the 77-second historical baseline). This still **fails** the required 15% objective; all three, including 78 seconds, are retained in `benchmarks/baselines/sw2-24-expanded-attempts.json`.

The next isolated change is `.github/scripts/ci_parallel_windows.py`: it dispatches the same **19 complete source-regression commands** and **both complete STRICT/VERIFY gates** concurrently under a bounded top-level two-worker coordinator. All subgroups still have bounded three-worker execution; no tests are omitted, interrupted, or replaced with cached PASS. The exact HEAD and governed worktree must remain clean before and after. Ubuntu's 19 serial regressions and full final tests are unchanged. This combined design has no speed claim until three *new* complete exact-SHA attempts pass, and any failure must remain a blocking first-failed gate.

## Combined candidate: measured target achieved

At helper-free exact candidate `8bb6f0f839c8557ecb084cae2df8dfe151169aab`, `Governance CI` run `37713042819` completed **three** full attempts, each with all six permanent contexts SUCCESS. Windows Governance Selftest elapsed times were **49, 68 and 64 seconds**. The full observed sample median is **64 seconds**, a **16.9% decrease** versus the six-successful-run historical 77-second median and above the predeclared **15% reduction** target. All attempts, including 68 seconds, are recorded in `benchmarks/baselines/sw2-24-combined-attempts.json`.

This is an observed, non-randomized hosted-runner comparison, **not** causal proof of hardware-normalized runtime improvement. Median aggregate job-seconds were **199** for the candidate versus **197** for the historical baseline, so there is **no supported cost-saving claim**. Warm/cold runner cache state is `NOT_PROVEN`, and GitHub billing minutes are not inferred from timestamps. The executable CI code and proof above do not substitute for full six-context testing of the final accepted HEAD, identical-tree squash merge, post-merge `main`, and separate terminal governance closure.
