# Learning Cards

Each card has four layers: **L0** a twelve-year-old can follow → **L1** the mechanism → **L2** how to use it → **limit** when it fails. Plus the gap evidence.

---

## 过程可观测

> 只看最后一句『我做完了』，中间发生过什么全靠猜。

### L41 · 轨迹最小化

`loop-trace-minifier` · `components/L41-loop-trace-minifier/`

- **L0（人话）** 日志几百行，出事时只想看「谁决定了什么、哪里错了」。这工具把废话去掉，只留能判定的部分。
- **L1（本质）** 五类保留（decide/error/state/tool/retry），其余丢。判据是「删掉这条之后还能不能判定为什么这样走」——所以决策与错误一条都不能少。
- **L2（怎么用）** 事后复盘用；若保留下来的东西里没有 decide 或 error，说明日志设计有问题，先改打点。
- **边界** 保留规则是预设的；领域特有的关键事件要自行加入。
- **空白证据** 日志采样有成熟做法，缺「按可判定性而非比例」的最小化原语（抽样未单列）。

### L42 · 延迟归因

`step-latency-attributor` · `components/L42-step-latency-attributor/`

- **L0（人话）** 「很慢」不是答案。要知道是花在等、在算、在重试，还是在空转——四种情况的解法完全不同。
- **L1（本质）** 把耗时按 wait/compute/retry/idle 分类算占比，给针对性建议。核心：只有 compute 值得加算力；其余三种加算力是白花钱。
- **L2（怎么用）** 性能问题先分类再优化；top=retry 时应该修失败原因，不是加机器。
- **边界** 依赖 span 标注正确；未分类耗时会落到默认桶。
- **空白证据** APM 有 span 分析，缺「按 agent 步骤语义分类」的归因器（抽样未单列）。

### L43 · 无声停滞检测

`silent-stall-detector` · `components/L43-silent-stall-detector/`

- **L0（人话）** 最贵的失败不是报错退出，而是「还在跑，但什么都没发生」，而且没人发现。
- **L1（本质）** 按最后一次进展距今时长占预算比例分档（alive / warning / critical），并报漏掉几次心跳。它把「沉默」变成可报警的事件，而不是靠人偶尔看一眼。
- **L2（怎么用）** 长任务必须打心跳；budget_use ≥0.8 时立刻中断汇报，别等它自己结束。
- **边界** 需要稳定的心跳定义；「进展」若无法打点则不可用。
- **空白证据** 监控的存活探针测进程在不在，缺「有没有实质进展」的判定（抽样 0 命中）。

### L44 · 完成声明核验

`progress-claim-verifier` · `components/L44-progress-claim-verifier/`

- **L0（人话）** 说「我做完了」要有三样东西：真跑过、有产物、有数字。缺一样就只能说「写了但没验」。
- **L1（本质）** 三件证据（run / artifact / number），缺一项即降级。它把汇报用语与证据状态绑定，防止「完成」被当成一种语气。
- **L2（怎么用）** 每次汇报前跑；unverified 时用 must_say 的原句，别自己改写成好听的。
- **边界** 只查证据项是否存在，不查证据是否充分。
- **空白证据** CI 有构建状态，缺「对一句自述做证据核验」的判定器（抽样未单列）。
