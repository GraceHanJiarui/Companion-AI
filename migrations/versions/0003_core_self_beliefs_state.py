from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "core_self_versions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_core_self_versions_active", "core_self_versions", ["active"])

    op.create_table(
        "beliefs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(length=64), nullable=False, index=True),

        sa.Column("kind", sa.String(length=32), nullable=False),  # boundary/preference/style/relationship
        sa.Column("key", sa.String(length=128), nullable=True),   # normalized key (optional)
        sa.Column("value", sa.Text(), nullable=False),            # natural language belief
        sa.Column("strength", sa.Float(), nullable=False, server_default="0.7"),

        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),  # active/superseded/revoked
        sa.Column("evidence_event_id", sa.Integer(), nullable=True),
        sa.Column("evidence_memory_id", sa.Integer(), nullable=True),
        sa.Column("supersedes_id", sa.Integer(), nullable=True),

        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_beliefs_session_kind_status", "beliefs", ["session_id", "kind", "status"])

    op.create_table(
        "session_state",
        sa.Column("session_id", sa.String(length=64), primary_key=True),
        sa.Column("relation_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("policy_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("session_state")
    op.drop_index("ix_beliefs_session_kind_status", table_name="beliefs")
    op.drop_table("beliefs")
    op.drop_index("ix_core_self_versions_active", table_name="core_self_versions")
    op.drop_table("core_self_versions")
