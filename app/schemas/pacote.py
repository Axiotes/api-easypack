from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PacoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tp_pacote: int
    nm_pacote: str = Field(min_length=1, max_length=255)
    id_cliente: int = Field(gt=0)
    id_produto: int = Field(gt=0)
    ticket: str = Field(min_length=1, max_length=100)
    versao_correcao: str = Field(min_length=1, max_length=50)
    ticket_bug: str | None = Field(default=None, max_length=100)
    merge: str | None = Field(default=None, max_length=255)
    sn_mergeado: Literal["S", "N"] = "N"
    sn_aplicado: Literal["N"] = "N"
    sn_aprovado_gerente: Literal["N"] = "N"
    sn_aprovado_usu: Literal["N"] = "N"
    sn_aprovado_code_review: Literal["N"] = "N"


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


class PacoteContagemFiltros(BaseModel):
    id_cliente: int = Field(gt=0)
    nm_pacote: str | None = Field(default=None, min_length=1, max_length=255)
    id_produto: int | None = Field(default=None, gt=0)
    versao_correcao: str | None = Field(default=None, min_length=1, max_length=50)
    sn_mergeado: Literal["S", "N"] | None = None
    sn_aplicado: Literal["S", "N"] | None = None
    sn_aprovado_gerente: Literal["S", "N"] | None = None
    ticket: str | None = Field(default=None, max_length=100)
    ticket_bug: str | None = Field(default=None, max_length=100)
    id_setor: int | None = Field(default=None, gt=0, description="Setor da correção")


class PacoteContagemRead(BaseModel):
    total_pacotes: int
    total_aplicados: int
    total_pendentes: int


class PacoteListagemFiltros(PacoteContagemFiltros):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1)


class PacoteDetalhadoRead(BaseModel):
    id: int
    id_correcao: int
    nm_pacote: str
    versao_correcao: str
    id_produto: int
    nm_produto: str
    id_setor: int
    nm_setor: str
    sg_setor: str
    ticket: str
    ticket_bug: str | None
    sn_mergeado: str | None
    sn_aprovado_gerente: str
    sn_aplicado: str


class PacoteCompletoRead(BaseModel):
    id: int
    id_correcao: int
    tp_pacote: int
    nm_pacote: str
    sn_aplicado: str
    sn_aprovado_usu: str | None
    sn_aprovado_gerente: str
    id_usuario_aplicacao: str | None = Field(description="Nome completo do usuário que aplicou o pacote")
    id_usuario_aprovador_gerente: str | None = Field(description="Nome completo do gerente aprovador")
    id_usuario_aprovador_par: str | None = Field(description="Nome completo do aprovador par")
    ticket: str
    ticket_bug: str | None
    merge: str | None
    id_cliente: str = Field(description="Nome do cliente da correção")
    id_produto: str = Field(description="Nome do produto da correção")
    id_usuario: str = Field(description="Nome completo do usuário da correção")
    id_setor: str = Field(description="Nome do setor da correção")
    sn_mergeado: str | None
    versao_correcao: str
    sn_aprovado_code_review: str
    id_usuario_aprovador: str | None = Field(description="Nome completo do aprovador da correção")
