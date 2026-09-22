from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.cargos import router as cargos_router
from app.api.v1.endpoints.clientes import router as clientes_router
from app.api.v1.endpoints.correcoes import router as correcoes_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.pacotes import router as pacotes_router
from app.api.v1.endpoints.produtos import router as produtos_router
from app.api.v1.endpoints.setores import router as setores_router
from app.api.v1.endpoints.subsetores import router as subsetores_router
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

router.include_router(
    setores_router,
    tags=["Setores"]
)

router.include_router(
    subsetores_router,
    tags=["Subsetores"]
)

router.include_router(
    produtos_router,
    tags=["Produtos"]
)

router.include_router(
    cargos_router,
    tags=["Cargos"]
)
