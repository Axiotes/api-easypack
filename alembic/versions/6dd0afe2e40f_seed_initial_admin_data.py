"""seed initial admin data

Revision ID: 6dd0afe2e40f
Revises: 774d228dcd30
Create Date: 2026-09-17 23:09:01.269993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dd0afe2e40f'
down_revision: Union[str, None] = '774d228dcd30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# bcrypt hash of "admin123" — troque a senha do usuário admin assim que possível.
ADMIN_SENHA_HASH = "$2b$12$I.vSFbhCec2l5YurMDtVu.lqPJ8r6caqBlvKnmq8R/7oPHpXcJZi2"


def upgrade() -> None:
    conn = op.get_bind()

    setor = sa.table(
        "setor",
        sa.column("id", sa.BigInteger),
        sa.column("nm_setor", sa.String),
    )
    produto = sa.table(
        "produto",
        sa.column("id", sa.BigInteger),
        sa.column("nm_produto", sa.String),
    )
    subsetor = sa.table(
        "subsetor",
        sa.column("id", sa.BigInteger),
        sa.column("id_setor", sa.BigInteger),
        sa.column("nm_subsetor", sa.String),
        sa.column("id_produto", sa.BigInteger),
    )
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

    conn.execute(setor.insert().values(id=1, nm_setor="TI"))
    conn.execute(produto.insert().values(id=1, nm_produto="Sistema Principal"))
    conn.execute(
        subsetor.insert().values(id=1, id_setor=1, nm_subsetor="Suporte N1", id_produto=1)
    )
    conn.execute(
        usuario.insert().values(
            id=1,
            nm_usuario="admin",
            id_subsetor=1,
            cargo="ADMIN",
            id_produto=1,
            senha=ADMIN_SENHA_HASH,
            nm_completo="Administrador do Sistema",
        )
    )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM usuario WHERE id = 1"))
    op.execute(sa.text("DELETE FROM subsetor WHERE id = 1"))
    op.execute(sa.text("DELETE FROM produto WHERE id = 1"))
    op.execute(sa.text("DELETE FROM setor WHERE id = 1"))
