# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L43 — 无声停滞检测（过程可观测）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l43_stall(last_progress_ts, now, budget, heartbeat_interval=10):
    """没有报错、没有退出、也没有进展——这是最贵的一种失败。"""
    silent = now - last_progress_ts
    used = silent / budget if budget else 1.0
    overdue_beats = silent // heartbeat_interval if heartbeat_interval else 0
    if used >= 0.8:
        verdict, action = "stalled-critical", "立即中断并汇报：已耗尽 %.0f%% 预算无进展" % (used * 100)
    elif used >= 0.4:
        verdict, action = "stalled-warning", "打点汇报一次，并给出「还要多久」的估计"
    else:
        verdict, action = "alive", "继续"
    return {"silent_s": silent, "budget_use": round(used, 3),
            "missed_beats": int(overdue_beats), "verdict": verdict, "action": action}


def l43_demo():
    for s in (5, 45, 95):
        print("  静默 %3ds -> %s" % (s, l43_stall(0, s, 100)))


def l43_selftest():
    assert l43_stall(0, 5, 100)["verdict"] == "alive"
    assert l43_stall(0, 45, 100)["verdict"] == "stalled-warning"
    assert l43_stall(0, 95, 100)["verdict"] == "stalled-critical"
    assert l43_stall(0, 45, 100)["missed_beats"] == 4
    return True


if __name__ == "__main__":
    l43_demo()
