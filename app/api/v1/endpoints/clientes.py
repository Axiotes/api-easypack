from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from app.services import cliente_service

router = APIRouter()


@router.post("/clientes", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(
    data: ClienteCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user),
) -> Cliente:
    return cliente_service.create_cliente(db, data, usuario_atual)


@router.get("/clientes", response_model=list[ClienteRead])
def listar_clientes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> list[Cliente]:
    return cliente_service.list_clientes(db, skip=skip, limit=limit)


@router.get("/clientes/busca", response_model=list[ClienteRead])
def buscar_clientes(
    nome: str = Query(min_length=1, max_length=255),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> list[Cliente]:
    return cliente_service.search_clientes(db, nome, skip=skip, limit=limit)


@router.get("/clientes/{cliente_id}", response_model=ClienteRead)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Cliente:
    return cliente_service.get_cliente(db, cliente_id)


@router.put("/clientes/{cliente_id}", response_model=ClienteRead)
def atualizar_cliente(
    cliente_id: int,
    data: ClienteUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user),
) -> Cliente:
    return cliente_service.update_cliente(db, cliente_id, data, usuario_atual)


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user),
) -> None:
    cliente_service.delete_cliente(db, cliente_id, usuario_atual)
