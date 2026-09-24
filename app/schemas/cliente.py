from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Estado = Literal[
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]


class ClienteCreate(BaseModel):
    nm_cliente: str = Field(min_length=1, max_length=255)
    estado: Estado | None = None
    status_ambiente: Literal["PRE-PROD", "PRD"] = "PRE-PROD"
    id_setor_atendimento: int
    id_usuario: int


class ClienteUpdate(BaseModel):
    nm_cliente: str | None = Field(default=None, min_length=1, max_length=255)
    estado: Estado | None = None
    status_ambiente: Literal["PRE-PROD", "PRD"] = "PRE-PROD"
    id_setor_atendimento: int | None = None
    id_usuario: int | None = None


class ClienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_cliente: str
    estado: Estado | None
    status_ambiente: Literal["PRE-PROD", "PRD"]
    id_setor_atendimento: int
    id_usuario: int
