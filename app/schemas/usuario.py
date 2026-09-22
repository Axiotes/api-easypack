from pydantic import BaseModel, ConfigDict, Field

from app.models.usuario import CargoUsuario


class UsuarioCreate(BaseModel):
    nm_usuario: str = Field(min_length=3, max_length=100)
    nm_completo: str = Field(min_length=3, max_length=255)
    senha: str = Field(min_length=6, max_length=100)
    cargo: CargoUsuario
    id_subsetor: int
    id_produto: int


class UsuarioUpdate(BaseModel):
    nm_usuario: str | None = Field(default=None, min_length=3, max_length=100)
    nm_completo: str | None = Field(default=None, min_length=3, max_length=255)
    senha: str | None = Field(default=None, min_length=6, max_length=100)
    cargo: CargoUsuario | None = None
    id_subsetor: int | None = None
    id_produto: int | None = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nm_usuario: str
    nm_completo: str
    cargo: CargoUsuario
    id_subsetor: int
    id_produto: int


class LoginRequest(BaseModel):
    nm_usuario: str = Field(min_length=3, max_length=100, examples=["maria.silva"])
    senha: str = Field(min_length=0, max_length=100, examples=["admin123"])


class Token(BaseModel):
    token: str
    message: str = "Login realizado com sucesso"
