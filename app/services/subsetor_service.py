from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.subsetor import Subsetor
from app.repositories import subsetor_repository


def list_subsetores(db: Session) -> list[Subsetor]:
    return subsetor_repository.list_all(db)


def get_subsetor(db: Session, subsetor_id: int) -> Subsetor:
    subsetor = subsetor_repository.get_by_id(db, subsetor_id)
    if subsetor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subsetor não encontrado")
    return subsetor
