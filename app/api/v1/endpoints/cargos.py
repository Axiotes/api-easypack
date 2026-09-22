from fastapi import APIRouter, Depends

from app.core.cargo import CARGO_HIERARQUIA
from app.core.deps import get_current_user
from app.models.usuario import Usuario

router = APIRouter()


@router.get("/cargos", response_model=list[str])
def listar_cargos(_: Usuario = Depends(get_current_user)) -> list[str]:
    return [cargo.value for cargo in CARGO_HIERARQUIA]
