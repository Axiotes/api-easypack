from pydantic import BaseModel, ConfigDict


class SetorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_setor: str
    sg_setor: str
