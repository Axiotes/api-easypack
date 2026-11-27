from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.setor import Setor


def get_by_id(db: Session, setor_id: int) -> Setor | None:
    return db.get(Setor, setor_id)


def list_all(db: Session) -> list[Setor]:
    return list(db.scalars(select(Setor)).all())
