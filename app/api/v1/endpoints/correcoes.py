from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.correcao import Correcao
from app.models.usuario import Usuario
from app.schemas.correcao import CorrecaoCreate, CorrecaoRead, CorrecaoUpdate
from app.services import correcao_service

router = APIRouter()


@router.post("/correcoes", response_model=CorrecaoRead, status_code=status.HTTP_201_CREATED)
def cadastrar_correcao(data: CorrecaoCreate, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Correcao:
    return correcao_service.create_correcao(db, data)


@router.get("/correcoes", response_model=list[CorrecaoRead])
def listar_correcoes(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> list[Correcao]:
    return correcao_service.list_correcoes(db)


@router.get("/correcoes/{correcao_id}", response_model=CorrecaoRead)
def obter_correcao(correcao_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Correcao:
    return correcao_service.get_correcao(db, correcao_id)


@router.put("/correcoes/{correcao_id}", response_model=CorrecaoRead)
def atualizar_correcao(correcao_id: int, data: CorrecaoUpdate, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> Correcao:
    return correcao_service.update_correcao(db, correcao_id, data)


@router.delete("/correcoes/{correcao_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_correcao(correcao_id: int, db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> None:
    correcao_service.delete_correcao(db, correcao_id)
