from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.event import Event

router = APIRouter()

@router.get("/sessions/{session_id}/events")
def get_events(session_id: str, db: Session = Depends(get_db)):
    stmt = (
        select(Event)
        .where(Event.session_id == session_id)
        .order_by(Event.created_at.asc(), Event.id.asc())
    )
    rows = db.execute(stmt).scalars().all()

    data = [
        {
            "id": r.id,
            "actor": r.actor,
            "content": r.content,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]

    return JSONResponse(content=data, media_type="application/json; charset=utf-8")
