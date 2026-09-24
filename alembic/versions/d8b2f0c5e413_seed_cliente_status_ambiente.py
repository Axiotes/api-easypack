"""seed cliente status ambiente and estado

Revision ID: d8b2f0c5e413
Revises: c7a1e9b4d302
Create Date: 2026-09-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d8b2f0c5e413"
down_revision: Union[str, None] = "c7a1e9b4d302"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CLIENTES = [
    (1, "Cliente Aurora", "PRD", "SP"),
    (2, "Cliente Horizonte", "PRD", "RJ"),
    (3, "Cliente Pioneiro", "PRE-PROD", "MG"),
    (4, "Cliente Vértice", "PRE-PROD", "PR"),
]


def _atualizar_clientes(restaurar: bool = False) -> None:
    cliente = sa.table(
        "cliente",
        sa.column("id", sa.BigInteger),
        sa.column("nm_cliente", sa.String),
        sa.column("status_ambiente", sa.String),
        sa.column("estado", sa.String),
    )
    for cliente_id, nome, ambiente, estado in CLIENTES:
        op.execute(
            cliente.update()
            .where(cliente.c.id == cliente_id, cliente.c.nm_cliente == nome)
            .values(
                status_ambiente="PRE-PROD" if restaurar else ambiente,
                estado=None if restaurar else estado,
            )
        )


def upgrade() -> None:
    _atualizar_clientes()


def downgrade() -> None:
    _atualizar_clientes(restaurar=True)
