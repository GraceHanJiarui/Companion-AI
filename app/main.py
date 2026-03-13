from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.sessions import router as sessions_router
from app.api.health import router as health_router
from app.api.debug import router as debug_router  # 如果你加了 debug

from app.db.session import SessionLocal
from app.core.core_self import seed_core_self_if_empty

from app.outbox.worker import run_outbox_worker_forever  # NEW


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    db = SessionLocal()
    try:
        seed_core_self_if_empty(db)
    finally:
        db.close()

    # start outbox worker as a background task
    worker_task = asyncio.create_task(run_outbox_worker_forever())

    try:
        yield
    finally:
        worker_task.cancel()
        # optional: await cancellation
        try:
            await worker_task
        except Exception:
            pass


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(health_router)
app.include_router(debug_router)  # 可选
