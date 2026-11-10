from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Sequence

PROMPT_VERSION = "s0-placeholder"
MATERIALS_VERSION = "s0-fixture-v1"
FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _error_payload(code: str, message: str) -> dict[str, Any]:
    return {"error": {"code": code, "message": message}}


def _success_payload(started_at: float) -> dict[str, Any]:
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    return {
        "topic": "S0 占位主题：Agent 评测",
        "evidence": [
            {
                "claim": "S0 占位结论：仅验证输出结构，不代表真实资讯",
                "snippet": "S0 占位资料：这不是学习资料，仅用于验证证据字段。",
                "source_type": "local",
                "locator": "fixtures/s0_note.md#L1-L3",
                "date": "2026-11-11",
            }
        ],
        "notes_mapping": [
            {
                "note": "S0 占位笔记",
                "relation": "supports",
                "locator": "fixtures/s0_note.md#L1-L3",
            }
        ],
        "gaps": [],
        "next_action": {
            "minutes": 25,
            "action": "S0 占位动作：确认输出结构",
        },
        "self_check": [
            "输出字段是否齐全",
            "证据是否有可定位来源",
        ],
        "run": {
            "run_id": f"s0-{uuid.uuid4().hex}",
            "elapsed_ms": elapsed_ms,
            "prompt_version": PROMPT_VERSION,
            "materials_version": MATERIALS_VERSION,
        },
    }


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="evibrief")
    subparsers = parser.add_subparsers(dest="command", required=True)
    ask_parser = subparsers.add_parser("ask", help="Generate an S0 placeholder brief")
    ask_parser.add_argument(
        "--fixture",
        required=True,
        help="Path to a local question fixture",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    started_at = time.perf_counter()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _parse_args(argv)
    fixture_path = Path(args.fixture)
    try:
        resolved_fixture = fixture_path.resolve()
    except (OSError, RuntimeError) as exc:
        _emit(
            _error_payload(
                "FIXTURE_NOT_FOUND",
                f"无法解析本地 fixture 路径：{fixture_path}（{exc}）",
            )
        )
        return 2

    if not resolved_fixture.is_relative_to(FIXTURES_ROOT):
        _emit(
            _error_payload(
                "FIXTURE_NOT_FOUND",
                "只允许读取仓库 fixtures 目录内的本地问题文件。",
            )
        )
        return 2

    if not resolved_fixture.is_file():
        _emit(
            _error_payload(
                "FIXTURE_NOT_FOUND",
                f"找不到本地 fixture：{fixture_path}",
            )
        )
        return 2

    try:
        question = resolved_fixture.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        _emit(
            _error_payload(
                "FIXTURE_NOT_FOUND",
                f"无法读取本地 fixture：{fixture_path}（{exc}）",
            )
        )
        return 2

    if not question.strip():
        _emit(
            _error_payload(
                "EMPTY_QUESTION",
                "问题内容为空；请提供非空的本地问题 fixture。",
            )
        )
        return 2

    _emit(_success_payload(started_at))
    return 0


if __name__ == "__main__":
    sys.exit(main())
