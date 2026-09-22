from pydantic import BaseModel, ConfigDict, Field


class PacoteCreate(BaseModel):
    id_correcao: int
    tp_pacote: int
    nm_pacote: str = Field(min_length=1, max_length=255)
    sn_aprovado_usu: str | None = Field(default=None, pattern="^[SN]$")


class PacoteUpdate(BaseModel):
    tp_pacote: int | None = None
    nm_pacote: str | None = Field(default=None, min_length=1, max_length=255)
    sn_aprovado_usu: str | None = Field(default=None, pattern="^[SN]$")


class PacoteAplicarRequest(BaseModel):
    id_usuario_aprovador_par: int | None = Field(
        default=None,
        description=(
            "Obrigatório quando quem aplica o pacote tem cargo Estagiário: "
            "outro usuário do mesmo subsetor, com cargo mínimo Pleno, que aprovou a aplicação."
        ),
    )


class PacoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_correcao: int
    tp_pacote: int
    nm_pacote: str
    sn_aplicado: str
    sn_aprovado_usu: str | None
    sn_aprovado_gerente: str
    id_usuario_aplicacao: int | None
    id_usuario_aprovador_gerente: int | None
    id_usuario_aprovador_par: int | None
