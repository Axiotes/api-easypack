"""seed release governance catalog and demonstration data

Revision ID: 9b7c3d1e2f4a
Revises: 8c4e7a9d1b2f
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9b7c3d1e2f4a"
down_revision: Union[str, None] = "8c4e7a9d1b2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# bcrypt hash of "admin123". The fixture password is for local demonstration only.
DEMO_SENHA_HASH = "$2b$12$I.vSFbhCec2l5YurMDtVu.lqPJ8r6caqBlvKnmq8R/7oPHpXcJZi2"


def upgrade() -> None:
    produto = sa.table("produto", sa.column("id", sa.BigInteger), sa.column("nm_produto", sa.String))
    setor = sa.table("setor", sa.column("id", sa.BigInteger), sa.column("nm_setor", sa.String))
    subsetor = sa.table("subsetor", sa.column("id", sa.BigInteger), sa.column("id_setor", sa.BigInteger), sa.column("nm_subsetor", sa.String), sa.column("id_produto", sa.BigInteger))
    usuario = sa.table("usuario", sa.column("id", sa.BigInteger), sa.column("nm_usuario", sa.String), sa.column("id_subsetor", sa.BigInteger), sa.column("cargo", sa.String), sa.column("id_produto", sa.BigInteger), sa.column("senha", sa.String), sa.column("nm_completo", sa.String))
    cliente = sa.table("cliente", sa.column("id", sa.BigInteger), sa.column("nm_cliente", sa.String), sa.column("id_setor_atendimento", sa.BigInteger), sa.column("id_usuario", sa.BigInteger))
    correcao = sa.table("correcao", sa.column("id", sa.BigInteger), sa.column("ticket", sa.String), sa.column("ticket_bug", sa.String), sa.column("merge", sa.String), sa.column("id_cliente", sa.BigInteger), sa.column("id_produto", sa.BigInteger), sa.column("id_usuario", sa.BigInteger), sa.column("id_setor", sa.BigInteger), sa.column("sn_mergeado", sa.CHAR), sa.column("versao_correcao", sa.String), sa.column("sn_aprovado_code_review", sa.CHAR))
    pacote = sa.table("pacote", sa.column("id", sa.BigInteger), sa.column("id_correcao", sa.BigInteger), sa.column("sn_aplicado", sa.CHAR), sa.column("tp_pacote", sa.BigInteger), sa.column("nm_pacote", sa.String), sa.column("sn_aprovado_usu", sa.CHAR), sa.column("sn_aprovado_gerente", sa.CHAR))

    # Transforms the original admin seed so the catalog contains only the requested values.
    op.execute(sa.text("UPDATE produto SET nm_produto = 'Soul' WHERE id = 1"))
    op.execute(sa.text("UPDATE setor SET nm_setor = 'Fábrica (FB)' WHERE id = 1"))
    op.bulk_insert(setor, [{"id": 2, "nm_setor": "Serviços Técnicos (ST)"}])
    op.execute(sa.text("UPDATE subsetor SET id_setor = 2, nm_subsetor = 'Gerencia GPs ST', id_produto = NULL WHERE id = 1"))
    op.execute(sa.text("UPDATE usuario SET nm_usuario = 'maria.silva', id_subsetor = 1, id_produto = 1, nm_completo = 'Maria Luisa da Silva' WHERE id = 1"))

    op.bulk_insert(produto, [
        {"id": 2, "nm_produto": "PEP"}, {"id": 3, "nm_produto": "Pagu"}, {"id": 4, "nm_produto": "SACR"},
    ])
    op.bulk_insert(subsetor, [
        {"id": 2, "id_setor": 2, "nm_subsetor": "Dev Soul ST", "id_produto": 1},
        {"id": 3, "id_setor": 2, "nm_subsetor": "Dev PEP ST", "id_produto": 2},
        {"id": 4, "id_setor": 2, "nm_subsetor": "Prime Soul", "id_produto": 1},
        {"id": 5, "id_setor": 2, "nm_subsetor": "Prime PEP", "id_produto": 2},
        {"id": 6, "id_setor": 1, "nm_subsetor": "Dev PEP FB", "id_produto": 2},
        {"id": 7, "id_setor": 1, "nm_subsetor": "Dev Soul FB", "id_produto": 1},
        {"id": 8, "id_setor": 1, "nm_subsetor": "Gerencia GPs FB", "id_produto": None},
    ])
    op.bulk_insert(usuario, [
        {"id": 2, "nm_usuario": "bruno.silva", "id_subsetor": 2, "cargo": "GERENTE_PROJETO", "id_produto": 1, "senha": DEMO_SENHA_HASH, "nm_completo": "Bruno Silva"},
        {"id": 3, "nm_usuario": "carla.souza", "id_subsetor": 3, "cargo": "GERENTE_PROJETO", "id_produto": 2, "senha": DEMO_SENHA_HASH, "nm_completo": "Carla Souza"},
        {"id": 4, "nm_usuario": "diego.lima", "id_subsetor": 7, "cargo": "GERENTE_PROJETO", "id_produto": 1, "senha": DEMO_SENHA_HASH, "nm_completo": "Diego Lima"},
        {"id": 5, "nm_usuario": "elisa.costa", "id_subsetor": 6, "cargo": "GERENTE_PROJETO", "id_produto": 2, "senha": DEMO_SENHA_HASH, "nm_completo": "Elisa Costa"},
        {"id": 6, "nm_usuario": "felipe.rocha", "id_subsetor": 2, "cargo": "ESPECIALISTA", "id_produto": 1, "senha": DEMO_SENHA_HASH, "nm_completo": "Felipe Rocha"},
        {"id": 7, "nm_usuario": "gabriela.alves", "id_subsetor": 3, "cargo": "SENIOR", "id_produto": 2, "senha": DEMO_SENHA_HASH, "nm_completo": "Gabriela Alves"},
        {"id": 8, "nm_usuario": "henrique.melo", "id_subsetor": 7, "cargo": "PLENO", "id_produto": 1, "senha": DEMO_SENHA_HASH, "nm_completo": "Henrique Melo"},
        {"id": 9, "nm_usuario": "isabela.nunes", "id_subsetor": 6, "cargo": "JUNIOR", "id_produto": 2, "senha": DEMO_SENHA_HASH, "nm_completo": "Isabela Nunes"},
        {"id": 10, "nm_usuario": "joao.freitas", "id_subsetor": 4, "cargo": "ESTAGIARIO", "id_produto": 1, "senha": DEMO_SENHA_HASH, "nm_completo": "João Freitas"},
        {"id": 11, "nm_usuario": "karen.martins", "id_subsetor": 5, "cargo": "ESTAGIARIO", "id_produto": 2, "senha": DEMO_SENHA_HASH, "nm_completo": "Karen Martins"},
        {"id": 12, "nm_usuario": "lucas.barros", "id_subsetor": 8, "cargo": "COORDENADOR", "id_produto": 2, "senha": DEMO_SENHA_HASH, "nm_completo": "Lucas Barros"},
    ])
    op.bulk_insert(cliente, [
        {"id": 1, "nm_cliente": "Cliente Aurora", "id_setor_atendimento": 2, "id_usuario": 2},
        {"id": 2, "nm_cliente": "Cliente Horizonte", "id_setor_atendimento": 2, "id_usuario": 3},
        {"id": 3, "nm_cliente": "Cliente Pioneiro", "id_setor_atendimento": 1, "id_usuario": 4},
        {"id": 4, "nm_cliente": "Cliente Vértice", "id_setor_atendimento": 1, "id_usuario": 5},
    ])
    op.bulk_insert(correcao, [
        {"id": 1, "ticket": "SOUL-100", "ticket_bug": "BUG-100", "merge": "release/soul-1.0.1", "id_cliente": 1, "id_produto": 1, "id_usuario": 8, "id_setor": 1, "sn_mergeado": "S", "versao_correcao": "1.0.1", "sn_aprovado_code_review": "S"},
        {"id": 2, "ticket": "PEP-200", "ticket_bug": "BUG-200", "merge": "release/pep-2.3.1", "id_cliente": 2, "id_produto": 2, "id_usuario": 9, "id_setor": 1, "sn_mergeado": "S", "versao_correcao": "2.3.1", "sn_aprovado_code_review": "S"},
    ])
    op.bulk_insert(pacote, [
        {"id": 1, "id_correcao": 1, "sn_aplicado": "S", "tp_pacote": 1, "nm_pacote": "pacote-soul-1.0.1", "sn_aprovado_usu": "S", "sn_aprovado_gerente": "S"},
        {"id": 2, "id_correcao": 2, "sn_aplicado": "N", "tp_pacote": 1, "nm_pacote": "pacote-pep-2.3.1", "sn_aprovado_usu": "S", "sn_aprovado_gerente": "S"},
    ])


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM pacote WHERE id IN (1, 2)"))
    op.execute(sa.text("DELETE FROM correcao WHERE id IN (1, 2)"))
    op.execute(sa.text("DELETE FROM cliente WHERE id IN (1, 2, 3, 4)"))
    op.execute(sa.text("DELETE FROM usuario WHERE id BETWEEN 2 AND 12"))
    op.execute(sa.text("DELETE FROM subsetor WHERE id BETWEEN 2 AND 8"))
    op.execute(sa.text("DELETE FROM produto WHERE id BETWEEN 2 AND 4"))
    op.execute(sa.text("UPDATE usuario SET id_subsetor = 1, id_produto = 1, nm_completo = 'Administrador do Sistema' WHERE id = 1"))
    op.execute(sa.text("UPDATE subsetor SET id_setor = 1, nm_subsetor = 'Suporte N1', id_produto = 1 WHERE id = 1"))
    op.execute(sa.text("DELETE FROM setor WHERE id = 2"))
    op.execute(sa.text("UPDATE produto SET nm_produto = 'Sistema Principal' WHERE id = 1"))
    op.execute(sa.text("UPDATE setor SET nm_setor = 'TI' WHERE id = 1"))
