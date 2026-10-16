"""add catalogo de tipo de pacote, produto portaria e gp sem produto obrigatorio

Revision ID: 7a1b708f2de3
Revises: 69155d164402
Create Date: 2026-10-16

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7a1b708f2de3"
down_revision: Union[str, None] = "69155d164402"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FORMS_REPORTS = "FORMS_REPORTS"
FRONT_BACK = "FRONT_BACK"


def upgrade() -> None:
    op.add_column("produto", sa.Column("nm_grupo_tipo_pacote", sa.String(length=20), nullable=True))
    op.execute(sa.text(f"UPDATE produto SET nm_grupo_tipo_pacote = '{FORMS_REPORTS}' WHERE id = 1"))
    op.execute(sa.text(f"UPDATE produto SET nm_grupo_tipo_pacote = '{FRONT_BACK}' WHERE id = 2"))
    op.execute(sa.text(f"UPDATE produto SET nm_grupo_tipo_pacote = '{FORMS_REPORTS}' WHERE id = 3"))
    op.execute(sa.text(f"UPDATE produto SET nm_grupo_tipo_pacote = '{FRONT_BACK}' WHERE id = 4"))
    op.alter_column("produto", "nm_grupo_tipo_pacote", existing_type=sa.String(length=20), nullable=False)

    produto = sa.table(
        "produto",
        sa.column("id", sa.BigInteger),
        sa.column("nm_produto", sa.String),
        sa.column("nm_grupo_tipo_pacote", sa.String),
    )
    op.bulk_insert(produto, [{"id": 5, "nm_produto": "Portaria", "nm_grupo_tipo_pacote": FRONT_BACK}])

    op.create_table(
        "tipo_pacote",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("nm_tipo", sa.String(length=50), nullable=False),
        sa.Column("nm_grupo", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    tipo_pacote = sa.table(
        "tipo_pacote",
        sa.column("id", sa.BigInteger),
        sa.column("nm_tipo", sa.String),
        sa.column("nm_grupo", sa.String),
    )
    op.bulk_insert(
        tipo_pacote,
        [
            {"id": 1, "nm_tipo": "Forms", "nm_grupo": FORMS_REPORTS},
            {"id": 2, "nm_tipo": "Reports", "nm_grupo": FORMS_REPORTS},
            {"id": 3, "nm_tipo": "Front", "nm_grupo": FRONT_BACK},
            {"id": 4, "nm_tipo": "Back", "nm_grupo": FRONT_BACK},
        ],
    )
    # Normaliza pacotes de demonstração pré-existentes (tp_pacote era um número livre) para o
    # tipo de pacote compatível com o grupo do produto da correção, antes de criar a FK.
    op.execute(
        sa.text(
            """
            UPDATE pacote p
            JOIN correcao c ON c.id = p.id_correcao
            JOIN produto pr ON pr.id = c.id_produto
            LEFT JOIN tipo_pacote tp ON tp.id = p.tp_pacote AND tp.nm_grupo = pr.nm_grupo_tipo_pacote
            SET p.tp_pacote = (SELECT MIN(id) FROM tipo_pacote WHERE nm_grupo = pr.nm_grupo_tipo_pacote)
            WHERE tp.id IS NULL
            """
        )
    )
    op.create_foreign_key("fk_pacote_tp_pacote_tipo_pacote", "pacote", "tipo_pacote", ["tp_pacote"], ["id"])

    op.alter_column("usuario", "id_produto", existing_type=sa.BigInteger(), nullable=True)


def downgrade() -> None:
    op.alter_column("usuario", "id_produto", existing_type=sa.BigInteger(), nullable=False)

    op.drop_constraint("fk_pacote_tp_pacote_tipo_pacote", "pacote", type_="foreignkey")
    op.drop_table("tipo_pacote")

    op.execute(sa.text("DELETE FROM produto WHERE id = 5"))
    op.drop_column("produto", "nm_grupo_tipo_pacote")
