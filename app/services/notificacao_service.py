from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notificacao import Notificacao
from app.models.usuario import Usuario
from app.repositories import notificacao_repository, usuario_repository
from app.schemas.notificacao import NotificacaoCreate


def create_notificacao(db: Session, data: NotificacaoCreate) -> Notificacao:
    if usuario_repository.get_by_id(db, data.id_usuario) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    notificacao = Notificacao(**data.model_dump())
    return notificacao_repository.create(db, notificacao)


def marcar_como_lida(db: Session, notificacao_id: int, usuario_atual: Usuario) -> Notificacao:
    notificacao = notificacao_repository.get_by_id(db, notificacao_id)
    if notificacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificação não encontrada")
    if notificacao.id_usuario != usuario_atual.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Notificação não pertence ao usuário")

    notificacao.lido = True
    return notificacao_repository.update(db, notificacao)
