# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L41 — 轨迹最小化（过程可观测）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


_KEEP = ("decide", "error", "state", "tool", "retry")


def l41_minify(events, keep_kinds=_KEEP):
    """只留「可判定信息」：决策、错误、状态变化、工具调用、重试。

    丢掉的是：思考碎念、重复确认、纯输出。
    判据：删掉这条之后，还能不能判定「这一步为什么这样走」。
    """
    kept, dropped = [], 0
    for e in events:
        if e.get("kind") in keep_kinds:
            kept.append({"i": e.get("i"), "kind": e["kind"], "text": e.get("text", "")[:80]})
        else:
            dropped += 1
    n = len(events)
    return {
        "原始条数": n,
        "保留条数": len(kept),
        "压缩比": round(1 - len(kept) / n, 3) if n else 0.0,
        "kept": kept,
        "dropped": dropped,
        "verdict": "可判定信息仍在" if any(k["kind"] in ("decide", "error") for k in kept) else "风险：决策与错误都没留",
    }


def l41_demo():
    events = [
        {"i": 0, "kind": "think", "text": "我想想"},
        {"i": 1, "kind": "decide", "text": "先跑基准再写文档"},
        {"i": 2, "kind": "tool", "text": "run bench"},
        {"i": 3, "kind": "error", "text": "float noise r=0.9999"},
        {"i": 4, "kind": "think", "text": "嗯"},
        {"i": 5, "kind": "state", "text": "8/8 PASS"},
        {"i": 6, "kind": "out", "text": "长文本输出"},
    ]
    r = l41_minify(events)
    print("  %d -> %d 条（压缩 %.0f%%）| %s" % (r["原始条数"], r["保留条数"], r["压缩比"] * 100, r["verdict"]))
    print("  保留:", [(k["kind"], k["text"][:20]) for k in r["kept"]])


def l41_selftest():
    r = l41_minify([{"i": 0, "kind": "think", "text": "x"},
                    {"i": 1, "kind": "decide", "text": "y"},
                    {"i": 2, "kind": "error", "text": "z"}])
    assert r["保留条数"] == 2 and r["压缩比"] == round(1 - 2 / 3, 3)
    assert l41_minify([{"i": 0, "kind": "think", "text": "x"}])["verdict"].startswith("风险")
    return True


if __name__ == "__main__":
    l41_demo()
