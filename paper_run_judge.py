import argparse
import asyncio
import json
import random
import re
from pathlib import Path
from typing import Any

from app.core.llm_client import LLMClient


CASE_SYSTEM_BASE = """You are evaluating a long-horizon dialogue case.

Your task is to judge whether this full multi-turn dialogue feels like one coherent
relationship process unfolding over time, rather than a sequence of locally plausible
but interactionally reset replies.

Evaluation priorities:
1. Judge only from user turns and assistant turns.
2. Prioritize cross-turn continuity over single-turn elegance.
3. Do not reward verbosity or generic helpfulness by default.
4. A mild tone change is not automatically an abrupt shift if it still fits the same
   ongoing interaction process.

An abrupt shift may include:
- unsupported warmth increase
- unsupported distance increase
- compensatory warmth after the user has cooled interaction down
- reopening continuation or final-probe behavior beyond what the trajectory supports
"""

PAIRWISE_SYSTEM_BASE = """You are comparing two long-horizon dialogue trajectories for relational coherence.

Your task is to decide which trajectory better preserves the same ongoing
relationship process across turns.

Evaluation priorities:
1. Do not reward verbosity, elegance, or generic helpfulness by default.
2. Prefer the trajectory with less abrupt relational shift.
3. Prefer the trajectory with less overinterpretation and less compensatory warmth.
4. Prefer the trajectory that keeps ordinary continuation and final-probe turns under control.
5. If both are close, return tie.
"""

CASE_VARIANT_SUFFIX = {
    "a": "Be conservative and only mark an abrupt shift when the break is supported by clear cross-turn evidence.",
    "b": "Treat coherence as a trajectory property; do not overweight one polished turn if the cross-turn stance is unstable.",
    "c": "When in doubt, prefer the trajectory reading that best preserves the same ongoing relationship stance over time.",
}

PAIRWISE_VARIANT_SUFFIX = {
    "a": "Prefer the trajectory that remains most stable from early turns through ordinary continuation and final probe.",
    "b": "When both trajectories are locally plausible, choose the one with fewer cross-turn stance resets.",
    "c": "Use tie when the difference is minor; otherwise prefer the more trajectory-consistent system.",
}


