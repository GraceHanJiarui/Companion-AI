from __future__ import annotations

import httpx
from app.core.config import settings


class Embedder:
    async def embed(self, text: str) -> list[float]:
        url = f"{settings.llm_base_url.rstrip('/')}/embeddings"
        headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.embedding_model,
            "input": text,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)

        if resp.status_code >= 400:
            try:
                err = resp.json()
            except Exception:
                err = {"raw": resp.text}
            raise RuntimeError(f"Embedding error {resp.status_code}: {err}")

        data = resp.json()
        emb = data["data"][0]["embedding"]

        # --- hard cast + validation ---
        try:
            casted = [float(x) for x in emb]
        except Exception as e:
            # show a small sample to diagnose unexpected formats
            sample = emb[:5] if isinstance(emb, list) else emb
            raise RuntimeError(f"Embedding cast failed: {e}; sample={sample}; type0={type(emb[0]) if isinstance(emb, list) and emb else type(emb)}")

        # Validate element type
        if not casted or not isinstance(casted[0], float):
            raise RuntimeError(f"Embedding not float after cast; type0={type(casted[0]) if casted else None}")

        return casted
