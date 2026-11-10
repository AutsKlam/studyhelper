# S0 任务卡 — Walking Skeleton

> 状态：READY  
> 阶段：S0（流程演练；不接模型、RAG、Tavily、MySQL、LangGraph、MCP、网页）  
> 时间盒：30 分钟  
> 允许材料：仅 `PLAN.md`、`NEXT.md`、本任务卡；不打开 `agentstudy/`

## 已确认的产品定位

- 场景：Agent 面试热点简报。
- 用户 / 决策：准备 Agent 岗面试的你；决定“今天 25 分钟学哪个主题”。
- 输出：6 个内容字段 + `run` 元数据。

成功 fixture 问题固定为：`最近 7 天 Agent 评测方向有什么值得我花 25 分钟跟进的主题？`

## 三源问题（S1/S2 目标；S0 不实现）

- 本地 RAG：我对 LangGraph 检查点或评测的笔记有哪些？
- Tavily：最近 7 天 Agent 评测、架构有哪些新文章或发布？
- MySQL：`materials_meta` 中 `topic=eval/interview` 的资料及适用阶段是什么？
- 必拒答反例：替我编项目指标或 STAR 结果；要求把 10 份资料全文总结。

## U3 不可接受错误（S1 起验证）

- 把学习资料当项目证据。
- 编造面试题来源、项目指标或 STAR 结果。
- 结论没有材料定位或来源类型。
- 把“看过”当掌握；把资料全文堆砌当简报。
- 越权读取、密钥入库、任意 SQL 或写操作。

## stage

S0

## artifact

一个可运行的 `evibrief ask` walking skeleton：单命令、本地 fixture、固定 JSON 输出、一个成功检查、一个失败检查、一个小 PR。

## user / decision

准备 Agent 岗面试的你；决定“今天 25 分钟学哪个主题”。

## in scope

1. 从仓库根目录运行：`python -m evibrief ask --fixture fixtures/s0_question.txt`。
2. 成功时输出固定 JSON；至少 1 条带 `source_type` / `locator` 的本地证据占位，至少 1 条笔记映射。
3. 至少两个可读失败：空问题/空文件和 fixture 不存在；非 0 退出，不得静默崩溃。
4. 一个小 PR：变更地图、成功/失败运行证据、回滚点。

## non-goals

- 不接模型、RAG、Tavily、MySQL、LangGraph、MCP、网页。
- 不实现真实检索、评测、多 agent、记忆、前端。
- 不写业务逻辑；不做生产级 UI 或 PDF 导出。
- 不修改 `agentstudy/`，不读取其中的学习资料。

## acceptance

- A1：从仓库根目录执行 `python -m evibrief ask --fixture fixtures/s0_question.txt`，退出码 0，stdout 为合法 JSON。
- A2：JSON 恰含 6 个内容字段 `topic`、`evidence`、`notes_mapping`、`gaps`、`next_action`、`self_check`，外加 `run`；`evidence` 至少 1 条且含 `claim`、`snippet`、`source_type`、`locator`、`date`；`notes_mapping` 至少 1 条且含 `note`、`relation`、`locator`。
- A3：空问题/空文件返回非 0，输出 `error.code=EMPTY_QUESTION`；不存在的 fixture 返回非 0，输出 `error.code=FIXTURE_NOT_FOUND`；两者都有可读 `message`。
- A4：仅使用本地 fixture 与标准库；代码、日志、依赖中无模型/RAG/Tavily/MySQL/LangGraph/MCP/网页调用；无密钥、无越界路径。
- A5：小 PR 含变更文件地图（逐文件映射 A1–A5）、成功/失败运行记录、回滚点；未直接推 main，未夹带 S1 功能。

## counterexample

- 输入为空字符串或 `fixtures/s0_empty.txt` 为空：必须返回 `EMPTY_QUESTION`，不得输出“今日焦点主题”。
- 指定 `fixtures/does-not-exist.txt`：必须返回 `FIXTURE_NOT_FOUND`，不得伪造证据。
- S1 起追加：输入“替我编一个项目指标或 STAR 结果”必须拒答；S0 只记录，不实现。

## output contract

成功输出（stdout，退出码 0）：

```json
{
  "topic": "S0 占位主题：Agent 评测",
  "evidence": [
    {
      "claim": "S0 占位结论：仅验证输出结构，不代表真实资讯",
      "snippet": "S0 占位资料：这不是学习资料，仅用于验证证据字段。",
      "source_type": "local",
      "locator": "fixtures/s0_note.md#L1-L3",
      "date": "2026-11-11"
    }
  ],
  "notes_mapping": [
    {
      "note": "S0 占位笔记",
      "relation": "supports",
      "locator": "fixtures/s0_note.md#L1-L3"
    }
  ],
  "gaps": [],
  "next_action": {
    "minutes": 25,
    "action": "S0 占位动作：确认输出结构"
  },
  "self_check": [
    "输出字段是否齐全",
    "证据是否有可定位来源"
  ],
  "run": {
    "run_id": "s0-<timestamp-or-uuid>",
    "elapsed_ms": 0,
    "prompt_version": "s0-placeholder",
    "materials_version": "s0-fixture-v1"
  }
}
```

失败输出（stdout，退出码非 0）：

```json
{
  "error": {
    "code": "EMPTY_QUESTION",
    "message": "可读错误说明"
  }
}
```

```json
{
  "error": {
    "code": "FIXTURE_NOT_FOUND",
    "message": "可读错误说明"
  }
}
```

约束：

- `source_type` 只能是 `local`、`web`、`db`；S0 只允许 `local`。
- `notes_mapping.relation` 只能是 `supports`、`contradicts`、`missing`。
- 成功输出不得缺少字段；空数组可以接受，但 `evidence` 和 `notes_mapping` 至少各 1 条。
- 不把占位内容伪装成真实资讯或真实项目证据。
- S1 起再增加“证据不足拒答”对象；S0 只做结构错误。

## timebox

30 分钟；到点停止并回报，不自动扩范围。

## allowed materials

仅 `PLAN.md`、`NEXT.md`、本任务卡。S0 不打开 `agentstudy/`。
