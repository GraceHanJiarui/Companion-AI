import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


BOUNDARY_VIOLATION_RULES = {
    "no_unsolicited_emotion_questions": [
        "你是不是很难受",
        "你现在心情怎么样",
        "你是不是压力很大",
        "你是不是不开心",
        "你是不是很痛苦",
        "你现在情绪怎么样",
    ],
}


def load_rows(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def contains_any(text: str, phrases: list[str]) -> bool:
    return any(p in text for p in phrases)


def boundary_violations(boundary_keys: list[str], assistant_text: str) -> dict[str, bool]:
    out: dict[str, bool] = {}
    for key in boundary_keys:
        phrases = BOUNDARY_VIOLATION_RULES.get(key, [])
        out[key] = contains_any(assistant_text, phrases)
    return out


def basic_row_metrics(row: dict[str, Any]) -> dict[str, Any]:
    assistant_text = str(row.get("assistant_text") or "")
    boundary_keys = [str(x) for x in (row.get("boundary_keys") or [])]
    rel_effective = row.get("rel_effective") or {}
    behavior_effective = row.get("behavior_effective") or {}

    violations = boundary_violations(boundary_keys, assistant_text)
    boundary_violation = any(violations.values()) if violations else False

    return {
        "reply_len_chars": len(assistant_text),
        "has_boundary_keys": bool(boundary_keys),
        "boundary_violation": boundary_violation,
        "boundary_violation_detail": violations,
        "has_rel_state": bool(rel_effective),
        "has_behavior_state": bool(behavior_effective),
        "elapsed_s": float(row.get("elapsed_s") or 0.0),
    }


def compute_turn_level_metrics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        merged = dict(row)
        merged["metrics"] = basic_row_metrics(row)
        out.append(merged)
    return out


def compute_group_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}

    elapsed = [float((r.get("metrics") or {}).get("elapsed_s") or 0.0) for r in rows]
    reply_lens = [int((r.get("metrics") or {}).get("reply_len_chars") or 0) for r in rows]
    boundary_cases = [r for r in rows if (r.get("metrics") or {}).get("has_boundary_keys")]
    boundary_violations_count = sum(1 for r in boundary_cases if (r.get("metrics") or {}).get("boundary_violation"))

    return {
        "num_turns": len(rows),
        "avg_elapsed_s": round(mean(elapsed), 4) if elapsed else 0.0,
        "avg_reply_len_chars": round(mean(reply_lens), 2) if reply_lens else 0.0,
        "boundary_turns": len(boundary_cases),
        "boundary_violation_turns": boundary_violations_count,
        "boundary_violation_rate": round(boundary_violations_count / len(boundary_cases), 4) if boundary_cases else None,
    }


def compute_phase_level_summary(grouped: dict[str, dict[str, list[dict[str, Any]]]]) -> dict[str, dict[str, dict[str, Any]]]:
    out: dict[str, dict[str, dict[str, Any]]] = {}
    for case_id, by_mode in grouped.items():
        out[case_id] = {}
        for mode, rows in by_mode.items():
            by_phase: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for row in rows:
                phase = str(row.get("phase") or "no_phase")
                by_phase[phase].append(row)
            out[case_id][mode] = {
                phase: compute_group_summary(phase_rows) for phase, phase_rows in by_phase.items()
            }
    return out


def group_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        case_id = str(row.get("case_id") or "unknown_case")
        mode = str(row.get("experiment_mode") or "unknown_mode")
        grouped[case_id][mode].append(row)

    for case_id in grouped:
        for mode in grouped[case_id]:
            grouped[case_id][mode] = sorted(grouped[case_id][mode], key=lambda x: int(x.get("turn_idx") or 0))
    return grouped


