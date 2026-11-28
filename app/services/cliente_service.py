from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import auditoria
from app.models.cliente import Cliente
from app.models.usuario import CargoUsuario, Usuario
from app.repositories import cliente_repository, usuario_repository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


def _validar_gerente_projeto(usuario_atual: Usuario) -> None:
    if usuario_atual.cargo != CargoUsuario.GERENTE_PROJETO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas um Gerente de Projeto pode gerenciar clientes",
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
    _validar_gerente_projeto(usuario_atual)
    _validar_responsavel_gerente_projeto(db, data.id_usuario)
    cliente = cliente_repository.create(db, Cliente(**data.model_dump()))
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CLIENTE, cliente.id, auditoria.ACAO_CRIAR,
        f"Cliente {cliente.nm_cliente} cadastrado",
    )
    return cliente


def list_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    return cliente_repository.list_all(db, skip=skip, limit=limit)


def search_clientes(db: Session, nome: str, skip: int = 0, limit: int = 100) -> list[Cliente]:
    return cliente_repository.search_by_name(db, nome, skip=skip, limit=limit)


def get_cliente(db: Session, cliente_id: int) -> Cliente:
    cliente = cliente_repository.get_by_id(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return cliente


def update_cliente(db: Session, cliente_id: int, data: ClienteUpdate, usuario_atual: Usuario) -> Cliente:
    _validar_gerente_projeto(usuario_atual)
    cliente = get_cliente(db, cliente_id)

    changes = data.model_dump(exclude_unset=True)
    if "id_usuario" in changes:
        _validar_responsavel_gerente_projeto(db, changes["id_usuario"])

    for field, value in changes.items():
        setattr(cliente, field, value)
    cliente = cliente_repository.update(db, cliente)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CLIENTE, cliente.id, auditoria.ACAO_ATUALIZAR,
        f"Cliente {cliente.nm_cliente} atualizado",
    )
    return cliente


def delete_cliente(db: Session, cliente_id: int, usuario_atual: Usuario) -> None:
    _validar_gerente_projeto(usuario_atual)
    cliente = get_cliente(db, cliente_id)
    cliente_id_registrado, nm_cliente_registrado = cliente.id, cliente.nm_cliente
    cliente_repository.delete(db, cliente)
    auditoria.registrar(
        db, usuario_atual, auditoria.ENTIDADE_CLIENTE, cliente_id_registrado, auditoria.ACAO_EXCLUIR,
        f"Cliente {nm_cliente_registrado} excluído",
    )
