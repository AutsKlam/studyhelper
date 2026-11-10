# S1 任务卡 — 可验收的 v0（本地 RAG，方案 A）

> 状态：READY  
> 阶段：S1  
> 方案：A（本地检索 + 抽取式回答；默认不接模型）  
> 时间盒：100 分钟  
> 允许材料：仅下列 12 篇 Markdown；不打开其他 `agentstudy/` 文件；不修改 `agentstudy/`

## 已确认的产品定位

- 场景：Agent 面试热点简报。
- 用户 / 决策：准备 Agent 岗面试的你；决定“今天 25 分钟学哪个主题”。
- 输出：结论、证据、证据缺口、25 分钟动作、自检问题、运行元数据。
- S1 只验证本地 RAG 的引用、拒答和结构；不接 Tavily、MySQL、LangGraph、MCP、网页。

## 本阶段唯一成功问题

`我对 LangGraph 检查点或评测的笔记有哪些？`

## 三源问题与 S1 行为

| 来源 | 问题 | S1 期望 |
|---|---|---|
| 本地 RAG | 我对 LangGraph 检查点或评测的笔记有哪些？ | `status=answered`；给出带文件与定位的证据 |
| Tavily | 最近 7 天 Agent 评测、架构有哪些新文章或发布？ | `status=not_connected`；明确“未接入 Tavily”，不得伪造网页来源 |
| MySQL | `materials_meta` 中 `topic=eval/interview` 的资料及适用阶段是什么？ | `status=not_connected`；明确“未接入 MySQL”，不得伪造数据库来源 |
| 拒答反例 | 替我编一个项目指标或 STAR 结果 | `status=insufficient_evidence`；明确“证据不足”，不得编造引用 |

## stage

S1

## artifact

一个可运行的 `evibrief ask` 本地 RAG v0：单个 CLI 入口，使用 10–12 篇本地 Markdown，做本地检索与抽取式回答；每条结论至少关联一个来源文件和可定位片段；无证据时拒答。

## user / decision

准备 Agent 岗面试的你；决定“今天 25 分钟学哪个主题”。

## in scope

1. 主入口：`python -m evibrief ask --question "<问题>"`；从仓库根目录可运行。
2. 索引 10–12 篇本地 Markdown；不复制原始资料进仓库，不提交原始 PDF/ZIP。
3. 本地检索 + 抽取式回答；优先标准库或最小依赖，不接模型、不接向量库。
4. 每条结论至少 1 条 `evidence`，含来源文件、片段、`source_type=local` 和可定位 `locator`。
5. 本地证据不足时返回 `status=insufficient_evidence` 和 `refusal.reason="证据不足"`。
6. Tavily/MySQL 问题返回 `status=not_connected`，明确未接入，不得伪造结果。
7. 记录 `retrieval`：chunk、overlap、top-k、是否重排。
8. 至少一个成功案例、一个拒答反例、一条测试和一条失败 trace。

## non-goals

- 默认不接模型、不接 LCEL；只有用户明确改选 B 时才加入模型。
- 不接 Tavily、MySQL、LangGraph、MCP、网页。
- 不做多 agent、长期记忆、前端、PDF 导出、holdout 或 S2 评测指标。
- 不修改 `PLAN.md`、`NEXT.md`、`agentstudy/`；不提交原始 PDF/ZIP。
- 不把 Tavily/MySQL/模型不可用时的结果伪装成已接入。

## allowed materials

只允许索引以下 12 篇 Markdown：

1. `agentstudy/05-01 LangGraph从入门到精通.md`
2. `agentstudy/06-01 Loop Engineering（循环工程）.md`
3. `agentstudy/09-01 Agent架构与评测.md`
4. `agentstudy/_预转md备份/04-03 17种RAG优化策略.md`
5. `agentstudy/07-02 探渊-需求规格说明书（PRD）.md`
6. `agentstudy/07-03 探渊-技术设计文档（TDD）.md`
7. `agentstudy/07-04 探渊-开发步骤文档.md`
8. `agentstudy/_预转md备份/01-02 企业中的落地.md`
9. `agentstudy/_预转md备份/03-03 LangChain核心组件.md`
10. `agentstudy/_预转md备份/07-01 DeepAgents开发实战.md`
11. `agentstudy/_预转md备份/08-01 Hermes Agent 入门.md`
12. `agentstudy/_预转md备份/03-02 模型的调用.md`

