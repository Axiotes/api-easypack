from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import auditoria
from app.core.cargo import CARGOS_APROVACAO_CODE_REVIEW
from app.core.constantes import SG_SETOR_FABRICA
from app.core.produto import produto_atende
from app.models.correcao import Correcao
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.repositories import correcao_repository, produto_repository, usuario_repository
from app.schemas.correcao import CorrecaoCreate, CorrecaoMergeRequest, CorrecaoUpdate


def _validar_produto_usuario(db: Session, id_usuario: int, id_produto: int) -> None:
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário responsável não encontrado")
    if usuario.produto is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Usuário responsável não possui produto definido",
        )
    produto = produto_repository.get_by_id(db, id_produto)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    if produto_atende(usuario.produto.nm_produto, produto.nm_produto):
        return

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=(
            f"Usuário do produto {usuario.produto.nm_produto} não pode ser responsável por "
            f"correções do produto {produto.nm_produto}"
        ),
    )


def create_correcao(db: Session, data: CorrecaoCreate, usuario_atual: Usuario) -> Correcao:
    _validar_produto_usuario(db, data.id_usuario, data.id_produto)
    correcao = Correcao(**data.model_dump(), sn_aprovado_code_review="N")
    correcao = correcao_repository.create(db, correcao)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CORRECAO, correcao.id, auditoria.ACAO_CRIAR,
        f"Correção {correcao.ticket} cadastrada",
    )
    return correcao


def list_correcoes(db: Session) -> list[Correcao]:
    return correcao_repository.list_all(db)


def get_correcao(db: Session, correcao_id: int) -> Correcao:
    correcao = correcao_repository.get_by_id(db, correcao_id)
    if correcao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Correção não encontrada")
    return correcao


def update_correcao(db: Session, correcao_id: int, data: CorrecaoUpdate, usuario_atual: Usuario) -> Correcao:
    correcao = get_correcao(db, correcao_id)
    changes = data.model_dump(exclude_unset=True)

    if "id_usuario" in changes or "id_produto" in changes:
        novo_usuario = changes.get("id_usuario", correcao.id_usuario)
        novo_produto = changes.get("id_produto", correcao.id_produto)
        _validar_produto_usuario(db, novo_usuario, novo_produto)

    for field, value in changes.items():
        setattr(correcao, field, value)
    correcao = correcao_repository.update(db, correcao)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CORRECAO, correcao.id, auditoria.ACAO_ATUALIZAR,
        f"Correção {correcao.ticket} atualizada",
    )
    return correcao


def aprovar_correcao(db: Session, correcao_id: int, usuario_atual: Usuario) -> Correcao:
    correcao = get_correcao(db, correcao_id)

    if usuario_atual.cargo not in CARGOS_APROVACAO_CODE_REVIEW:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas um usuário com cargo de desenvolvimento pode aprovar o code review",
        )
    if usuario_atual.subsetor.setor.sg_setor != SG_SETOR_FABRICA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas um usuário do setor Fábrica pode aprovar uma correção",
        )
    if usuario_atual.id_produto != correcao.id_produto:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário aprovador deve pertencer ao mesmo produto da correção",
        )

    correcao.sn_aprovado_code_review = "S"
    correcao.id_usuario_aprovador = usuario_atual.id
    correcao = correcao_repository.update(db, correcao)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CORRECAO, correcao.id, auditoria.ACAO_APROVAR_CODE_REVIEW,
        f"Code review da correção {correcao.ticket} aprovado",
    )
    return correcao


def alterar_mergeado(db: Session, correcao_id: int, usuario_atual: Usuario, data: CorrecaoMergeRequest) -> Correcao:
    correcao = get_correcao(db, correcao_id)

    if usuario_atual.subsetor.id_setor != correcao.id_setor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário só pode alterar o status de merge de correções do próprio setor",
        )
    if data.sn_mergeado == "S" and correcao.sn_aprovado_code_review != "S":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não é possível marcar a correção como mergeada sem o code review aprovado",
        )

    correcao.sn_mergeado = data.sn_mergeado
    correcao = correcao_repository.update(db, correcao)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CORRECAO, correcao.id, auditoria.ACAO_ALTERAR_MERGE,
        f"Status de merge da correção {correcao.ticket} alterado para "
        f"{'mergeado' if data.sn_mergeado == 'S' else 'não mergeado'}",
    )
    return correcao


def delete_correcao(db: Session, correcao_id: int, usuario_atual: Usuario) -> None:
    correcao = get_correcao(db, correcao_id)

    if usuario_atual.id_produto != correcao.id_produto:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coordenador só pode deletar correções do seu próprio produto",
        )

    correcao_id_registrado, ticket_registrado = correcao.id, correcao.ticket
    correcao_repository.delete(db, correcao)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CORRECAO, correcao_id_registrado, auditoria.ACAO_EXCLUIR,
        f"Correção {ticket_registrado} excluída",
    )
