from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.correcao import Correcao
from app.repositories import correcao_repository
from app.schemas.correcao import CorrecaoCreate, CorrecaoUpdate


def create_correcao(db: Session, data: CorrecaoCreate) -> Correcao:
    return correcao_repository.create(db, Correcao(**data.model_dump()))


def list_correcoes(db: Session) -> list[Correcao]:
    return correcao_repository.list_all(db)


def get_correcao(db: Session, correcao_id: int) -> Correcao:
    correcao = correcao_repository.get_by_id(db, correcao_id)
    if correcao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Correção não encontrada")
    return correcao


def update_correcao(db: Session, correcao_id: int, data: CorrecaoUpdate) -> Correcao:
    correcao = get_correcao(db, correcao_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(correcao, field, value)
    return correcao_repository.update(db, correcao)


def delete_correcao(db: Session, correcao_id: int) -> None:
    correcao_repository.delete(db, get_correcao(db, correcao_id))
