from sqlalchemy.orm import Session
from app.models.event import Event
from app.models.event import TurnEvent

def log_event(db: Session, session_id: str, actor: str, content: str) -> int:
    e = Event(session_id=session_id, actor=actor, content=content)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e.id

def create_turn_event(
    db: Session,
    session_id: str,
    user_text: str,
    assistant_text: str,
    behavior: dict,
    scene: str | None = None,
    tone_eval: dict | None = None,
    # trace_id: str | None = None,
):
    e = TurnEvent(
        session_id=session_id,
        user_text=user_text,
        assistant_text=assistant_text,
        behavior=behavior,
        scene=scene,
        tone_eval=tone_eval,
        # trace_id=trace_id,
    )
    db.add(e)
    db.commit()
