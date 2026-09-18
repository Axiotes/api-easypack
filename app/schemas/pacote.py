from pydantic import BaseModel, ConfigDict, Field


class PacoteCreate(BaseModel):
    id_correcao: int
    tp_pacote: int
    nm_pacote: str = Field(min_length=1, max_length=255)
    sn_aplicado: str = Field(default="N", pattern="^[SN]$")
    sn_aprovado_usu: str | None = Field(default=None, pattern="^[SN]$")
    sn_aprovado_gerente: str = Field(default="N", pattern="^[SN]$")


class PacoteUpdate(BaseModel):
    tp_pacote: int | None = None
    nm_pacote: str | None = Field(default=None, min_length=1, max_length=255)
    sn_aplicado: str | None = Field(default=None, pattern="^[SN]$")
    sn_aprovado_usu: str | None = Field(default=None, pattern="^[SN]$")
    sn_aprovado_gerente: str | None = Field(default=None, pattern="^[SN]$")


class PacoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_correcao: int
    tp_pacote: int
    nm_pacote: str
    sn_aplicado: str
    sn_aprovado_usu: str | None
    sn_aprovado_gerente: str
