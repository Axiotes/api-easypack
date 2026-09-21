from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.usuario import Usuario
from app.repositories import usuario_repository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


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


def list_usuarios(db: Session) -> list[Usuario]:
    return usuario_repository.list_all(db)


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    usuario = usuario_repository.get_by_id(db, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario


def update_usuario(db: Session, usuario_id: int, data: UsuarioUpdate) -> Usuario:
    usuario = get_usuario(db, usuario_id)
    changes = data.model_dump(exclude_unset=True)

    if "nm_usuario" in changes:
        existing = usuario_repository.get_by_nm_usuario(db, changes["nm_usuario"])
        if existing is not None and existing.id != usuario_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nome de usuário já cadastrado")

    if "senha" in changes:
        changes["senha"] = hash_password(changes["senha"])

    for field, value in changes.items():
        setattr(usuario, field, value)
    return usuario_repository.update(db, usuario)


def delete_usuario(db: Session, usuario_id: int) -> None:
    usuario_repository.delete(db, get_usuario(db, usuario_id))


def authenticate(db: Session, nm_usuario: str, senha: str) -> Usuario | None:
    usuario = usuario_repository.get_by_nm_usuario(db, nm_usuario)
    if usuario is None or not verify_password(senha, usuario.senha):
        return None
    return usuario
