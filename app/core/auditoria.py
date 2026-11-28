from sqlalchemy.orm import Session

from app.models.log_operacao import LogOperacao
from app.models.usuario import Usuario
from app.repositories import log_operacao_repository

# Entidades auditadas.
ENTIDADE_CORRECAO = "Correcao"
ENTIDADE_PACOTE = "Pacote"
ENTIDADE_USUARIO = "Usuario"
ENTIDADE_CLIENTE = "Cliente"

# Ações auditadas.
ACAO_CRIAR = "CRIAR"
ACAO_ATUALIZAR = "ATUALIZAR"
ACAO_EXCLUIR = "EXCLUIR"
ACAO_APROVAR_CODE_REVIEW = "APROVAR_CODE_REVIEW"
ACAO_ALTERAR_MERGE = "ALTERAR_MERGE"
ACAO_APROVAR_GERENTE = "APROVAR_GERENTE"
ACAO_APLICAR = "APLICAR"


def registrar(
    db: Session,
    usuario_atual: Usuario,
    nm_entidade: str,
    id_entidade: int,
    ds_acao: str,
    ds_detalhe: str,
) -> None:
    """Grava uma entrada no histórico de operações. Não interrompe a operação principal em caso de falha."""
    log = LogOperacao(
        id_usuario=usuario_atual.id,
        nm_usuario=usuario_atual.nm_usuario,
        nm_entidade=nm_entidade,
        id_entidade=id_entidade,
        ds_acao=ds_acao,
        ds_detalhe=ds_detalhe,
    )
    log_operacao_repository.create(db, log)
