from pydantic import BaseModel, ConfigDict, Field

from app.models.usuario import CargoUsuario


class UsuarioCreate(BaseModel):
    nm_usuario: str = Field(min_length=3, max_length=100)
    nm_completo: str = Field(min_length=3, max_length=255)
    senha: str = Field(min_length=6, max_length=100)
    cargo: CargoUsuario
    id_subsetor: int
    id_produto: int


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_usuario: str
    nm_completo: str
    cargo: CargoUsuario
    id_subsetor: int
    id_produto: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