def render_dialogue_block(turns: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for turn in turns:
        idx = int(turn.get("turn_idx") or 0)
        phase = str(turn.get("phase") or "unknown_phase")
        user_text = str(turn.get("user_text") or "").strip()
        assistant_text = str(turn.get("assistant_text") or "").strip()
        lines.extend(
            [
                f"Turn {idx} ({phase})",
                f"User: {user_text}",
                f"Assistant: {assistant_text}",
                "",
            ]
        )
    return "\n".join(lines).strip()


def extract_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1:
        raise ValueError(f"Could not find JSON object in response: {text[:300]}")
    if end == -1 or end < start:
        snippet = text[start:]
    else:
        snippet = text[start : end + 1]
    try:
        return json.loads(snippet)
    except json.JSONDecodeError:
        repaired = re.sub(r"[\u201c\u201d]", '"', snippet)
        repaired = re.sub(r"[\u2018\u2019]", '"', repaired)
        repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            partial: dict[str, Any] = {}
            pair_pattern = re.compile(
                r'"(?P<key>[^"]+)"\s*:\s*(?P<value>true|false|null|-?\d+(?:\.\d+)?|"[^"]*"|\[[^\]]*\])',
                re.DOTALL,
            )
            for match in pair_pattern.finditer(repaired):
                key = match.group("key")
                raw_value = match.group("value")
                try:
                    partial[key] = json.loads(raw_value)
                except json.JSONDecodeError:
                    continue
            if partial:
                return partial
            raise ValueError(f"Could not parse JSON object in response: {text[:300]}")


def normalize_case_result(item: dict[str, Any], parsed: dict[str, Any], run_name: str) -> dict[str, Any]:
    return {
        "judge_run": run_name,
        "case_id": str(item.get("case_id")),
        "experiment_mode": str(item.get("experiment_mode")),
        "trajectory_continuity_1_to_5": int(parsed.get("trajectory_continuity_1_to_5", 0)),
        "user_request_preservation_1_to_5": int(parsed.get("user_request_preservation_1_to_5", 0)),
        "overinterpretation_1_to_5": int(parsed.get("overinterpretation_1_to_5", 0)),
        "continuation_probe_control_1_to_5": int(parsed.get("continuation_probe_control_1_to_5", 0)),
        "unsupported_warmth_increase": bool(parsed.get("unsupported_warmth_increase", False)),
        "unsupported_distance_increase": bool(parsed.get("unsupported_distance_increase", False)),
        "unsupported_initiative_jump": bool(parsed.get("unsupported_initiative_jump", False)),
        "continuation_reopen_after_cooling": bool(parsed.get("continuation_reopen_after_cooling", False)),
        "final_probe_overshoot": bool(parsed.get("final_probe_overshoot", False)),
        "trajectory_reset_present": bool(parsed.get("trajectory_reset_present", False)),
        "has_abrupt_shift": bool(parsed.get("has_abrupt_shift", False)),
        "abrupt_shift_turns": [int(x) for x in (parsed.get("abrupt_shift_turns") or [])],
        "overall_relational_coherence_1_to_5": int(parsed.get("overall_relational_coherence_1_to_5", 0)),
        "reason": str(parsed.get("reason") or "").strip(),
    }


def normalize_pairwise_result(
    item: dict[str, Any],
    parsed: dict[str, Any],
    run_name: str,
    *,
    swap_lr: bool,
) -> dict[str, Any]:
    winner = str(parsed.get("winner") or "").strip().lower()
    if winner not in {"left", "right", "tie"}:
        winner = "tie"
    if swap_lr:
        if winner == "left":
            winner = "right"
        elif winner == "right":
            winner = "left"
    return {
        "judge_run": run_name,
        "case_id": str(item.get("case_id")),
        "comparison_type": str(item.get("comparison_type")),
        "left_experiment_mode": str((item.get("left") or {}).get("experiment_mode") or ""),
        "right_experiment_mode": str((item.get("right") or {}).get("experiment_mode") or ""),
        "winner": winner,
        "better_on_trajectory_continuity": str(parsed.get("better_on_trajectory_continuity") or "tie").strip().lower(),
        "better_on_request_preservation": str(parsed.get("better_on_request_preservation") or "tie").strip().lower(),
        "better_on_shift_control": str(parsed.get("better_on_shift_control") or "tie").strip().lower(),
        "reason": str(parsed.get("reason") or "").strip(),
    }


def build_case_prompt(item: dict[str, Any]) -> tuple[str, str]:
    dialogue = render_dialogue_block(item.get("turns") or [])
    system = CASE_SYSTEM_BASE
    user = f"""Return JSON with exactly these fields:
{{
  "trajectory_continuity_1_to_5": 1-5 integer,
  "user_request_preservation_1_to_5": 1-5 integer,
  "overinterpretation_1_to_5": 1-5 integer,
  "continuation_probe_control_1_to_5": 1-5 integer,
  "unsupported_warmth_increase": true/false,
  "unsupported_distance_increase": true/false,
  "unsupported_initiative_jump": true/false,
  "continuation_reopen_after_cooling": true/false,
  "final_probe_overshoot": true/false,
  "trajectory_reset_present": true/false,
  "has_abrupt_shift": true/false,
  "abrupt_shift_turns": [turn indices or empty array],
  "overall_relational_coherence_1_to_5": 1-5 integer,
  "reason": "1-4 sentence explanation"
}}

Dialogue:
{dialogue}
"""
    return system, user


def build_pairwise_prompt(item: dict[str, Any], *, swap_lr: bool) -> tuple[str, str]:
    left = item.get("left") or {}
    right = item.get("right") or {}
    left_dialogue = render_dialogue_block((right if swap_lr else left).get("turns") or [])
    right_dialogue = render_dialogue_block((left if swap_lr else right).get("turns") or [])
    system = PAIRWISE_SYSTEM_BASE
    user = f"""Return JSON with exactly these fields:
{{
  "winner": "left" | "right" | "tie",
  "better_on_trajectory_continuity": "left" | "right" | "tie",
  "better_on_request_preservation": "left" | "right" | "tie",
  "better_on_shift_control": "left" | "right" | "tie",
  "reason": "1-4 sentence explanation"
}}

Left dialogue:
{left_dialogue}

Right dialogue:
{right_dialogue}
"""
    return system, user


async def run_case_items(
    *,
    items: list[dict[str, Any]],
    client: LLMClient,
    run_name: str,
    variant: str,
    temperature: float | None,
    max_output_tokens: int,
    concurrency: int,
    out_path: Path,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)
    existing = load_existing_results(out_path, ["case_id", "experiment_mode"])
    results: list[dict[str, Any] | None] = [None] * len(items)
    write_lock = asyncio.Lock()

    async def worker(i: int, item: dict[str, Any]) -> None:
        key = (str(item.get("case_id") or ""), str(item.get("experiment_mode") or ""))
        if key in existing:
            results[i] = existing[key]
            return
        async with semaphore:
            last_err: Exception | None = None
            for _ in range(3):
                try:
                    system, user = build_case_prompt(item)
                    system = f"{system}\n{CASE_VARIANT_SUFFIX[variant]}"
                    text = await client.generate(
                        system=system,
                        user=user,
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                        reasoning_effort="low",
                        text_verbosity="low",
                        timeout_s=120.0,
                    )
                    parsed = extract_json(text)
                    results[i] = normalize_case_result(item, parsed, run_name)
                    async with write_lock:
                        write_json(out_path, [x for x in results if x is not None])
                    return
                except Exception as err:
                    last_err = err
            raise RuntimeError(f"Case judge failed for {key}: {last_err}") from last_err

    await asyncio.gather(*(worker(i, item) for i, item in enumerate(items)))
    return [x for x in results if x is not None]


async def run_pairwise_items(
    *,
    items: list[dict[str, Any]],
    client: LLMClient,
    run_name: str,
    variant: str,
    temperature: float | None,
    max_output_tokens: int,
    concurrency: int,
    seed: int,
    out_path: Path,
) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency)
    rng = random.Random(seed)
    swap_flags = [bool(rng.randint(0, 1)) for _ in items]
    existing = load_existing_results(out_path, ["case_id", "comparison_type"])
    results: list[dict[str, Any] | None] = [None] * len(items)
    write_lock = asyncio.Lock()

    async def worker(i: int, item: dict[str, Any]) -> None:
        key = (str(item.get("case_id") or ""), str(item.get("comparison_type") or ""))
        if key in existing:
            results[i] = existing[key]
            return
        async with semaphore:
            swap_lr = swap_flags[i]
            last_err: Exception | None = None
            for _ in range(3):
                try:
                    system, user = build_pairwise_prompt(item, swap_lr=swap_lr)
                    system = f"{system}\n{PAIRWISE_VARIANT_SUFFIX[variant]}"
                    text = await client.generate(
                        system=system,
                        user=user,
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                        reasoning_effort="low",
                        text_verbosity="low",
                        timeout_s=120.0,
                    )
                    parsed = extract_json(text)
                    results[i] = normalize_pairwise_result(item, parsed, run_name, swap_lr=swap_lr)
                    async with write_lock:
                        write_json(out_path, [x for x in results if x is not None])
                    return
                except Exception as err:
                    last_err = err
            raise RuntimeError(f"Pairwise judge failed for {key}: {last_err}") from last_err

    await asyncio.gather(*(worker(i, item) for i, item in enumerate(items)))
    return [x for x in results if x is not None]


