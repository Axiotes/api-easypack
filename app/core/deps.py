from collections.abc import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models.usuario import CargoUsuario, Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc

    usuario = db.get(Usuario, int(user_id))
    if usuario is None:
        raise credentials_exception
    return usuario


def require_roles(*roles: CargoUsuario) -> Callable[[Usuario], Usuario]:
    def dependency(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.cargo not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário sem permissão para executar esta ação",
            )
        return current_user

    return dependency
