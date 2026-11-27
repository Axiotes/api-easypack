from sqlalchemy.orm import Session

from app.models.notificacao import Notificacao


def create(db: Session, notificacao: Notificacao) -> Notificacao:
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao
