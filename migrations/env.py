from __future__ import annotations

import os
import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from dotenv import load_dotenv
load_dotenv()

# ---- add this block ----
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
# ------------------------

from app.db.base import Base
from app.models import event  # noqa: F401
from app.models import outbox_job  # noqa: F401  # NEW: ensure metadata includes outbox_jobs

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url() -> str:
    return os.environ["DATABASE_URL"]

def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
