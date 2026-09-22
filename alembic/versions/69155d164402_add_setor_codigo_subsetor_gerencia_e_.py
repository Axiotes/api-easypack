"""add setor codigo subsetor gerencia e colunas de auditoria de aprovacao

Revision ID: 69155d164402
Revises: 9b7c3d1e2f4a
Create Date: 2026-09-21 21:43:30.057304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69155d164402'
down_revision: Union[str, None] = '9b7c3d1e2f4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("setor", sa.Column("sg_setor", sa.String(length=10), nullable=True))
    op.execute(sa.text("UPDATE setor SET sg_setor = 'FB' WHERE id = 1"))
    op.execute(sa.text("UPDATE setor SET sg_setor = 'ST' WHERE id = 2"))
    op.alter_column("setor", "sg_setor", existing_type=sa.String(length=10), nullable=False)
    op.create_unique_constraint("uq_setor_sg_setor", "setor", ["sg_setor"])

    op.add_column(
        "subsetor",
        sa.Column("sn_gerencia", sa.CHAR(length=1), nullable=False, server_default="N"),
    )
    op.execute(sa.text("UPDATE subsetor SET sn_gerencia = 'S' WHERE id IN (1, 8)"))

    op.add_column("pacote", sa.Column("id_usuario_aplicacao", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_pacote_id_usuario_aplicacao_usuario", "pacote", "usuario", ["id_usuario_aplicacao"], ["id"]
    )
    op.add_column("pacote", sa.Column("id_usuario_aprovador_gerente", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_pacote_id_usuario_aprovador_gerente_usuario",
        "pacote",
        "usuario",
        ["id_usuario_aprovador_gerente"],
        ["id"],
    )
    op.add_column("pacote", sa.Column("id_usuario_aprovador_par", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_pacote_id_usuario_aprovador_par_usuario", "pacote", "usuario", ["id_usuario_aprovador_par"], ["id"]
    )

    op.add_column("correcao", sa.Column("id_usuario_aprovador", sa.BigInteger(), nullable=True))
    op.create_foreign_key(
        "fk_correcao_id_usuario_aprovador_usuario", "correcao", "usuario", ["id_usuario_aprovador"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_correcao_id_usuario_aprovador_usuario", "correcao", type_="foreignkey")
    op.drop_column("correcao", "id_usuario_aprovador")

    op.drop_constraint("fk_pacote_id_usuario_aprovador_par_usuario", "pacote", type_="foreignkey")
    op.drop_column("pacote", "id_usuario_aprovador_par")
    op.drop_constraint("fk_pacote_id_usuario_aprovador_gerente_usuario", "pacote", type_="foreignkey")
    op.drop_column("pacote", "id_usuario_aprovador_gerente")
    op.drop_constraint("fk_pacote_id_usuario_aplicacao_usuario", "pacote", type_="foreignkey")
    op.drop_column("pacote", "id_usuario_aplicacao")

    op.drop_column("subsetor", "sn_gerencia")

    op.drop_constraint("uq_setor_sg_setor", "setor", type_="unique")
    op.drop_column("setor", "sg_setor")
