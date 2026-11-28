from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.database.session import get_db
from app.models.log_operacao import LogOperacao
from app.models.usuario import CargoUsuario, Usuario
from app.schemas.log_operacao import LogOperacaoRead
from app.services import log_operacao_service

router = APIRouter()


@router.get("/logs", response_model=list[LogOperacaoRead])
def listar_logs(
    nm_entidade: str | None = None,
    id_entidade: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(CargoUsuario.COORDENADOR, CargoUsuario.GERENTE_PROJETO)),
) -> list[LogOperacao]:
    return log_operacao_service.list_logs(db, nm_entidade, id_entidade)
