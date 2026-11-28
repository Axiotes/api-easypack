from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.log_operacao import LogOperacao


def create(db: Session, log: LogOperacao) -> LogOperacao:
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_all(db: Session, nm_entidade: str | None = None, id_entidade: int | None = None) -> list[LogOperacao]:
    stmt = select(LogOperacao).order_by(LogOperacao.dt_operacao.desc(), LogOperacao.id.desc())
    if nm_entidade is not None:
        stmt = stmt.where(LogOperacao.nm_entidade == nm_entidade)
    if id_entidade is not None:
        stmt = stmt.where(LogOperacao.id_entidade == id_entidade)
    return list(db.scalars(stmt).all())
