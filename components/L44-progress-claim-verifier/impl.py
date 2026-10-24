# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L44 — 完成声明核验（过程可观测）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l44_verify(claim, evidence):
    """把「我完成了」拆成必须存在的证据项；缺一项就不许标完成。"""
    required = ["run", "artifact", "number"]
    have = set(evidence)
    missing = [r for r in required if r not in have]
    return {
        "claim": claim,
        "verified": not missing,
        "missing": missing,
        "verdict": "verified" if not missing else ("partial" if len(missing) == 1 else "unverified"),
        "must_say": None if not missing else "只能说「已写入但未验证」，不能说「完成」",
    }


def l44_demo():
    for ev in (["run", "artifact", "number"], ["artifact"], []):
        r = l44_verify("55 件全部做完", ev)
        print("  证据%s -> %-10s 缺%s" % (ev, r["verdict"], r["missing"]))


def l44_selftest():
    assert l44_verify("x", ["run", "artifact", "number"])["verified"] is True
    assert l44_verify("x", ["run", "artifact"])["verdict"] == "partial"
    assert l44_verify("x", [])["verdict"] == "unverified"
    return True


if __name__ == "__main__":
    l44_demo()
