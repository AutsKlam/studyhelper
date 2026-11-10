# 缺陷日志

一条缺陷只记一个可观察现象。日常最少保留 9 个字段；阻塞或跨阶段问题再补全。

| D-ID | stage | symptom | reproduction | impact | trace/evidence | category | root cause | handling | retest | status/owner |
|---|---|---|---|---|---|---|---|---|---|---|
| D-PROC-01 | S0→S1 | S0 已合并，但 NEXT.md 未更新 | 打开远程 NEXT.md | 下一 agent 可能重复 S0 | PR #1 已合并（merge commit `9766507`）；远程 NEXT.md 仍为 S0 / READY / 上次产物“无” | 流程 / 状态同步 | A3 在 S0 合并后未及时更新 NEXT.md | A3 更新状态 | NEXT.md 显示 S1 READY 且链接 PR #1 | fixed / A3 |

记录时间：2026-11-11
