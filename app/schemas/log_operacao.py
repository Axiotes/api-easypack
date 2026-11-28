from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogOperacaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dt_operacao: datetime
    id_usuario: int
    nm_usuario: str
    nm_entidade: str
    id_entidade: int
    ds_acao: str
    ds_detalhe: str
