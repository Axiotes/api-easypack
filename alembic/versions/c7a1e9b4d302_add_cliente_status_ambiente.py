"""add cliente status ambiente and estado

Revision ID: c7a1e9b4d302
Revises: 69155d164402
Create Date: 2026-09-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c7a1e9b4d302"
down_revision: Union[str, None] = "69155d164402"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    colunas = {coluna["name"] for coluna in sa.inspect(op.get_bind()).get_columns("cliente")}

    if "estado" not in colunas:
        op.add_column("cliente", sa.Column("estado", sa.String(length=2), nullable=True))
    if "status_ambiente" not in colunas:
        op.add_column(
            "cliente",
            sa.Column(
                "status_ambiente",
                sa.Enum("PRE-PROD", "PRD", name="status_ambiente_cliente", create_constraint=True),
                nullable=False,
                server_default="PRE-PROD",
            ),
        )


def downgrade() -> None:
    colunas = {coluna["name"] for coluna in sa.inspect(op.get_bind()).get_columns("cliente")}

    if "status_ambiente" in colunas:
        op.drop_column("cliente", "status_ambiente")
    if "estado" in colunas:
        op.drop_column("cliente", "estado")
