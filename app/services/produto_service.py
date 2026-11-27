from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.repositories import produto_repository


def list_produtos(db: Session) -> list[Produto]:
    return produto_repository.list_all(db)


def get_produto(db: Session, produto_id: int) -> Produto:
    produto = produto_repository.get_by_id(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto
