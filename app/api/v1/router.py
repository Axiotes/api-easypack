from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.clientes import router as clientes_router
from app.api.v1.endpoints.correcoes import router as correcoes_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.pacotes import router as pacotes_router
from app.api.v1.endpoints.usuarios import router as usuarios_router

router = APIRouter()

router.include_router(
    health_router,
    tags=["Health"]
)

router.include_router(
    auth_router,
    tags=["Autenticação"]
)

router.include_router(
    usuarios_router,
    tags=["Usuários"]
)

router.include_router(
    clientes_router,
    tags=["Clientes"]
)

router.include_router(
    correcoes_router,
    tags=["Correções"]
)

router.include_router(
    pacotes_router,
    tags=["Pacotes"]
)