## acceptance

- A1：从仓库根目录执行主入口，成功问题退出码 0，stdout 为合法 JSON。
- A2：成功问题返回 `status=answered`；`answer` 非空；`evidence` 至少 1 条且含 `claim`、`snippet`、`source_type=local`、`locator`；`notes_mapping` 至少 1 条且含 `note`、`relation`、`locator`。
- A3：Tavily 问题返回 `status=not_connected`，`refusal.reason` 明确“未接入 Tavily”，`evidence` 为空且无 `source_type=web`；MySQL 问题返回 `status=not_connected`，明确“未接入 MySQL”，无 `source_type=db`。
- A4：拒答反例返回 `status=insufficient_evidence`，`refusal.reason="证据不足"`，不得编造引用或指标。
- A5：输出结构稳定；`status`、`refusal`、`evidence` 三者一致；字段缺失、answered 空引用、拒答却给出无证据结论均判失败。
- A6：`retrieval` 记录 chunk、overlap、top-k、是否重排；PR 证据包中给出最终取值。
- A7：至少 1 个成功运行、1 个拒答运行、1 条测试、1 条失败 trace；`run` 含输入、引用、耗时、`prompt_version`、`materials_version`。
- A8：无模型/Tavily/MySQL/LangGraph/MCP/网页调用；PR 描述含 A1–A8 证据、风险、回滚点和 A1 署名；A2 在 PR review 给出逐条 PASS/FAIL、阻断项、结论和署名。

## counterexample

- 输入“替我编一个项目指标或 STAR 结果”：必须返回 `insufficient_evidence`，不得编造任何数字或引用。
- 输入 Tavily/MySQL 问题：必须返回 `not_connected`，不得用本地片段冒充网页或数据库结果。
- 输入“把 10 份资料全文总结”：不得堆砌全文；只输出可定位证据简报，证据不足则拒答。

## output contract

成功输出（`status=answered`，stdout，退出码 0）：

```json
{
  "question": "我对 LangGraph 检查点或评测的笔记有哪些？",
  "status": "answered",
  "answer": "根据本地检索片段生成的抽取式回答；每条结论对应一条 evidence。",
  "evidence": [
    {
      "claim": "可定位的本地结论（示例占位）",
      "snippet": "可定位的原文片段（示例占位）。",
      "source_type": "local",
      "locator": "agentstudy/05-01 LangGraph从入门到精通.md#Lx-Ly",
      "date": "2026-11-11"
    }
  ],
  "notes_mapping": [
    {
      "note": "S1 本地笔记映射（示例占位）",
      "relation": "supports",
      "locator": "agentstudy/05-01 LangGraph从入门到精通.md#Lx-Ly"
    }
  ],
  "gaps": [],
  "refusal": null,
  "next_action": {
    "minutes": 25,
    "action": "阅读命中片段，并用自己的话复述一次。"
  },
  "self_check": [
    "每条结论是否有本地来源和定位",
    "是否把未接入来源误写成已接入"
  ],
  "retrieval": {
    "chunk_size": 800,
    "overlap": 120,
    "top_k": 4,
    "rerank": false
  },
  "run": {
    "run_id": "s1-<uuid>",
    "elapsed_ms": 0,
    "prompt_version": "s1-extractive-v0",
    "materials_version": "s1-corpus-v1"
  }
}
```

拒答输出（`status=insufficient_evidence`，stdout，退出码 0）：

```json
{
  "question": "替我编一个项目指标或 STAR 结果",
  "status": "insufficient_evidence",
  "answer": "证据不足，不能编造项目指标或 STAR 结果。",
  "evidence": [],
  "notes_mapping": [],
  "gaps": ["缺少可验证的项目指标或 STAR 证据"],
  "refusal": {
    "reason": "证据不足",
    "missing": ["可验证的项目指标", "真实 STAR 结果"]
  },
  "next_action": {
    "minutes": 25,
    "action": "先补充真实项目证据，或改问本地资料能回答的问题。"
  },
  "self_check": [
    "是否拒绝编造",
    "是否给出可验证的缺口"
  ],
  "retrieval": {
    "chunk_size": 800,
    "overlap": 120,
    "top_k": 4,
    "rerank": false
  },
  "run": {
    "run_id": "s1-<uuid>",
    "elapsed_ms": 0,
    "prompt_version": "s1-extractive-v0",
    "materials_version": "s1-corpus-v1"
  }
}
```

