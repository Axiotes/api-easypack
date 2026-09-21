from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from app.services import cliente_service

router = APIRouter()


@router.post("/clientes", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(data: ClienteCreate, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Cliente:
    return cliente_service.create_cliente(db, data)


@router.get("/clientes", response_model=list[ClienteRead])
def listar_clientes(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> list[Cliente]:
    return cliente_service.list_clientes(db)


@router.get("/clientes/{cliente_id}", response_model=ClienteRead)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Cliente:
    return cliente_service.get_cliente(db, cliente_id)


@router.put("/clientes/{cliente_id}", response_model=ClienteRead)
def atualizar_cliente(cliente_id: int, data: ClienteUpdate, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Cliente:
    return cliente_service.update_cliente(db, cliente_id, data)


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> None:
    cliente_service.delete_cliente(db, cliente_id)
