from pydantic import BaseModel, ConfigDict


class ProdutoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_produto: str
