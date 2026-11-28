from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.core.opencl_utils import dispositivo_atual
from app.models.usuario import Usuario

router = APIRouter()


@router.get("/opencl/info")
def obter_info_opencl(_: Usuario = Depends(get_current_user)) -> dict:
    dispositivo = dispositivo_atual()
    return {
        "disponivel": dispositivo is not None,
        "dispositivo": dispositivo,
    }
