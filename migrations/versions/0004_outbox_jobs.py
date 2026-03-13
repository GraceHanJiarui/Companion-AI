from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "outbox_jobs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_outbox_jobs_kind", "outbox_jobs", ["kind"])
    op.create_index("ix_outbox_jobs_status", "outbox_jobs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_outbox_jobs_status", table_name="outbox_jobs")
    op.drop_index("ix_outbox_jobs_kind", table_name="outbox_jobs")
    op.drop_table("outbox_jobs")
