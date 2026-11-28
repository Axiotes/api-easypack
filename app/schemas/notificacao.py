from pydantic import BaseModel, ConfigDict


class NotificacaoCreate(BaseModel):
    id_usuario: int


class NotificacaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_usuario: int
    lido: bool
