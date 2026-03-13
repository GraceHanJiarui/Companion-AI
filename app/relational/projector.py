from __future__ import annotations

from dataclasses import dataclass
from typing import List


def clamp01(x: float) -> float:
    try:
        x = float(x)
    except Exception:
        return 0.0
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def clamp(x: float, lo: float, hi: float) -> float:
    try:
        x = float(x)
    except Exception:
        return lo
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@dataclass(frozen=True)
class RelState:
    bond: float
    care: float
    trust: float
    stability: float


@dataclass(frozen=True)
class Behavior:
    # 因变量（快变量）
    E: float
    Q_clarify: float
    Directness: float
    T_w: float
    Q_aff: float
    Initiative: float
    Disclosure_Content: float
    Disclosure_Style: float


def project_behavior(
    rel: RelState,
    *,
    active_boundary_keys: List[str] | None = None,
    scene: List[str] | None = None,
) -> Behavior:
    """
    将关系态（Bond/Care/Trust/Stability）确定性投影为行为态（8 维因变量）。

    注意：
    - 这里的输出被理解为“关系域的外显方式”，不是任务域的显式姿态控制。
    - scene 由 LLM 判断（语义），这里只做小幅偏置，保证稳定可控。
    """
    keys = set(active_boundary_keys or [])
    tags = set(scene or [])

    bond = clamp01(rel.bond)
    care = clamp01(rel.care)
    trust = clamp01(rel.trust)
    stability = clamp01(rel.stability)

    invest = clamp01(0.35 * bond + 0.35 * care + 0.30 * trust)

    # 额外付出
    E = clamp01(0.15 + 0.85 * invest)

    # 澄清追问深度（更敢问更深：由 trust 主导）
    Q_clarify = clamp01(0.10 + 0.70 * trust + 0.20 * invest)

    # 纠偏直率（由 trust 主导）
    Directness = clamp01(0.10 + 0.85 * trust)

    # 温暖度（由 care/bond 主导）
    T_w = clamp01(0.10 + 0.55 * care + 0.25 * bond)

    # 关怀追问倾向（由 care/bond 主导，受边界限制）
    Q_aff = clamp01(0.05 + 0.65 * care + 0.20 * bond)

    # 主动推进（投入 + 许可）
    Initiative = clamp01(0.10 + 0.60 * invest + 0.20 * trust)

    # 披露内容开放度：bond/care 越高越容易披露；stability 越低越容易出现“失落/想念但自担”的内容
    dc = 0.10 + 0.45 * ((bond + care) / 2.0) + 0.35 * (1.0 - stability)

    # scene 偏置（小步）
    if "leave_or_pause" in tags:
        dc += 0.10
    if "relationship_addressing" in tags:
        dc += 0.05
    if "user_vulnerable" in tags:
        dc += 0.05
    if "tech_help" in tags or "task_focus" in tags:
        dc -= 0.08

    Disclosure_Content = clamp01(dc)

    # 披露风格强度：由 bond/care/invest 推动，但不应超过内容开放度的软上限
    ds = 0.10 + 0.60 * ((bond + care) / 2.0) + 0.10 * invest
    Disclosure_Style = clamp01(min(ds, 0.20 + 0.80 * Disclosure_Content))

    return Behavior(
        E=E,
        Q_clarify=Q_clarify,
        Directness=Directness,
        T_w=T_w,
        Q_aff=Q_aff,
        Initiative=Initiative,
        Disclosure_Content=Disclosure_Content,
        Disclosure_Style=Disclosure_Style,
    )
