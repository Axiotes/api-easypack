from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.usuario import Usuario
from app.repositories import usuario_repository
from app.schemas.usuario import UsuarioCreate


def create_usuario(db: Session, data: UsuarioCreate) -> Usuario:
    if usuario_repository.get_by_nm_usuario(db, data.nm_usuario) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nome de usuário já cadastrado",
        )

    usuario = Usuario(
        nm_usuario=data.nm_usuario,
        nm_completo=data.nm_completo,
        senha=hash_password(data.senha),
        cargo=data.cargo,
        id_subsetor=data.id_subsetor,
        id_produto=data.id_produto,
    )
    return usuario_repository.create(db, usuario)


def authenticate(db: Session, nm_usuario: str, senha: str) -> Usuario | None:
    usuario = usuario_repository.get_by_nm_usuario(db, nm_usuario)
    if usuario is None or not verify_password(senha, usuario.senha):
        return None
    return usuario
