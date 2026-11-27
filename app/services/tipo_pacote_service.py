from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.tipo_pacote import TipoPacote
from app.repositories import tipo_pacote_repository


def list_tipos_pacote(db: Session) -> list[TipoPacote]:
    return tipo_pacote_repository.list_all(db)


def get_tipo_pacote(db: Session, tipo_pacote_id: int) -> TipoPacote:
    tipo_pacote = tipo_pacote_repository.get_by_id(db, tipo_pacote_id)
    if tipo_pacote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de pacote não encontrado")
    return tipo_pacote
