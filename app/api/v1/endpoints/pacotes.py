from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database.session import get_db
from app.models.pacote import Pacote
from app.models.usuario import CargoUsuario, Usuario
from app.schemas.pacote import (
    PacoteAplicarRequest, PacoteContagemFiltros, PacoteContagemRead,
    PacoteCreate, PacoteRead, PacoteUpdate,
)
from app.services import pacote_service

router = APIRouter()


@router.post("/pacotes", response_model=PacoteRead, status_code=status.HTTP_201_CREATED)
def cadastrar_pacote(
    data: PacoteCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Pacote:
    return pacote_service.create_pacote(db, data)


@router.get("/pacotes", response_model=list[PacoteRead])
def listar_pacotes(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> list[Pacote]:
    return pacote_service.list_pacotes(db)


@router.get("/pacotes/contagem", response_model=PacoteContagemRead)
def contar_pacotes(
    filtros: Annotated[PacoteContagemFiltros, Query()],
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> PacoteContagemRead:
    return pacote_service.count_pacotes(db, filtros)


@router.get("/pacotes/{pacote_id}", response_model=PacoteRead)
def obter_pacote(
    pacote_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Pacote:
    return pacote_service.get_pacote(db, pacote_id)


@router.put("/pacotes/{pacote_id}", response_model=PacoteRead)
def atualizar_pacote(
    pacote_id: int,
    data: PacoteUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Pacote:
    return pacote_service.update_pacote(db, pacote_id, data)


@router.post("/pacotes/{pacote_id}/aprovar-gerente", response_model=PacoteRead)
def aprovar_pacote_gerente(
    pacote_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(require_roles(CargoUsuario.GERENTE_PROJETO)),
) -> Pacote:
    return pacote_service.aprovar_pacote_gerente(db, pacote_id, usuario_atual)


@router.post("/pacotes/{pacote_id}/aplicar", response_model=PacoteRead)
def aplicar_pacote(
    pacote_id: int,
    data: PacoteAplicarRequest,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user),
) -> Pacote:
    return pacote_service.aplicar_pacote(db, pacote_id, usuario_atual, data)


@router.delete("/pacotes/{pacote_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pacote(
    pacote_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> None:
    pacote_service.delete_pacote(db, pacote_id)
