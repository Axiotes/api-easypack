from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.services import usuario_service

router = APIRouter()


@router.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Usuario:
    return usuario_service.create_usuario(db, data)


@router.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> list[Usuario]:
    return usuario_service.list_usuarios(db)


@router.get("/usuarios/me", response_model=UsuarioRead)
def obter_usuario_logado(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return current_user


@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obter_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Usuario:
    return usuario_service.get_usuario(db, usuario_id)


@router.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Usuario:
    return usuario_service.update_usuario(db, usuario_id, data)


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> None:
    usuario_service.delete_usuario(db, usuario_id)