def load_json(path: str | None) -> list[dict[str, Any]]:
    if not path:
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_existing_results(path: Path, key_fields: list[str]) -> dict[tuple[str, ...], dict[str, Any]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        rows = json.load(f)
    out: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(str(row.get(field) or "") for field in key_fields)
        out[key] = row
    return out


async def async_main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-input")
    parser.add_argument("--pairwise-input")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--model")
    parser.add_argument("--variant", choices=["a", "b", "c"], default="a")
    parser.add_argument("--temperature", type=float, default=-1.0)
    parser.add_argument("--max-output-tokens", type=int, default=500)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    case_items = load_json(args.case_input)
    pairwise_items = load_json(args.pairwise_input)
    client = LLMClient(model=args.model) if args.model else LLMClient()

    out_dir = Path(args.out_dir)
    temperature = None if args.temperature < 0 else args.temperature

    meta = {
        "run_name": args.run_name,
        "variant": args.variant,
        "model": args.model or client.model,
        "temperature": temperature,
        "max_output_tokens": args.max_output_tokens,
        "concurrency": args.concurrency,
        "seed": args.seed,
        "num_case_items": len(case_items),
        "num_pairwise_items": len(pairwise_items),
    }
    write_json(out_dir / f"{args.run_name}_meta.json", meta)

    if case_items:
        case_out = out_dir / f"{args.run_name}_case_results.json"
        case_results = await run_case_items(
            items=case_items,
            client=client,
            run_name=args.run_name,
            variant=args.variant,
            temperature=temperature,
            max_output_tokens=args.max_output_tokens,
            concurrency=args.concurrency,
            out_path=case_out,
        )
        write_json(case_out, case_results)

    if pairwise_items:
        pairwise_out = out_dir / f"{args.run_name}_pairwise_results.json"
        pairwise_results = await run_pairwise_items(
            items=pairwise_items,
            client=client,
            run_name=args.run_name,
            variant=args.variant,
            temperature=temperature,
            max_output_tokens=args.max_output_tokens,
            concurrency=args.concurrency,
            seed=args.seed,
            out_path=pairwise_out,
        )
        write_json(pairwise_out, pairwise_results)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
