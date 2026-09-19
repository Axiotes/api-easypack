from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_roles
from app.database.session import get_db
from app.models.usuario import CargoUsuario, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.services import usuario_service

router = APIRouter()


@router.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_roles(CargoUsuario.COORDENADOR)),
) -> Usuario:
    return usuario_service.create_usuario(db, data)


@router.get("/usuarios/me", response_model=UsuarioRead)
def obter_usuario_logado(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return current_user
