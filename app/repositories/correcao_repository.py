from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.correcao import Correcao


def get_by_id(db: Session, correcao_id: int) -> Correcao | None:
    return db.get(Correcao, correcao_id)


def list_all(db: Session) -> list[Correcao]:
    return list(db.scalars(select(Correcao)).all())


def create(db: Session, correcao: Correcao) -> Correcao:
    db.add(correcao)
    db.commit()
    db.refresh(correcao)
    return correcao


def update(db: Session, correcao: Correcao) -> Correcao:
    db.commit()
    db.refresh(correcao)
    return correcao


def delete(db: Session, correcao: Correcao) -> None:
    db.delete(correcao)
    db.commit()
