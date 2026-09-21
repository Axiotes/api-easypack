from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente


def get_by_id(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def list_all(db: Session) -> list[Cliente]:
    return list(db.scalars(select(Cliente)).all())


def create(db: Session, cliente: Cliente) -> Cliente:
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update(db: Session, cliente: Cliente) -> Cliente:
    db.commit()
    db.refresh(cliente)
    return cliente


def delete(db: Session, cliente: Cliente) -> None:
    db.delete(cliente)
    db.commit()
