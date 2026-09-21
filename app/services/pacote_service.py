from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pacote import Pacote
from app.repositories import pacote_repository
from app.schemas.pacote import PacoteCreate, PacoteUpdate


def create_pacote(db: Session, data: PacoteCreate) -> Pacote:
    pacote = Pacote(**data.model_dump())
    return pacote_repository.create(db, pacote)


def list_pacotes(db: Session) -> list[Pacote]:
    return pacote_repository.list_all(db)


def get_pacote(db: Session, pacote_id: int) -> Pacote:
    pacote = pacote_repository.get_by_id(db, pacote_id)
    if pacote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacote não encontrado")
    return pacote


def update_pacote(db: Session, pacote_id: int, data: PacoteUpdate) -> Pacote:
    pacote = get_pacote(db, pacote_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pacote, field, value)
    return pacote_repository.update(db, pacote)


def delete_pacote(db: Session, pacote_id: int) -> None:
    pacote = get_pacote(db, pacote_id)
    pacote_repository.delete(db, pacote)
