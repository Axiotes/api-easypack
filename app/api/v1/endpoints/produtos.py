from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.schemas.produto import ProdutoRead
from app.services import produto_service

router = APIRouter()


@router.get("/produtos", response_model=list[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db), _: Usuario = Depends(get_current_user)) -> list[Produto]:
    return produto_service.list_produtos(db)


@router.get("/produtos/{produto_id}", response_model=ProdutoRead)
def obter_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Produto:
    return produto_service.get_produto(db, produto_id)
