"""replace technical user roles with organizational job roles

Revision ID: 8c4e7a9d1b2f
Revises: 6dd0afe2e40f
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8c4e7a9d1b2f"
down_revision: Union[str, None] = "6dd0afe2e40f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OLD_CARGO = sa.Enum("ADMIN", "GERENTE", "ANALISTA", name="cargo_usuario")
NEW_CARGO = sa.Enum(
    "GERENTE_PROJETO",
    "COORDENADOR",
    "ESPECIALISTA",
    "SENIOR",
    "PLENO",
    "JUNIOR",
    "ESTAGIARIO",
    name="cargo_usuario",
)


def upgrade() -> None:
    # MySQL cannot change an ENUM when rows contain values absent from the new set.
    # A temporary VARCHAR allows the existing seed to be converted safely.
    op.alter_column(
        "usuario",
        "cargo",
        existing_type=OLD_CARGO,
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.execute(sa.text("UPDATE usuario SET cargo = 'COORDENADOR' WHERE cargo = 'ADMIN'"))
    op.execute(sa.text("UPDATE usuario SET cargo = 'GERENTE_PROJETO' WHERE cargo = 'GERENTE'"))
    op.execute(sa.text("UPDATE usuario SET cargo = 'PLENO' WHERE cargo = 'ANALISTA'"))
    op.alter_column(
        "usuario",
        "cargo",
        existing_type=sa.String(length=30),
        type_=NEW_CARGO,
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "usuario",
        "cargo",
        existing_type=NEW_CARGO,
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.execute(sa.text("UPDATE usuario SET cargo = 'ADMIN' WHERE cargo = 'COORDENADOR'"))
    op.execute(sa.text("UPDATE usuario SET cargo = 'GERENTE' WHERE cargo = 'GERENTE_PROJETO'"))
    op.execute(sa.text("UPDATE usuario SET cargo = 'ANALISTA' WHERE cargo NOT IN ('ADMIN', 'GERENTE')"))
    op.alter_column(
        "usuario",
        "cargo",
        existing_type=sa.String(length=30),
        type_=OLD_CARGO,
        existing_nullable=False,
    )
