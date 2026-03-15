import argparse
import asyncio
import json
import time
import uuid
import hashlib
from pathlib import Path
from typing import Any

try:
    import httpx  # type: ignore
except ImportError:  # pragma: no cover
    httpx = None
    import urllib.parse
    import urllib.error
    import urllib.request


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


class SimpleResponse:
    def __init__(self, status_code: int, payload: dict[str, Any]):
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, Any]:
        return self._payload

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise RuntimeError(f"HTTP {self.status_code}: {self._payload}")


class StdlibAsyncClient:
    def __init__(self, timeout: float = 180.0):
        self.timeout = timeout

    async def __aenter__(self) -> "StdlibAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    async def post(self, url: str, json: dict[str, Any]) -> SimpleResponse:
        return await asyncio.to_thread(self._request, "POST", url, json)

    async def get(self, url: str, params: dict[str, Any] | None = None) -> SimpleResponse:
        return await asyncio.to_thread(self._request, "GET", url, None, params)

    def _request(
        self,
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        params: dict[str, Any] | None = None,
    ) -> SimpleResponse:
        data = None
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if params:
            query = urllib.parse.urlencode(params, doseq=True)
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}{query}"
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                return SimpleResponse(resp.status, parsed)
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw) if raw else {"detail": raw}
            except json.JSONDecodeError:
                parsed = {"detail": raw}
            return SimpleResponse(e.code, parsed)


def build_session_id(session_prefix: str, case_id: str, experiment_mode: str) -> str:
    """
    Keep session_id <= 64 to satisfy ChatIn validation.
    """
    raw = f"{session_prefix}_{case_id}_{experiment_mode}_{uuid.uuid4().hex[:8]}"
    if len(raw) <= 64:
        return raw

    mode_short_map = {
        "baseline_prompt_only": "bpo",
        "baseline_prompt_only_strong": "bpos",
        "baseline_relational_instruction": "bri",
        "explicit_rel_state_direct": "erd",
        "explicit_rel_state_projected": "erp",
        "explicit_rel_state_direct_oracle": "erdo",
        "explicit_rel_state_projected_oracle": "erpo",
        "baseline_relational_instruction_oracle_collapsed": "bric",
        "baseline_relational_instruction_oracle_collapsed": "bric",
        "explicit_rel_state_direct_vA": "erda",
        "explicit_rel_state_direct_vB": "erdb",
        "explicit_rel_state_direct_vC": "erdc",
        "explicit_rel_state_projected_vA": "erpa",
        "explicit_rel_state_projected_vB": "erpb",
        "explicit_rel_state_projected_vC": "erpc",
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


def extract_case_turns(case: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Support both legacy {"turns": [...]} and long-range
    {"phases": [{"phase": ..., "user_text": ...}, ...]} formats.
    """
    if isinstance(case.get("phases"), list):
        turns: list[dict[str, Any]] = []
        for idx, item in enumerate(case.get("phases") or []):
            if not isinstance(item, dict):
                raise ValueError("each phase item must be a dict")
            user_text = item.get("user_text")
            if not isinstance(user_text, str) or not user_text.strip():
                raise ValueError(f"phase at index {idx} must contain non-empty user_text")
            turns.append(
                {
                    "turn_idx": idx,
                    "phase": str(item.get("phase") or f"phase_{idx}"),
                    "user_text": user_text,
                    "oracle_relational_summary": item.get("oracle_relational_summary"),
                    "oracle_behavior_summary": item.get("oracle_behavior_summary"),
                }
            )
        return turns

    raw_turns = case.get("turns") or []
    if not isinstance(raw_turns, list):
        raise ValueError("case turns must be a list")
    return [
        {
            "turn_idx": idx,
            "phase": None,
            "user_text": str(user_text),
        }
        for idx, user_text in enumerate(raw_turns)
    ]


def extract_boundary_keys(beliefs: list[dict[str, Any]]) -> list[str]:
    keys: list[str] = []
    for b in beliefs or []:
        if not isinstance(b, dict):
            continue
        if b.get("kind") == "boundary" and b.get("key"):
            keys.append(str(b["key"]))
    return keys


async def run_turn(
    client: Any,
    base_url: str,
    session_id: str,
    case_id: str,
    turn_idx: int,
    phase: str | None,
    user_text: str,
    experiment_mode: str,
    oracle_relational_summary: str | None = None,
    oracle_behavior_summary: str | None = None,
) -> dict[str, Any]:
    t0 = time.perf_counter()
    resp = await client.post(
        f"{base_url}/chat",
        json={
            "session_id": session_id,
            "user_text": user_text,
            "experiment_mode": experiment_mode,
            "oracle_relational_summary": oracle_relational_summary,
            "oracle_behavior_summary": oracle_behavior_summary,
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
        "phase": phase,
        "user_text": user_text,
        "assistant_text": reply,
        "oracle_relational_summary": oracle_relational_summary,
        "oracle_behavior_summary": oracle_behavior_summary,
        "boundary_keys": extract_boundary_keys(beliefs),
        "memory_previews": memories,
        "rel_effective": ((policy_view.get("rel") or {}).get("effective") or {}),
        "behavior_effective": policy_view.get("behavior_effective") or {},
        "_last_controller": debug.get("_last_controller") or {},
        "relational_instruction": (((debug.get("_last_controller") or {}).get("notes") or {}).get("relational_instruction")),
        "relational_instruction_labels": (((debug.get("_last_controller") or {}).get("notes") or {}).get("labels") or []),
        "trace_id": debug.get("_last_trace_id"),
        "elapsed_s": round(elapsed_s, 6),
    }


async def run_case(
    client: Any,
    base_url: str,
    case: dict[str, Any],
    experiment_mode: str,
    session_prefix: str,
) -> list[dict[str, Any]]:
    case_id = str(case.get("case_id") or f"case_{uuid.uuid4().hex[:8]}")
    turns = extract_case_turns(case)

    session_id = f"{session_prefix}_{case_id}_{experiment_mode}_{uuid.uuid4().hex[:8]}"
    session_id = build_session_id(session_prefix, case_id, experiment_mode)
    rows: list[dict[str, Any]] = []

    for turn in turns:
        row = await run_turn(
            client=client,
            base_url=base_url,
            session_id=session_id,
            case_id=case_id,
            turn_idx=int(turn["turn_idx"]),
            phase=turn.get("phase"),
            user_text=str(turn["user_text"]),
            experiment_mode=experiment_mode,
            oracle_relational_summary=(turn.get("oracle_relational_summary") if isinstance(turn.get("oracle_relational_summary"), str) else None),
            oracle_behavior_summary=(turn.get("oracle_behavior_summary") if isinstance(turn.get("oracle_behavior_summary"), str) else None),
        )
        rows.append(row)

    return rows


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--cases-json", default="")
    parser.add_argument("--output", default="paper_experiment_results.jsonl")
    parser.add_argument("--session-prefix", default="paper")
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument(
        "--modes",
        nargs="+",
        default=[
            "baseline_prompt_only",
            "baseline_prompt_only_strong",
            "baseline_relational_instruction",
            "explicit_rel_state_direct",
            "explicit_rel_state_projected",
            "explicit_rel_state_direct_oracle",
            "explicit_rel_state_projected_oracle",
        ],
    )
    args = parser.parse_args()

    cases = load_cases(args.cases_json or None)
    if args.max_cases is not None:
        cases = cases[: max(0, args.max_cases)]
    out_path = Path(args.output)

    client_cls = httpx.AsyncClient if httpx is not None else StdlibAsyncClient
    async with client_cls(timeout=180.0) as client:
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
