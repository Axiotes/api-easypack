from pydantic import BaseModel, ConfigDict, Field


class CorrecaoCreate(BaseModel):
    ticket: str = Field(min_length=1, max_length=100)
    ticket_bug: str | None = Field(default=None, max_length=100)
    merge: str | None = Field(default=None, max_length=255)
    id_cliente: int
    id_produto: int
    id_usuario: int
    id_setor: int
    sn_mergeado: str | None = Field(default=None, pattern="^[SN]$")
    versao_correcao: str = Field(min_length=1, max_length=50)


class CorrecaoUpdate(BaseModel):
    ticket: str | None = Field(default=None, min_length=1, max_length=100)
    ticket_bug: str | None = Field(default=None, max_length=100)
    merge: str | None = Field(default=None, max_length=255)
    id_cliente: int | None = None
    id_produto: int | None = None
    id_usuario: int | None = None
    id_setor: int | None = None
    sn_mergeado: str | None = Field(default=None, pattern="^[SN]$")
    versao_correcao: str | None = Field(default=None, min_length=1, max_length=50)


class CorrecaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket: str
    ticket_bug: str | None
    merge: str | None
    id_cliente: int
    id_produto: int
    id_usuario: int
    id_setor: int
    sn_mergeado: str | None
    versao_correcao: str
    sn_aprovado_code_review: str
    id_usuario_aprovador: int | None
