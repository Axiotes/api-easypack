"""merge notificacoes e historico de operacoes

Revision ID: 507784db0606
Revises: d4a7c1e9b6f2, 2f4a8c1d6e90
Create Date: 2026-11-27 22:55:16.149002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '507784db0606'
down_revision: Union[str, None] = ('d4a7c1e9b6f2', '2f4a8c1d6e90')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
