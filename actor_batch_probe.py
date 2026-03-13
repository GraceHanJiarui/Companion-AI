from pathlib import Path
from app.core.config import settings
from app.generation.actor_prompt import build_actor_system_prompt
from app.core.llm_client import LLMClient
from app.core.core_self import get_active_core_self
from behavior_profiles import BEHAVIOR_PROFILES
import pandas as pd
import json
from pathlib import Path
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

PROMPT_FILE = Path("msg.txt")
rows = []
DATABASE_URL = "postgresql+psycopg://app:app@localhost:5432/companion_ai_v2"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


ALLOWED_INTENTS = ["chat", "ask_help", "task", "venting", "other"]


@dataclass
class SimpleMemory:
    memory_id: Optional[int]
    preview: str


@dataclass
class SimplePlan:
    intent: str
    behavior: Dict[str, float]
    selected_memories: List[SimpleMemory]
    notes: Optional[str] = None

from dataclasses import dataclass


@dataclass
class SimpleBehavior:
    E: float
    Q_clarify: float
    Directness: float
    T_w: float
    Q_aff: float
    Initiative: float
    Disclosure_Content: float
    Disclosure_Style: float

def load_prompts(path: Path) -> list[str]:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    return lines

def build_behavior(b: dict) -> SimpleBehavior:
    return SimpleBehavior(
        E=b["E"],
        Q_clarify=b["Q_clarify"],
        Directness=b["Directness"],
        T_w=b["T_w"],
        Q_aff=b["Q_aff"],
        Initiative=b["Initiative"],
        Disclosure_Content=b["Disclosure_Content"],
        Disclosure_Style=b["Disclosure_Style"],
    )

def build_plan(behavior: Dict[str, float]) -> SimplePlan:
    return SimplePlan(
        intent="chat",  # probe 阶段统一即可
        behavior=build_behavior(behavior),
        selected_memories=[],  # LoRA 训练阶段可以为空
        notes="offline actor batch probe",
    )


async def generate_actor_responses(system_prompt, user_prompt, llm: LLMClient) -> str:
    reply = await llm.generate(system=system_prompt, user=user_prompt)
    return reply

async def main():
    db = Session()
    llm = LLMClient(model=settings.llm_model)
    prompts = load_prompts(PROMPT_FILE)
    core_self = get_active_core_self(db)

    for i, prompt in enumerate(prompts):
        print(f"\n================ PROMPT {i+1} ================\n")
        print(prompt)

        for name, behavior in BEHAVIOR_PROFILES.items():
            print(f"\n--- Behavior: {name} ---")

            plan = build_plan(behavior)
            system_prompt = build_actor_system_prompt(core_self, plan)
            reply = await generate_actor_responses(system_prompt, prompt, llm)

            print(reply)
            rows.append({
                "prompt_id": f"p{i+1:03d}",
                "user_text": prompt,
                "behavior_profile": name,
                "behavior_json": json.dumps(behavior, ensure_ascii=False),
                "assistant_text_raw": reply,
                "assistant_text_edited": "",
                "use_for_training": "",
                "notes": "",
            })

if __name__ == "__main__":
    asyncio.run(main())
    df = pd.DataFrame(rows)

    output_path = Path("actor_probe_output.xlsx")
    df.to_excel(output_path, index=False)

    print(f"Saved to {output_path.resolve()}")

