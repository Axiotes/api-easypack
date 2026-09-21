from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database.session import get_db
from app.schemas.usuario import LoginRequest, Token
from app.services import usuario_service

router = APIRouter()


@router.post(
    "/auth/login",
    response_model=Token,
    summary="Realiza o login de um usuário",
    description="Recebe somente `nm_usuario` e `senha`. Em caso de sucesso, retorna um token JWT Bearer.",
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
) -> Token:
    usuario = usuario_service.authenticate(db, data.nm_usuario, data.senha)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(usuario.nm_usuario, usuario.cargo.value)
    return Token(token=token)
