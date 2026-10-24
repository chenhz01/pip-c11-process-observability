# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L43 selftest — 断言写在实现旁边，改坏了立刻红。"""
import impl


def main():
    impl.l43_selftest()
    print("PASS L43 silent-stall-detector")


if __name__ == "__main__":
    main()
