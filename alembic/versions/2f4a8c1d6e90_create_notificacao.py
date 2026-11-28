"""create notificacao table

Revision ID: 2f4a8c1d6e90
Revises: 7a1b708f2de3, d8b2f0c5e413
Create Date: 2026-11-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f4a8c1d6e90"
down_revision: Union[str, Sequence[str], None] = ("7a1b708f2de3", "d8b2f0c5e413")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notificacao",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("id_usuario", sa.BigInteger(), nullable=False),
        sa.Column("lido", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("notificacao")
