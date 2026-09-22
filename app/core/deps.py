from collections.abc import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models.usuario import CargoUsuario, Usuario

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
        nm_usuario = payload.get("sub")
        cargo = payload.get("cargo")
        if not isinstance(nm_usuario, str) or not isinstance(cargo, str):
            raise credentials_exception
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc

    usuario = db.scalars(select(Usuario).where(Usuario.nm_usuario == nm_usuario)).first()
    if usuario is None or usuario.cargo.value != cargo:
        raise credentials_exception
    return usuario


def require_roles(*cargos: CargoUsuario) -> Callable[[Usuario], Usuario]:
    def dependency(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.cargo not in cargos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário sem permissão para executar esta ação",
            )
        return current_user

    return dependency
