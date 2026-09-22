from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.subsetor import Subsetor
from app.models.usuario import Usuario
from app.schemas.subsetor import SubsetorRead
from app.services import subsetor_service

router = APIRouter()


@router.get("/subsetores", response_model=list[SubsetorRead])
def listar_subsetores(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> list[Subsetor]:
    return subsetor_service.list_subsetores(db)


@router.get("/subsetores/{subsetor_id}", response_model=SubsetorRead)
def obter_subsetor(
    subsetor_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Subsetor:
    return subsetor_service.get_subsetor(db, subsetor_id)
