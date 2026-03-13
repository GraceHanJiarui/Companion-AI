from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class Behavior(BaseModel):
    """
    行为态（快变量）：由关系态投影得到，用于指导 Actor 的表达倾向。
    """
    E: float = Field(ge=0.0, le=1.0, description="额外付出（多走一步的意愿）")
    Q_clarify: float = Field(ge=0.0, le=1.0, description="澄清/追问深度（偏任务澄清）")
    Directness: float = Field(ge=0.0, le=1.0, description="纠偏直率度（指出问题/风险的直接性）")
    T_w: float = Field(ge=0.0, le=1.0, description="温暖度（语气温度）")
    Q_aff: float = Field(ge=0.0, le=1.0, description="情绪/关系追问倾向（受边界约束）")
    Initiative: float = Field(ge=0.0, le=1.0, description="主动推进倾向（主动给下一步/替你推进）")
    Disclosure_Content: float = Field(ge=0.0, le=1.0, description="披露内容开放度（说什么）")
    Disclosure_Style: float = Field(ge=0.0, le=1.0, description="披露表达强度（怎么说）")


class MemoryPoint(BaseModel):
    memory_id: Optional[int] = None
    preview: str


class Plan(BaseModel):
    model_config = ConfigDict(extra="ignore")

    intent: Literal["chat", "ask_help", "task", "venting", "other"] = "chat"
    behavior: Behavior
    selected_memories: List[MemoryPoint] = Field(default_factory=list)

    notes: Optional[str] = None
