from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constantes import PRODUTOS_COM_ACESSO_A_PAGU, PRODUTO_PAGU, SG_SETOR_FABRICA
from app.models.correcao import Correcao
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.repositories import correcao_repository, produto_repository, usuario_repository
from app.schemas.correcao import CorrecaoCreate, CorrecaoUpdate


def _validar_produto_usuario(db: Session, id_usuario: int, id_produto: int) -> None:
    usuario = usuario_repository.get_by_id(db, id_usuario)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário responsável não encontrado")
    produto = produto_repository.get_by_id(db, id_produto)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    validar_acesso_produto(usuario, produto)


def validar_acesso_produto(usuario: Usuario, produto: Produto) -> None:
    nm_produto_usuario = usuario.produto.nm_produto
    nm_produto_correcao = produto.nm_produto

    if nm_produto_usuario == nm_produto_correcao:
        return
    if nm_produto_correcao == PRODUTO_PAGU and nm_produto_usuario in PRODUTOS_COM_ACESSO_A_PAGU:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=(
            f"Usuário do produto {nm_produto_usuario} não pode ser responsável por "
            f"correções do produto {nm_produto_correcao}"
        ),
    )


def create_correcao(db: Session, data: CorrecaoCreate) -> Correcao:
    _validar_produto_usuario(db, data.id_usuario, data.id_produto)
    correcao = Correcao(**data.model_dump(), sn_aprovado_code_review="N")
    return correcao_repository.create(db, correcao)


def list_correcoes(db: Session) -> list[Correcao]:
    return correcao_repository.list_all(db)


def get_correcao(db: Session, correcao_id: int) -> Correcao:
    correcao = correcao_repository.get_by_id(db, correcao_id)
    if correcao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Correção não encontrada")
    return correcao


def update_correcao(db: Session, correcao_id: int, data: CorrecaoUpdate) -> Correcao:
    correcao = get_correcao(db, correcao_id)
    changes = data.model_dump(exclude_unset=True)

    if "id_usuario" in changes or "id_produto" in changes:
        novo_usuario = changes.get("id_usuario", correcao.id_usuario)
        novo_produto = changes.get("id_produto", correcao.id_produto)
        _validar_produto_usuario(db, novo_usuario, novo_produto)

    for field, value in changes.items():
        setattr(correcao, field, value)
    return correcao_repository.update(db, correcao)


def aprovar_correcao(db: Session, correcao_id: int, usuario_atual: Usuario) -> Correcao:
    correcao = get_correcao(db, correcao_id)

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
    return correcao_repository.update(db, correcao)


def delete_correcao(db: Session, correcao_id: int, usuario_atual: Usuario) -> None:
    correcao = get_correcao(db, correcao_id)

    if usuario_atual.id_produto != correcao.id_produto:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Coordenador só pode deletar correções do seu próprio produto",
        )

    correcao_repository.delete(db, correcao)
