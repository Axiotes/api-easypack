from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.setor import Setor
from app.models.usuario import Usuario
from app.schemas.setor import SetorRead
from app.services import setor_service

router = APIRouter()


@router.get("/setores", response_model=list[SetorRead])
def listar_setores(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> list[Setor]:
    return setor_service.list_setores(db)


@router.get("/setores/{setor_id}", response_model=SetorRead)
def obter_setor(setor_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Setor:
    return setor_service.get_setor(db, setor_id)
