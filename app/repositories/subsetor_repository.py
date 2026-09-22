from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.subsetor import Subsetor


def get_by_id(db: Session, subsetor_id: int) -> Subsetor | None:
    return db.get(Subsetor, subsetor_id)


def list_all(db: Session) -> list[Subsetor]:
    return list(db.scalars(select(Subsetor)).all())
