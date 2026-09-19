from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories import cliente_repository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def create_cliente(db: Session, data: ClienteCreate) -> Cliente:
    return cliente_repository.create(db, Cliente(**data.model_dump()))


def list_clientes(db: Session) -> list[Cliente]:
    return cliente_repository.list_all(db)


def get_cliente(db: Session, cliente_id: int) -> Cliente:
    cliente = cliente_repository.get_by_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return cliente


def update_cliente(db: Session, cliente_id: int, data: ClienteUpdate) -> Cliente:
    cliente = get_cliente(db, cliente_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, field, value)
    return cliente_repository.update(db, cliente)


def delete_cliente(db: Session, cliente_id: int) -> None:
    cliente_repository.delete(db, get_cliente(db, cliente_id))
