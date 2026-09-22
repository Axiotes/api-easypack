from pydantic import BaseModel, ConfigDict


class SubsetorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_setor: int
    nm_subsetor: str
    id_produto: int | None
    sn_gerencia: str
