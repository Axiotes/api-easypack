from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notificacao import Notificacao
from app.repositories import notificacao_repository, usuario_repository
from app.schemas.notificacao import NotificacaoCreate


def create_notificacao(db: Session, data: NotificacaoCreate) -> Notificacao:
    if usuario_repository.get_by_id(db, data.id_usuario) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    notificacao = Notificacao(**data.model_dump())
    return notificacao_repository.create(db, notificacao)
