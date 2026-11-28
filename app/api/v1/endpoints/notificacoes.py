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
) -> Notificacao:
    return notificacao_service.create_notificacao(db, data)


@router.get("/notificacoes/pendentes/{usuario_id}", response_model=list[NotificacaoRead])
def listar_notificacoes_pendentes(
    usuario_id: int,
    db: Session = Depends(get_db),
) -> list[Notificacao]:
    return notificacao_service.list_notificacoes_pendentes(db, usuario_id)


@router.patch("/notificacoes/{notificacao_id}/lida", response_model=NotificacaoRead)
def marcar_notificacao_como_lida(
    notificacao_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user),
) -> Notificacao:
    return notificacao_service.marcar_como_lida(db, notificacao_id, usuario_atual)
