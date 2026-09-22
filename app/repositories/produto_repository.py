from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.produto import Produto


def get_by_id(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)


def list_all(db: Session) -> list[Produto]:
    return list(db.scalars(select(Produto)).all())
