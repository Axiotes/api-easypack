"""create log_operacao (historico das principais operacoes do sistema)

Revision ID: d4a7c1e9b6f2
Revises: b3f6e2a9c7d1
Create Date: 2026-11-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d4a7c1e9b6f2"
down_revision: Union[str, None] = "b3f6e2a9c7d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "log_operacao",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("dt_operacao", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("id_usuario", sa.BigInteger(), nullable=False),
        sa.Column("nm_usuario", sa.String(length=255), nullable=False),
        sa.Column("nm_entidade", sa.String(length=50), nullable=False),
        sa.Column("id_entidade", sa.BigInteger(), nullable=False),
        sa.Column("ds_acao", sa.String(length=50), nullable=False),
        sa.Column("ds_detalhe", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_log_operacao_entidade", "log_operacao", ["nm_entidade", "id_entidade"])


def downgrade() -> None:
    op.drop_index("ix_log_operacao_entidade", table_name="log_operacao")
    op.drop_table("log_operacao")
