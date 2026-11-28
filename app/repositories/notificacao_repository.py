from sqlalchemy.orm import Session

from app.models.notificacao import Notificacao


def create(db: Session, notificacao: Notificacao) -> Notificacao:
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao


def get_by_id(db: Session, notificacao_id: int) -> Notificacao | None:
    return db.get(Notificacao, notificacao_id)


def update(db: Session, notificacao: Notificacao) -> Notificacao:
    db.commit()
    db.refresh(notificacao)
    return notificacao
