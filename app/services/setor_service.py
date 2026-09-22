from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.setor import Setor
from app.repositories import setor_repository


def list_setores(db: Session) -> list[Setor]:
    return setor_repository.list_all(db)


def get_setor(db: Session, setor_id: int) -> Setor:
    setor = setor_repository.get_by_id(db, setor_id)
    if setor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setor não encontrado")
    return setor
