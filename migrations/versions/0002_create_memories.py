from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure pgvector extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    op.create_table(
        "memories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column("salience", sa.Float(), server_default="1.0", nullable=False),
        sa.Column("from_event_id", sa.Integer(), nullable=True),
        sa.Column("to_event_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_memories_session_id", "memories", ["session_id"])
    op.create_index("ix_memories_created_at", "memories", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_memories_created_at", table_name="memories")
    op.drop_index("ix_memories_session_id", table_name="memories")
    op.drop_table("memories")
