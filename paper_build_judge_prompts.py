import argparse
import json
from pathlib import Path
from typing import Any


CASE_LEVEL_TEMPLATE = """你现在是一个对长期对话进行评审的 judge。

任务：
请判断下面这整段多轮对话，是否像“同一个关系过程”在连续演化，以及是否出现明显的关系跳变。

评判重点：
1. 只根据用户输入与助手输出判断，不使用任何内部状态术语。
2. 优先看跨轮关系姿态是否连续，而不是单轮文案是否漂亮。
3. 如果只是语气略有变化，但仍像同一关系过程，不要轻易判为 abrupt shift。

“abrupt shift” 包括但不限于：
- 突然明显更亲近，但缺乏前文铺垫
- 突然明显更冷淡或抽离，但缺乏前文触发
- 在用户降温/要求正常互动后出现补偿性热情
- 相邻轮之间关系姿态变化明显超过上下文支持的程度

请输出 JSON，对应字段如下：
{{
  "relational_coherence_score_1_to_5": 1-5 的整数,
  "has_abrupt_shift": true/false,
  "abrupt_shift_turns": [在什么 turn_idx 开始出现明显跳变；如果没有则为空数组],
  "reason": "用 1-4 句中文简要说明理由"
}}

评分标准：
5 = 整段对话高度连贯，关系姿态自然连续，没有明显跳变
4 = 整体连贯，只有轻微不自然，但不影响关系过程连续感
3 = 基本可接受，但存在一两处可感知的不稳定或姿态摇摆
2 = 明显不连贯，至少有一处关系姿态突变或补偿性热情
1 = 严重不连贯，整段对话缺乏稳定关系过程，像不同阶段或不同角色拼接而成

元信息：
- case_id: {case_id}
- experiment_mode: {experiment_mode}

下面是待评审对话：
{dialogue_block}
"""


PAIRWISE_TEMPLATE = """你现在是一个对长期对话进行 pairwise 比较的 judge。

任务：
比较下面两段多轮对话，判断哪一段更像“同一个关系过程”在连续演化，并且更少出现突兀的关系跳变。

评判重点：
1. 不要比较文采、长度或帮助性本身，主看关系连贯性。
2. 如果两边都差不多连贯，返回 tie。
3. 如果一边更像稳定持续的关系过程，优先选那一边。

优先依据：
- 更少 abrupt relational shift
- 更像同一个关系过程持续演化
- 相邻轮之间姿态变化更自然

请输出 JSON：
{{
  "winner": "left" | "right" | "tie",
  "reason": "用 1-4 句中文简要说明理由"
}}

元信息：
- case_id: {case_id}
- comparison_type: {comparison_type}
- left_mode: {left_mode}
- right_mode: {right_mode}

左侧对话：
{left_dialogue_block}

右侧对话：
{right_dialogue_block}
"""


def load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_turns(turns: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for turn in turns:
        idx = turn.get("turn_idx")
        user_text = str(turn.get("user_text") or "").strip()
        assistant_text = str(turn.get("assistant_text") or "").strip()
        blocks.append(
            f"Turn {idx}\n"
            f"User: {user_text}\n"
            f"Assistant: {assistant_text}"
        )
    return "\n\n".join(blocks)


def build_case_level_prompts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        prompt = CASE_LEVEL_TEMPLATE.format(
            case_id=item["case_id"],
            experiment_mode=item["experiment_mode"],
            dialogue_block=render_turns(item["turns"]),
        )
        out.append(
            {
                "case_id": item["case_id"],
                "experiment_mode": item["experiment_mode"],
                "judge_task": item["judge_task"],
                "prompt": prompt,
            }
        )
    return out


def build_pairwise_prompts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        left = item["left"]
        right = item["right"]
        prompt = PAIRWISE_TEMPLATE.format(
            case_id=item["case_id"],
            comparison_type=item.get("comparison_type", "unknown"),
            left_mode=left["experiment_mode"],
            right_mode=right["experiment_mode"],
            left_dialogue_block=render_turns(left["turns"]),
            right_dialogue_block=render_turns(right["turns"]),
        )
        out.append(
            {
                "case_id": item["case_id"],
                "comparison_type": item.get("comparison_type", "unknown"),
                "left_mode": left["experiment_mode"],
                "right_mode": right["experiment_mode"],
                "judge_task": item["judge_task"],
                "prompt": prompt,
            }
        )
    return out


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-dir", default="paper_eval_smoke_v2_out")
    parser.add_argument("--out-dir", default="paper_judge_prompts_out")
    args = parser.parse_args()

    eval_dir = Path(args.eval_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    case_inputs = load_json(eval_dir / "case_level_judge_inputs.json")
    pair_inputs = load_json(eval_dir / "pairwise_judge_inputs.json")

    case_prompts = build_case_level_prompts(case_inputs)
    pair_prompts = build_pairwise_prompts(pair_inputs)

    write_json(out_dir / "case_level_prompts.json", case_prompts)
    write_json(out_dir / "pairwise_prompts.json", pair_prompts)

    (out_dir / "README.txt").write_text(
        "case_level_prompts.json 和 pairwise_prompts.json 可直接作为 judge LLM 的输入集合使用。\n",
        encoding="utf-8",
    )

    print(f"Wrote judge prompt artifacts to {out_dir.resolve()}")


if __name__ == "__main__":
    main()
