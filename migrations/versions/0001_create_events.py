from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(length=64), nullable=False),
        sa.Column("actor", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_events_session_id", "events", ["session_id"])
    op.create_index("ix_events_actor", "events", ["actor"])
    op.create_index("ix_events_created_at", "events", ["created_at"])

def downgrade() -> None:
    op.drop_index("ix_events_created_at", table_name="events")
    op.drop_index("ix_events_actor", table_name="events")
    op.drop_index("ix_events_session_id", table_name="events")
    op.drop_table("events")
