from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database.session import get_db
from app.models.pacote import Pacote
from app.models.usuario import CargoUsuario, Usuario
from app.schemas.pacote import PacoteCreate, PacoteRead, PacoteUpdate
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


@router.delete("/pacotes/{pacote_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pacote(
    pacote_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(CargoUsuario.ADMIN, CargoUsuario.GERENTE)),
) -> None:
    pacote_service.delete_pacote(db, pacote_id)
