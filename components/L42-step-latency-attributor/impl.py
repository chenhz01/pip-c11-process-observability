# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L42 — 延迟归因（过程可观测）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l42_attribute(spans):
    """spans: [{"name","kind","ms"}]，kind ∈ wait/compute/retry/idle。
    「一直很慢」不是结论；「60% 花在等」才是。"""
    total = sum(s["ms"] for s in spans)
    if not total:
        return {"total": 0, "by_kind": {}, "verdict": "no-data"}
    by = {}
    for s in spans:
        by[s["kind"]] = by.get(s["kind"], 0) + s["ms"]
    share = {k: round(v / total, 3) for k, v in by.items()}
    top = max(share, key=share.get)
    advice = {
        "wait": "在等：加并行或换更快的提供方；加算力没用",
        "compute": "在算：这是唯一值得加算力的地方",
        "retry": "在重试：先修失败原因，重试不是性能问题",
        "idle": "在空转：排程或调度有问题，先查队列",
    }.get(top, "先分类再看")
    return {"total": total, "by_kind": by, "share": share, "top": top, "advice": advice}


def l42_demo():
    spans = [{"name": "a", "kind": "compute", "ms": 400},
             {"name": "b", "kind": "wait", "ms": 900},
             {"name": "c", "kind": "retry", "ms": 300},
             {"name": "d", "kind": "idle", "ms": 100}]
    r = l42_attribute(spans)
    print("  总计 %dms，占比 %s" % (r["total"], r["share"]))
    print("  主因 %s -> %s" % (r["top"], r["advice"]))


def l42_selftest():
    r = l42_attribute([{"kind": "wait", "ms": 80}, {"kind": "compute", "ms": 20}])
    assert r["share"]["wait"] == 0.8 and r["top"] == "wait"
    assert l42_attribute([])["verdict"] == "no-data"
    return True


if __name__ == "__main__":
    l42_demo()
