"""seed colegas pleno nos subsetores Prime Soul e Prime PEP

Os subsetores "Prime Soul" (id 4) e "Prime PEP" (id 5) so tinham o
usuario Estagiario, sem nenhum colega de cargo minimo Pleno no mesmo
subsetor para aprovar a aplicacao de pacote (regra do Estagiario).

Revision ID: b3f6e2a9c7d1
Revises: 7a1b708f2de3
Create Date: 2026-11-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b3f6e2a9c7d1"
down_revision: Union[str, None] = "7a1b708f2de3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# bcrypt hash of "admin123". The fixture password is for local demonstration only.
DEMO_SENHA_HASH = "$2b$12$I.vSFbhCec2l5YurMDtVu.lqPJ8r6caqBlvKnmq8R/7oPHpXcJZi2"


def upgrade() -> None:
    usuario = sa.table(
        "usuario",
        sa.column("id", sa.BigInteger),
        sa.column("nm_usuario", sa.String),
        sa.column("id_subsetor", sa.BigInteger),
        sa.column("cargo", sa.String),
        sa.column("id_produto", sa.BigInteger),
        sa.column("senha", sa.String),
        sa.column("nm_completo", sa.String),
    )
    op.bulk_insert(
        usuario,
        [
            {
                "id": 13,
                "nm_usuario": "rafael.pires",
                "id_subsetor": 4,
                "cargo": "PLENO",
                "id_produto": 1,
                "senha": DEMO_SENHA_HASH,
                "nm_completo": "Rafael Pires",
            },
            {
                "id": 14,
                "nm_usuario": "tatiana.rocha",
                "id_subsetor": 5,
                "cargo": "PLENO",
                "id_produto": 2,
                "senha": DEMO_SENHA_HASH,
                "nm_completo": "Tatiana Rocha",
            },
        ],
    )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM usuario WHERE id IN (13, 14)"))
