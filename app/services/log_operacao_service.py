from sqlalchemy.orm import Session

from app.models.log_operacao import LogOperacao
from app.repositories import log_operacao_repository


def list_logs(db: Session, nm_entidade: str | None = None, id_entidade: int | None = None) -> list[LogOperacao]:
    return log_operacao_repository.list_all(db, nm_entidade, id_entidade)
