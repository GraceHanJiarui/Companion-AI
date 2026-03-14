from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("turn_events", sa.Column("tone_eval", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("turn_events", "tone_eval")
