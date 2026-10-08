#!/usr/bin/env python3
"""SW2-24 adversarial regression: no skipped tests, bounded workers and immutable inventory."""
from __future__ import annotations
import concurrent.futures
import importlib.util
import json
import sys
import tempfile
import threading
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".github"/"scripts"))
import ci_parallel_selftests as ci

def main()->int:
    assert len(ci.GROUPS)==7 and ci.MAX_WORKERS==3
    assert ci.GROUP_NAMES==(
        "consumer_finalize","schema_toolchain","analyzer_contract",
        "historical_evidence","public_docs","release_preflight","project_truth_compiler")
    group_commands={name:spec for name, specs in ci.GROUPS for spec in specs}
    assert len(group_commands)==len(ci.GROUPS)
    expected_count=sum(len(scripts) for _,scripts in ci.GROUPS)
    assert expected_count==10,expected_count
    with tempfile.TemporaryDirectory(prefix="sw2-24-ci-parallel-") as td:
        root=Path(td)
        for _,scripts in ci.GROUPS:
            for spec in scripts:
                f=root/spec.split()[0]
                f.parent.mkdir(parents=True,exist_ok=True)
                f.write_text("print('fixture')\n",encoding="utf-8")
        lock=threading.Lock()
        active=[0]
        max_active=[0]
        seen=[]
        def ok(argv,where):
            with lock:
                active[0]+=1
                max_active[0]=max(max_active[0],active[0])
                seen.append(Path(argv[1]).name)
            time.sleep(0.03)
            with lock:
                active[0]-=1
            return 0,"PASS fixture"
        result=ci.run_groups(root,runner=ok)
        assert result["result"]=="PASS",result
        assert result["expected_commands"]==expected_count
        assert result["executed_commands"]==expected_count
        assert max_active[0]>1,"parallel execution never overlapped"
        assert len(seen)==expected_count,"a regression command was skipped"
        assert [x["gate"] for x in result["gates"]]==list(ci.GROUP_NAMES)
        assert len(set(seen))==expected_count
        print("CI_PARALLEL_ALL_COMMANDS_ONCE=PASS")
        print("CI_PARALLEL_BOUNDED_CONCURRENCY=PASS")

        executed=[]
        def failed(argv,where):
            executed.append(Path(argv[1]).name)
            return (3 if Path(argv[1]).name=="selftest_schema_toolchain.py" else 0),"synthetic"
        bad=ci.run_groups(root,runner=failed)
        assert bad["result"]=="FAIL" and bad["executed_groups"]==len(ci.GROUPS)
        assert bad["first_failed_gate"].startswith("schema_toolchain:"),bad
        assert any(x["gate"]=="project_truth_compiler" and x["status"]=="PASS" for x in bad["gates"])
        assert len(executed)==expected_count-1,"group failure should not hide other groups"
        print("CI_PARALLEL_FIRST_FAILED_GATE=PASS")
        print("CI_PARALLEL_NO_GROUP_CANCELLATION=PASS")

        (root/"scripts/selftest_consumer_finalize.py").unlink()
        missing=ci.run_groups(root,runner=ok)
        assert missing["result"]=="FAIL" and missing["first_failed_gate"].startswith("consumer_finalize:"),missing
        assert missing["executed_groups"]==len(ci.GROUPS)
        print("CI_PARALLEL_MISSING_TEST_FAIL_CLOSED=PASS")

        invalid=ci.run_groups(root,workers=ci.MAX_WORKERS+1,runner=ok)
        assert invalid["result"]=="FAIL"
        assert invalid["first_failed_gate"]=="CI_PARALLEL_INVALID_GROUPS_OR_WORKERS"
        print("CI_PARALLEL_UNBOUNDED_WORKERS_REJECTED=PASS")
    print("RESULT=PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
