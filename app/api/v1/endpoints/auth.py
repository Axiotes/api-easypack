from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database.session import get_db
from app.schemas.usuario import Token
from app.services import usuario_service

router = APIRouter()


@router.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    usuario = usuario_service.authenticate(db, form_data.username, form_data.password)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=str(usuario.id))
    return Token(access_token=access_token)
