from pydantic import BaseModel, ConfigDict


class TipoPacoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_tipo: str
    nm_grupo: str
