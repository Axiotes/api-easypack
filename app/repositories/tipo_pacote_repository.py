from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tipo_pacote import TipoPacote


def get_by_id(db: Session, tipo_pacote_id: int) -> TipoPacote | None:
    return db.get(TipoPacote, tipo_pacote_id)


def list_all(db: Session) -> list[TipoPacote]:
    return list(db.scalars(select(TipoPacote)).all())
