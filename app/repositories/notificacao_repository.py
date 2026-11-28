from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notificacao import Notificacao


def create(db: Session, notificacao: Notificacao) -> Notificacao:
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao


def get_by_id(db: Session, notificacao_id: int) -> Notificacao | None:
    return db.get(Notificacao, notificacao_id)


def list_pendentes_por_usuario(db: Session, id_usuario: int) -> list[Notificacao]:
    query = select(Notificacao).where(
        Notificacao.id_usuario == id_usuario,
        Notificacao.lido.is_(False),
    )
    return list(db.scalars(query).all())


def update(db: Session, notificacao: Notificacao) -> Notificacao:
    db.commit()
    db.refresh(notificacao)
    return notificacao
