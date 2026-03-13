from __future__ import annotations
import re
from dataclasses import dataclass


@dataclass
class BeliefCandidate:
    kind: str
    key: str | None
    value: str
    strength: float = 0.7


_BOUNDARY_PAT = re.compile(
    r"(我不喜欢|我讨厌|别这样|可以不要|你别|"
    r"不要(再)?(这样|问|说|提)|"
    r"别(再)?(问|说|提))"
)

# 用于识别“情绪/压力”类词
_EMOTION_TOPIC_PAT = re.compile(r"(压力|情绪|心情|难受|焦虑|抑郁|崩溃|烦|累)")


def extract_beliefs_from_user_text(user_text: str) -> list[BeliefCandidate]:
    t = (user_text or "").strip()
    if not t:
        return []

    cands: list[BeliefCandidate] = []

    # 1) 边界类：如果命中边界词，再判断是否是“别问情绪/压力”
    if _BOUNDARY_PAT.search(t):
        key = None

        # 典型：别(再)?问 + 情绪/压力话题
        # 这里不做复杂 NLP，只做稳定可控的 MVP
        if ("问" in t or "提" in t) and _EMOTION_TOPIC_PAT.search(t):
            key = "no_unsolicited_emotion_questions"

        cands.append(
            BeliefCandidate(
                kind="boundary",
                key=key,
                value=f"用户表达了边界/否定：{t}",
                strength=0.9,
            )
        )

    # 2) 偏好类（保留你原逻辑）
    if "我喜欢" in t and len(t) >= 6:
        cands.append(BeliefCandidate(kind="preference", key=None, value=f"用户偏好：{t}", strength=0.7))
    if "我不喜欢" in t and len(t) >= 6:
        cands.append(BeliefCandidate(kind="preference", key=None, value=f"用户不偏好：{t}", strength=0.8))

    return cands
