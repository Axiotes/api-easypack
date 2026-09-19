from pydantic import BaseModel, ConfigDict, Field


class ClienteCreate(BaseModel):
    nm_cliente: str = Field(min_length=1, max_length=255)
    id_setor_atendimento: int
    id_usuario: int


class ClienteUpdate(BaseModel):
    nm_cliente: str | None = Field(default=None, min_length=1, max_length=255)
    id_setor_atendimento: int | None = None
    id_usuario: int | None = None


class ClienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_cliente: str
    id_setor_atendimento: int
    id_usuario: int