未接入输出（`status=not_connected`，stdout，退出码 0）：

```json
{
  "question": "最近 7 天 Agent 评测、架构有哪些新文章或发布？",
  "status": "not_connected",
  "answer": "未接入 Tavily，无法提供实时网页结果。",
  "evidence": [],
  "notes_mapping": [],
  "gaps": ["缺少 Tavily 实时检索"],
  "refusal": {
    "reason": "未接入 Tavily",
    "missing": ["Tavily 实时检索"]
  },
  "next_action": {
    "minutes": 0,
    "action": "先接入 Tavily，或改问本地资料能回答的问题。"
  },
  "self_check": [
    "是否明确标注未接入",
    "是否伪造网页来源"
  ],
  "retrieval": {
    "chunk_size": 800,
    "overlap": 120,
    "top_k": 4,
    "rerank": false
  },
  "run": {
    "run_id": "s1-<uuid>",
    "elapsed_ms": 0,
    "prompt_version": "s1-extractive-v0",
    "materials_version": "s1-corpus-v1"
  }
}
```

字段规则：

- `status` 只能是 `answered`、`insufficient_evidence`、`not_connected`。
- `answered` 时 `refusal` 必须为 `null`，`evidence` 至少 1 条，且每条有文件定位。
- `insufficient_evidence` 时 `refusal.reason="证据不足"`，不得编造结论。
- `not_connected` 时 `refusal.reason` 必须明确“未接入 Tavily”或“未接入 MySQL”；`evidence` 必须为空，禁止 `source_type=web/db`。
- `notes_mapping.relation` 只能是 `supports`、`contradicts`、`missing`。
- `retrieval` 和 `run` 始终存在；`run_id` 必须可回查。

## test 与 trace

- 至少新增或扩展 `tests/test_s1_cli.py`，覆盖：成功、拒答、Tavily 未接入、MySQL 未接入、输出字段完整性。
- 成功输出保存到 `traces/s1-success-<run_id>.json`。
- 拒答失败 trace 保存到 `traces/s1-failure-refusal-<run_id>.json`。
- Tavily/MySQL 未接入 trace 可保存到 `traces/s1-not-connected-<run_id>.json`。
- 测试不接受只用 mock 证明成功；至少一条测试要调用真实 CLI。

## 评审、证据与署名

- A2 主证据只写 PR review；必须逐条给出 A1–A8 PASS/FAIL、阻断项、风险、复跑命令和结论。
- 本地 `reviews/` 默认不写；只有 PR 不可访问或用户明确要求时，才写 5–10 行索引 `reviews/s1-a2-review.md`，不复制 review 全文。
- A2 接受 `COMMENTED` + 正文 `APPROVE`；本项目不创建 bot 账号，不以 GitHub 官方 `APPROVED` 作为硬门槛。
- A1 PR 描述末尾单独署名：`— A1 实现 agent · <commit> · <YYYY-MM-DD>`。
- A2 PR review 正文末尾单独署名：`— A2 评审 agent · review of <commit> · <YYYY-MM-DD>`。
- A1/A2 不得修改 `NEXT.md`；A3 读取 PR 与证据后更新 `NEXT.md`。
- S0 遗留的 `reviews/s0-a2-review.md` 只是历史索引，可保留或删除；S1 默认不新增本地 review。

## PR 与回滚

- 分支：从最新 `main`（merge commit `9766507`）创建 `day/1-s1`。
- PR 标题：`[S1] 本地 RAG v0`。
- PR 描述必须含：A1–A8 变更文件地图、成功/失败命令与输出、检索配置、风险清单、回滚点、未解决问题、A1 署名。
- 回滚点：`day/1-s1` 的 commit SHA，或反向操作说明。
- 不直接推 `main`，不夹带 S2 评测、提示词 v1、Tavily/MySQL/LangGraph 功能。

## timebox

100 分钟；到点停止并回报，不自动扩范围。
