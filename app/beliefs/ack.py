from __future__ import annotations
from app.models.belief import Belief

KEY_HUMAN_SUMMARY = {
    "no_unsolicited_emotion_questions": "不主动询问你的压力、情绪或心情",
}

def belief_to_ack_topic(b: Belief) -> str:
    if b.key and b.key in KEY_HUMAN_SUMMARY:
        return KEY_HUMAN_SUMMARY[b.key]
    return (b.value or "").strip()

def build_ack_block(topic: str, level: int) -> str:
    # level: 0 极短点头 / 1 短确认 / 2 完整温柔确认
    if level <= 0:
        style = (
            "用极短的一句点头式确认（不超过 12 个字），像人在认真听见对方："
            "例如“嗯，我记得的。”这类语气。不要展开。"
        )
    elif level == 1:
        style = (
            "用一到两句简短确认与轻承诺，不要长篇解释。"
            "语气温柔，但克制。"
        )
    else:
        style = (
            "用两到三句温柔、有感情的确认与承诺，但仍保持克制不过度。"
            "可以补一句“你想聊时再开口；不想聊我也尊重你”。"
        )

    return (
        "本轮需要做一件事：用户在重复强调一条重要边界/偏好。\n"
        f"要确认的点：{topic}\n"
        f"表达方式：{style}\n"
        "禁止项：不要说教、不要心理咨询师/教练口吻、不要夸张承诺（例如“永远不犯错”）。\n"
    )
