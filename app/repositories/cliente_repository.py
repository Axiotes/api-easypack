from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente


def get_by_id(db: Session, cliente_id: int) -> Cliente | None:
    return db.get(Cliente, cliente_id)


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    statement = select(Cliente).order_by(Cliente.id).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def search_by_name(db: Session, nome: str, skip: int = 0, limit: int = 100) -> list[Cliente]:
    statement = (
        select(Cliente)
        .where(Cliente.nm_cliente.icontains(nome, autoescape=True))
        .order_by(Cliente.id)
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


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
