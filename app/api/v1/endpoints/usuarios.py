from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database.session import get_db
from app.models.usuario import CargoUsuario, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioLogadoRead, UsuarioRead, UsuarioUpdate
from app.services import usuario_service

router = APIRouter()


@router.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(require_roles(CargoUsuario.COORDENADOR)),
) -> Usuario:
    return usuario_service.create_usuario(db, data, usuario_atual)


@router.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> list[Usuario]:
    return usuario_service.list_usuarios(db)


@router.get(
    "/usuarios/me",
    response_model=UsuarioLogadoRead,
    summary="Obtém o usuário logado",
    description="Consulta o usuário pelo id_usuario do JWT enviado no header Authorization: Bearer <token>.",
)
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
    usuario_atual: Usuario = Depends(require_roles(CargoUsuario.COORDENADOR)),
) -> Usuario:
    return usuario_service.update_usuario(db, usuario_id, data, usuario_atual)


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(require_roles(CargoUsuario.COORDENADOR)),
) -> None:
    usuario_service.delete_usuario(db, usuario_id, usuario_atual)
