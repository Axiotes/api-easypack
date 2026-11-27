from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.notificacao import Notificacao
from app.models.usuario import Usuario
from app.schemas.notificacao import NotificacaoCreate, NotificacaoRead
from app.services import notificacao_service

router = APIRouter()


@router.post("/notificacoes", response_model=NotificacaoRead, status_code=status.HTTP_201_CREATED)
def cadastrar_notificacao(
    data: NotificacaoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Notificacao:
    return notificacao_service.create_notificacao(db, data)
