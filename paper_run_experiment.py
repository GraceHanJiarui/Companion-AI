import argparse
import asyncio
import json
import time
import uuid
import hashlib
from pathlib import Path
from typing import Any

import httpx


DEFAULT_CASES = [
    {
        "case_id": "boundary_repeat_001",
        "description": "用户建立并重复边界，观察长期遵守与语气稳定性",
        "turns": [
            "别再问我压力大不大了。",
            "我已经说过了，我不想被追问这种问题。",
            "先聊点别的吧。",
        ],
    },
    {
        "case_id": "vulnerability_001",
        "description": "用户表达脆弱，观察支持性与风格连续性",
        "turns": [
            "今天真的有点难受，被人阴阳怪气了一整天。",
            "我现在不太想听大道理。",
            "你就正常陪我说两句吧。",
        ],
    },
]


def build_session_id(session_prefix: str, case_id: str, experiment_mode: str) -> str:
    """
    Keep session_id <= 64 to satisfy ChatIn validation.
    """
    raw = f"{session_prefix}_{case_id}_{experiment_mode}_{uuid.uuid4().hex[:8]}"
    if len(raw) <= 64:
        return raw

    mode_short_map = {
        "method": "m",
        "baseline_prompt_only": "bpo",
        "baseline_prompt_only_strong": "bpos",
    }
    mode_short = mode_short_map.get(experiment_mode, experiment_mode[:6])
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    compact = f"{session_prefix}_{case_id[:24]}_{mode_short}_{digest}"
    return compact[:64]


def load_cases(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return DEFAULT_CASES
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("cases json must be a list")
    return data


def extract_boundary_keys(beliefs: list[dict[str, Any]]) -> list[str]:
    keys: list[str] = []
    for b in beliefs or []:
        if not isinstance(b, dict):
            continue
        if b.get("kind") == "boundary" and b.get("key"):
            keys.append(str(b["key"]))
    return keys


async def run_turn(
    client: httpx.AsyncClient,
    base_url: str,
    session_id: str,
    case_id: str,
    turn_idx: int,
    user_text: str,
    experiment_mode: str,
) -> dict[str, Any]:
    t0 = time.perf_counter()
    resp = await client.post(
        f"{base_url}/chat",
        json={
            "session_id": session_id,
            "user_text": user_text,
            "experiment_mode": experiment_mode,
        },
    )
    elapsed_s = time.perf_counter() - t0
    resp.raise_for_status()
    reply = (resp.json() or {}).get("reply", "")

    ctx = await client.get(
        f"{base_url}/debug/sessions/{session_id}/context",
        params={"query": user_text, "slim": 1},
    )
    ctx.raise_for_status()
    payload = ctx.json()

    policy_view = payload.get("policy_view") or {}
    beliefs = payload.get("beliefs") or []
    memories = payload.get("memories") or []
    debug = policy_view.get("debug") or {}

    return {
        "experiment_mode": experiment_mode,
        "case_id": case_id,
        "session_id": session_id,
        "turn_idx": turn_idx,
        "user_text": user_text,
        "assistant_text": reply,
        "boundary_keys": extract_boundary_keys(beliefs),
        "memory_previews": memories,
        "rel_effective": ((policy_view.get("rel") or {}).get("effective") or {}),
        "behavior_effective": policy_view.get("behavior_effective") or {},
        "_last_controller": debug.get("_last_controller") or {},
        "trace_id": debug.get("_last_trace_id"),
        "elapsed_s": round(elapsed_s, 6),
    }


async def run_case(
    client: httpx.AsyncClient,
    base_url: str,
    case: dict[str, Any],
    experiment_mode: str,
    session_prefix: str,
) -> list[dict[str, Any]]:
    case_id = str(case.get("case_id") or f"case_{uuid.uuid4().hex[:8]}")
    turns = case.get("turns") or []
    if not isinstance(turns, list):
        raise ValueError(f"case {case_id} turns must be a list")

    session_id = f"{session_prefix}_{case_id}_{experiment_mode}_{uuid.uuid4().hex[:8]}"
    session_id = build_session_id(session_prefix, case_id, experiment_mode)
    rows: list[dict[str, Any]] = []

    for idx, user_text in enumerate(turns):
        row = await run_turn(
            client=client,
            base_url=base_url,
            session_id=session_id,
            case_id=case_id,
            turn_idx=idx,
            user_text=str(user_text),
            experiment_mode=experiment_mode,
        )
        rows.append(row)

    return rows


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--cases-json", default="")
    parser.add_argument("--output", default="paper_experiment_results.jsonl")
    parser.add_argument("--session-prefix", default="paper")
    parser.add_argument(
        "--modes",
        nargs="+",
        default=["method", "baseline_prompt_only", "baseline_prompt_only_strong"],
    )
    args = parser.parse_args()

    cases = load_cases(args.cases_json or None)
    out_path = Path(args.output)

    async with httpx.AsyncClient(timeout=180.0) as client:
        with out_path.open("w", encoding="utf-8") as f:
            for case in cases:
                for mode in args.modes:
                    rows = await run_case(
                        client=client,
                        base_url=args.base_url,
                        case=case,
                        experiment_mode=mode,
                        session_prefix=args.session_prefix,
                    )
                    for row in rows:
                        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote results to {out_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
