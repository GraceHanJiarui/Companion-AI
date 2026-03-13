import json
import pandas as pd
from pathlib import Path

INPUT_XLSX = Path("actor_probe_output.xlsx")
OUTPUT_JSONL = Path("actor_lora_train.jsonl")

df = pd.read_excel(INPUT_XLSX)

with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        if str(row.get("use_for_training")).lower() != "yes":
            continue

        assistant_text = row.get("assistant_text_edited")
        if not isinstance(assistant_text, str) or not assistant_text.strip():
            continue

        sample = {
            "user_text": row["user_text"],
            "behavior": json.loads(row["behavior_json"]),
            "assistant_text": assistant_text.strip(),
        }

        f.write(json.dumps(sample, ensure_ascii=False) + "\n")

print(f"Wrote training data to {OUTPUT_JSONL.resolve()}")
