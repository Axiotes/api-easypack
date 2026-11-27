from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.tipo_pacote import TipoPacote
from app.models.usuario import Usuario
from app.schemas.tipo_pacote import TipoPacoteRead
from app.services import tipo_pacote_service

router = APIRouter()


@router.get("/tipos-pacote", response_model=list[TipoPacoteRead])
def listar_tipos_pacote(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> list[TipoPacote]:
    return tipo_pacote_service.list_tipos_pacote(db)


@router.get("/tipos-pacote/{tipo_pacote_id}", response_model=TipoPacoteRead)
def obter_tipo_pacote(
    tipo_pacote_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> TipoPacote:
    return tipo_pacote_service.get_tipo_pacote(db, tipo_pacote_id)
