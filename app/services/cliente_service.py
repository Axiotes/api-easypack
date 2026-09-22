from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.models.usuario import CargoUsuario, Usuario
from app.repositories import cliente_repository, usuario_repository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def _validar_coordenador_gerencia(usuario_atual: Usuario) -> None:
    if usuario_atual.cargo != CargoUsuario.COORDENADOR or usuario_atual.subsetor.sn_gerencia != "S":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas um coordenador do subsetor Gerência pode gerenciar clientes",
        )


def _validar_responsavel_gerente_projeto(db: Session, id_usuario: int) -> None:
    responsavel = usuario_repository.get_by_id(db, id_usuario)
    if responsavel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário responsável não encontrado")
    if responsavel.cargo != CargoUsuario.GERENTE_PROJETO:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O usuário responsável pelo cliente deve ter cargo Gerente de Projeto",
        )


def create_cliente(db: Session, data: ClienteCreate, usuario_atual: Usuario) -> Cliente:
    _validar_coordenador_gerencia(usuario_atual)
    _validar_responsavel_gerente_projeto(db, data.id_usuario)
    return cliente_repository.create(db, Cliente(**data.model_dump()))


def list_clientes(db: Session) -> list[Cliente]:
    return cliente_repository.list_all(db)


def get_cliente(db: Session, cliente_id: int) -> Cliente:
    cliente = cliente_repository.get_by_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return cliente


def update_cliente(db: Session, cliente_id: int, data: ClienteUpdate, usuario_atual: Usuario) -> Cliente:
    _validar_coordenador_gerencia(usuario_atual)
    cliente = get_cliente(db, cliente_id)

    changes = data.model_dump(exclude_unset=True)
    if "id_usuario" in changes:
        _validar_responsavel_gerente_projeto(db, changes["id_usuario"])

    for field, value in changes.items():
        setattr(cliente, field, value)
    return cliente_repository.update(db, cliente)


def delete_cliente(db: Session, cliente_id: int, usuario_atual: Usuario) -> None:
    _validar_coordenador_gerencia(usuario_atual)
    cliente_repository.delete(db, get_cliente(db, cliente_id))
