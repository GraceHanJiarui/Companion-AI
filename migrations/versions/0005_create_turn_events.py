from alembic import op
import sqlalchemy as sa

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "turn_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("user_text", sa.Text(), nullable=False),
        sa.Column("assistant_text", sa.Text(), nullable=False),
        sa.Column("behavior", sa.JSON(), nullable=False),
        sa.Column("scene", sa.String(), nullable=True),
        # sa.Column("trace_id", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

def downgrade() -> None:
    op.drop_table("turn_events")
