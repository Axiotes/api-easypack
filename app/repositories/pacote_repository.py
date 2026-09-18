from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pacote import Pacote


def get_by_id(db: Session, pacote_id: int) -> Pacote | None:
    return db.get(Pacote, pacote_id)


def list_all(db: Session) -> list[Pacote]:
    return list(db.scalars(select(Pacote)).all())


def create(db: Session, pacote: Pacote) -> Pacote:
    db.add(pacote)
    db.commit()
    db.refresh(pacote)
    return pacote


def update(db: Session, pacote: Pacote) -> Pacote:
    db.commit()
    db.refresh(pacote)
    return pacote


def delete(db: Session, pacote: Pacote) -> None:
    db.delete(pacote)
    db.commit()
