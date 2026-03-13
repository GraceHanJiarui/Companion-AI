from fastapi import APIRouter, HTTPException
from app.core.llm_client import LLMClient

router = APIRouter()

@router.get("/health/llm")
async def health_llm():
    llm = LLMClient()
    try:
        text = await llm.generate(system="Say OK.", user="ping")
        return {"ok": True, "sample": text[:80]}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