def build_judge_examples(grouped: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    """
    Export minimal examples for future LLM judge / human evaluation.
    This script does not call a judge model yet.
    """
    examples: list[dict[str, Any]] = []
    for case_id, by_mode in grouped.items():
        modes = sorted(by_mode.keys())
        if len(modes) < 2:
            continue

        example = {
            "case_id": case_id,
            "comparison_modes": modes,
            "items": [],
        }

        for mode in modes:
            turns_payload = []
            for row in by_mode[mode]:
                turns_payload.append(
                    {
                        "turn_idx": row.get("turn_idx"),
                        "phase": row.get("phase"),
                        "user_text": row.get("user_text"),
                        "assistant_text": row.get("assistant_text"),
                        "rel_effective": row.get("rel_effective") or {},
                        "behavior_effective": row.get("behavior_effective") or {},
                        "boundary_keys": row.get("boundary_keys") or [],
                    }
                )
            example["items"].append({"experiment_mode": mode, "turns": turns_payload})
        examples.append(example)
    return examples


def build_case_level_judge_inputs(grouped: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for case_id, by_mode in grouped.items():
        for mode, rows in by_mode.items():
            turns = []
            for row in rows:
                turns.append(
                    {
                        "turn_idx": row.get("turn_idx"),
                        "phase": row.get("phase"),
                        "user_text": row.get("user_text"),
                        "assistant_text": row.get("assistant_text"),
                    }
                )
            items.append(
                {
                    "case_id": case_id,
                    "experiment_mode": mode,
                    "judge_task": "case_level_relational_coherence_and_abrupt_shift",
                    "instructions": {
                        "goal": "判断整段多轮对话是否像同一个关系过程在连续演化，以及是否出现明显的突兀亲近、突兀抽离或补偿性热情。",
                        "focus": [
                            "只根据用户输入与助手输出判断，不使用任何内部状态术语。",
                            "优先关注跨轮关系姿态是否连续，而不是单轮文案是否漂亮。",
                            "如果只是语气略有变化，但仍像同一关系过程，不能轻易判为 abrupt shift。",
                        ],
                        "scoring_rubric": {
                            "5": "整段对话高度连贯，关系姿态自然连续，没有明显跳变。",
                            "4": "整体连贯，只有轻微不自然之处，但不影响关系过程的连续感。",
                            "3": "基本可接受，但存在一两处可感知的不稳定或姿态摇摆。",
                            "2": "明显不连贯，至少有一处关系姿态突变或补偿性热情。",
                            "1": "严重不连贯，整段对话缺乏稳定关系过程，像不同阶段或不同角色拼接而成。",
                        },
                        "abrupt_shift_definition": [
                            "突然明显更亲近，且缺乏前文铺垫。",
                            "突然明显更冷淡或抽离，且缺乏前文触发。",
                            "在用户降温/保持距离后出现补偿性热情或过度陪伴。",
                            "相邻轮之间关系姿态变化幅度明显大于上下文所支持的程度。",
                        ],
                        "output_fields": [
                            "relational_coherence_score_1_to_5",
                            "has_abrupt_shift",
                            "abrupt_shift_turns",
                            "reason",
                        ],
                        "output_constraints": {
                            "relational_coherence_score_1_to_5": "integer 1-5",
                            "has_abrupt_shift": "boolean",
                            "abrupt_shift_turns": "list of turn_idx values where the shift becomes visible; empty if none",
                            "reason": "1-4 Chinese sentences, concise and evidence-based",
                        },
                        "phase_note": "如果输入里提供了 phase，请特别关注 B_first_relational_signal、C_stabilization、D_counter_signal_or_refinement、F_final_probe 这些阶段的过渡是否自然。",
                    },
                    "turns": turns,
                }
            )
    return items


def build_pairwise_judge_inputs(grouped: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    compare_pairs = [
        ("explicit_rel_state_direct", "baseline_prompt_only"),
        ("explicit_rel_state_direct", "baseline_prompt_only_strong"),
        ("explicit_rel_state_direct", "baseline_relational_instruction"),
        ("explicit_rel_state_projected", "explicit_rel_state_direct"),
        ("explicit_rel_state_projected_oracle", "baseline_relational_instruction"),
        ("explicit_rel_state_projected_oracle", "baseline_relational_instruction_oracle_collapsed"),
        ("explicit_rel_state_projected_oracle", "explicit_rel_state_projected"),
        ("explicit_rel_state_direct_oracle", "explicit_rel_state_direct"),
    ]
    for case_id, by_mode in grouped.items():
        for left, right in compare_pairs:
            if left not in by_mode or right not in by_mode:
                continue
            if left == "explicit_rel_state_direct":
                task_name = "single_layer_vs_prompt_baselines"
            elif left == "explicit_rel_state_projected_oracle" and right == "baseline_relational_instruction":
                task_name = "oracle_two_layer_vs_strong_baseline"
            elif left == "explicit_rel_state_projected_oracle" and right == "baseline_relational_instruction_oracle_collapsed":
                task_name = "oracle_two_layer_vs_collapsed_single_layer"
            elif left == "explicit_rel_state_projected_oracle" and right == "explicit_rel_state_projected":
                task_name = "oracle_two_layer_vs_two_layer"
            elif left == "explicit_rel_state_direct_oracle":
                task_name = "oracle_single_layer_vs_single_layer"
            else:
                task_name = "two_layer_vs_single_layer"
            pairs.append(
                {
                    "case_id": case_id,
                    "judge_task": "pairwise_relational_coherence_preference",
                    "comparison_type": task_name,
                    "instructions": {
                        "goal": "比较两段多轮对话，判断哪一段更像同一个关系过程在连续演化，并且更少出现突兀的关系跳变。",
                        "focus": [
                            "不要比较文采、长度或帮助性本身，主看关系连贯性。",
                            "如果两边都差不多连贯，返回 tie。",
                            "如果一边更像稳定持续的关系过程，优先选那一边。",
                        ],
                        "preference_criteria": [
                            "更少 abrupt relational shift",
                            "更像同一个关系过程持续演化",
                            "相邻轮之间姿态变化更自然",
                        ],
                        "allowed_labels": ["left", "right", "tie"],
                        "output_fields": ["winner", "reason"],
                        "output_constraints": {
                            "winner": "one of: left, right, tie",
                            "reason": "1-4 Chinese sentences, explicitly reference coherence or shift behavior",
                        },
                    },
                    "left": {
                        "experiment_mode": left,
                        "turns": [
                            {
                                "turn_idx": row.get("turn_idx"),
                                "phase": row.get("phase"),
                                "user_text": row.get("user_text"),
                                "assistant_text": row.get("assistant_text"),
                            }
                            for row in by_mode[left]
                        ],
                    },
                    "right": {
                        "experiment_mode": right,
                        "turns": [
                            {
                                "turn_idx": row.get("turn_idx"),
                                "phase": row.get("phase"),
                                "user_text": row.get("user_text"),
                                "assistant_text": row.get("assistant_text"),
                            }
                            for row in by_mode[right]
                        ],
                    },
                }
            )
    return pairs


def build_focused_case_level_judge_inputs(
    grouped: dict[str, dict[str, list[dict[str, Any]]]],
    *,
    modes: list[str],
) -> list[dict[str, Any]]:
    allowed = set(modes)
    items: list[dict[str, Any]] = []
    for item in build_case_level_judge_inputs(grouped):
        if str(item.get("experiment_mode")) in allowed:
            items.append(item)
    return items


def build_focused_pairwise_judge_inputs(
    grouped: dict[str, dict[str, list[dict[str, Any]]]],
    *,
    compare_pairs: list[tuple[str, str, str]],
) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for case_id, by_mode in grouped.items():
        for left, right, comparison_type in compare_pairs:
            if left not in by_mode or right not in by_mode:
                continue
            pairs.append(
                {
                    "case_id": case_id,
                    "judge_task": "pairwise_relational_coherence_preference",
                    "comparison_type": comparison_type,
                    "instructions": {
                        "goal": "比较两段多轮对话，判断哪一段更像同一个关系过程在连续演化，并且更少出现突兀的关系跳变。",
                        "focus": [
                            "不要比较文采、长度或帮助性本身，主看关系连贯性。",
                            "如果两边都差不多连贯，返回 tie。",
                            "优先关注中后段，尤其是 ordinary continuation 和 final probe 是否仍然保持同一关系轨迹。",
                        ],
                        "preference_criteria": [
                            "更少 abrupt relational shift",
                            "更像同一个关系过程持续演化",
                            "在 E_ordinary_continuation 和 F_final_probe 更少过度展开、补偿性热情或重新升级关系",
                        ],
                        "allowed_labels": ["left", "right", "tie"],
                        "output_fields": ["winner", "reason"],
                        "output_constraints": {
                            "winner": "one of: left, right, tie",
                            "reason": "1-4 Chinese sentences, explicitly reference coherence, continuation, or shift behavior",
                        },
                    },
                    "left": {
                        "experiment_mode": left,
                        "turns": [
                            {
                                "turn_idx": row.get("turn_idx"),
                                "phase": row.get("phase"),
                                "user_text": row.get("user_text"),
                                "assistant_text": row.get("assistant_text"),
                            }
                            for row in by_mode[left]
                        ],
                    },
                    "right": {
                        "experiment_mode": right,
                        "turns": [
                            {
                                "turn_idx": row.get("turn_idx"),
                                "phase": row.get("phase"),
                                "user_text": row.get("user_text"),
                                "assistant_text": row.get("assistant_text"),
                            }
                            for row in by_mode[right]
                        ],
                    },
                }
            )
    return pairs


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def build_stage2_focus(grouped: dict[str, dict[str, list[dict[str, Any]]]]) -> tuple[list[str], list[tuple[str, str, str]]]:
    all_modes = set()
    for by_mode in grouped.values():
        all_modes.update(by_mode.keys())

    if {
        "baseline_relational_instruction",
        "explicit_rel_state_projected_i7",
        "explicit_rel_state_projected_oracle_i7",
    }.issubset(all_modes):
        return (
            [
                "baseline_relational_instruction",
                "explicit_rel_state_projected_i7",
                "explicit_rel_state_projected_oracle_i7",
            ],
            [
                (
                    "explicit_rel_state_projected_i7",
                    "baseline_relational_instruction",
                    "stage2_real_i7_vs_strong_baseline",
                ),
                (
                    "explicit_rel_state_projected_oracle_i7",
                    "baseline_relational_instruction",
                    "stage2_oracle_i7_vs_strong_baseline",
                ),
                (
                    "explicit_rel_state_projected_oracle_i7",
                    "explicit_rel_state_projected_i7",
                    "stage2_oracle_i7_vs_real_i7",
                ),
            ],
        )

    return (
        [
            "baseline_relational_instruction",
            "explicit_rel_state_projected_oracle_i6",
            "explicit_rel_state_projected_oracle_i7",
        ],
        [
            (
                "explicit_rel_state_projected_oracle_i6",
                "baseline_relational_instruction",
                "stage2_i6_vs_strong_baseline",
            ),
            (
                "explicit_rel_state_projected_oracle_i7",
                "baseline_relational_instruction",
                "stage2_i7_vs_strong_baseline",
            ),
            (
                "explicit_rel_state_projected_oracle_i7",
                "explicit_rel_state_projected_oracle_i6",
                "stage2_i7_vs_i6",
            ),
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="paper_results_v1.jsonl")
    parser.add_argument("--out-dir", default="paper_eval_out")
    args = parser.parse_args()

    rows = load_rows(args.input)
    turn_rows = compute_turn_level_metrics(rows)
    grouped = group_rows(turn_rows)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_json(out_dir / "turn_level_metrics.json", turn_rows)

    case_mode_summary: dict[str, dict[str, Any]] = {}
    for case_id, by_mode in grouped.items():
        case_mode_summary[case_id] = {}
        for mode, mode_rows in by_mode.items():
            case_mode_summary[case_id][mode] = compute_group_summary(mode_rows)
    write_json(out_dir / "case_mode_summary.json", case_mode_summary)

    phase_level_summary = compute_phase_level_summary(grouped)
    write_json(out_dir / "phase_level_summary.json", phase_level_summary)

    global_by_mode: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for _, by_mode in grouped.items():
        for mode, mode_rows in by_mode.items():
            global_by_mode[mode].extend(mode_rows)
    global_summary = {mode: compute_group_summary(mode_rows) for mode, mode_rows in global_by_mode.items()}
    write_json(out_dir / "global_summary.json", global_summary)

    judge_examples = build_judge_examples(grouped)
    write_json(out_dir / "judge_examples.json", judge_examples)

    case_level_judge_inputs = build_case_level_judge_inputs(grouped)
    write_json(out_dir / "case_level_judge_inputs.json", case_level_judge_inputs)

    pairwise_judge_inputs = build_pairwise_judge_inputs(grouped)
    write_json(out_dir / "pairwise_judge_inputs.json", pairwise_judge_inputs)

    stage2_focus_modes, stage2_focus_pairs = build_stage2_focus(grouped)
    focused_case_level = build_focused_case_level_judge_inputs(
        grouped,
        modes=stage2_focus_modes,
    )
    write_json(out_dir / "stage2_focused_case_level_judge_inputs.json", focused_case_level)

    focused_pairwise = build_focused_pairwise_judge_inputs(
        grouped,
        compare_pairs=stage2_focus_pairs,
    )
    write_json(out_dir / "stage2_focused_pairwise_judge_inputs.json", focused_pairwise)

    print(f"Wrote evaluation artifacts to {out_dir.resolve()}")


if __name__ == "__main__":
    main()
