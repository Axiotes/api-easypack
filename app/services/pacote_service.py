from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.cargo import cargo_pelo_menos
from app.core.constantes import SG_SETOR_FABRICA, SG_SETOR_SERVICOS_TECNICOS
from app.models.correcao import Correcao
from app.models.pacote import Pacote
from app.models.usuario import CargoUsuario, Usuario
from app.repositories import pacote_repository, produto_repository, usuario_repository
from app.schemas.pacote import (
    PacoteCompletoRead,
    PacoteAplicarRequest, PacoteContagemFiltros, PacoteContagemRead, PacoteCreate, PacoteUpdate,
    PacoteDetalhadoRead, PacoteListagemFiltros,
)
from app.services.cliente_service import get_cliente
from app.services.correcao_service import validar_acesso_produto


def create_pacote(db: Session, data: PacoteCreate, usuario_atual: Usuario) -> Pacote:
    get_cliente(db, data.id_cliente)
    produto = produto_repository.get_by_id(db, data.id_produto)
    if produto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    validar_acesso_produto(usuario_atual, produto)
    correcao = Correcao(
        ticket=data.ticket, ticket_bug=data.ticket_bug, merge=data.merge,
        id_cliente=data.id_cliente, id_produto=data.id_produto,
        id_usuario=usuario_atual.id, id_setor=usuario_atual.subsetor.id_setor,
        sn_mergeado=data.sn_mergeado, versao_correcao=data.versao_correcao,
        sn_aprovado_code_review="N",
    )
    pacote = Pacote(
        correcao=correcao, tp_pacote=data.tp_pacote, nm_pacote=data.nm_pacote,
        sn_aplicado="N", sn_aprovado_gerente="N", sn_aprovado_usu="N",
    )
    return pacote_repository.create(db, pacote)


def list_pacotes(db: Session) -> list[Pacote]:
    return pacote_repository.list_all(db)


def get_pacote(db: Session, pacote_id: int) -> Pacote:
    pacote = pacote_repository.get_by_id(db, pacote_id)
    if pacote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacote não encontrado")
    return pacote


def update_pacote(db: Session, pacote_id: int, data: PacoteUpdate) -> Pacote:
    pacote = get_pacote(db, pacote_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pacote, field, value)
    return pacote_repository.update(db, pacote)


def delete_pacote(db: Session, pacote_id: int) -> None:
    pacote = get_pacote(db, pacote_id)
    pacote_repository.delete(db, pacote)


def aprovar_pacote_gerente(db: Session, pacote_id: int, usuario_atual: Usuario) -> Pacote:
    if usuario_atual.cargo != CargoUsuario.GERENTE_PROJETO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Gerente de Projeto pode aprovar um pacote",
        )
    pacote = get_pacote(db, pacote_id)
    pacote.sn_aprovado_gerente = "S"
    pacote.id_usuario_aprovador_gerente = usuario_atual.id
    return pacote_repository.update(db, pacote)


def aplicar_pacote(db: Session, pacote_id: int, usuario_atual: Usuario, data: PacoteAplicarRequest) -> Pacote:
    pacote = get_pacote(db, pacote_id)

    if pacote.sn_aplicado == "S":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pacote já foi aplicado")
    if pacote.sn_aprovado_gerente != "S":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Pacote ainda não foi aprovado pelo Gerente de Projeto",
        )

    validar_acesso_produto(usuario_atual, pacote.correcao.produto)

    cliente = pacote.correcao.cliente
    sg_setor_usuario = usuario_atual.subsetor.setor.sg_setor
    sg_setor_cliente = cliente.setor_atendimento.sg_setor
    if sg_setor_usuario == SG_SETOR_SERVICOS_TECNICOS and sg_setor_cliente == SG_SETOR_FABRICA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário do setor ST não pode aplicar pacote em cliente atendido pelo setor FB",
        )

    if usuario_atual.cargo == CargoUsuario.ESTAGIARIO:
        if data.id_usuario_aprovador_par is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "Usuário estagiário precisa da aprovação de outro usuário do mesmo "
                    "subsetor, com cargo mínimo Pleno, para aplicar o pacote"
                ),
            )
        aprovador = usuario_repository.get_by_id(db, data.id_usuario_aprovador_par)
        if aprovador is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário aprovador não encontrado")
        if aprovador.id == usuario_atual.id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O aprovador deve ser outro usuário, diferente de quem está aplicando o pacote",
            )
        if aprovador.id_subsetor != usuario_atual.id_subsetor:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O aprovador deve ser do mesmo subsetor do usuário estagiário",
            )
        if not cargo_pelo_menos(aprovador.cargo, CargoUsuario.PLENO):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O aprovador deve ter cargo mínimo Pleno",
            )
        pacote.id_usuario_aprovador_par = aprovador.id

    pacote.sn_aplicado = "S"
    pacote.id_usuario_aplicacao = usuario_atual.id
    return pacote_repository.update(db, pacote)


def count_pacotes(db: Session, filtros: PacoteContagemFiltros) -> PacoteContagemRead:
    get_cliente(db, filtros.id_cliente)
    return PacoteContagemRead(**pacote_repository.count_by_cliente(db, **filtros.model_dump()))


def list_pacotes_detalhados(db: Session, filtros: PacoteListagemFiltros) -> list[PacoteDetalhadoRead]:
    get_cliente(db, filtros.id_cliente)
    return [
        PacoteDetalhadoRead(**row)
        for row in pacote_repository.list_detailed_by_cliente(db, **filtros.model_dump())
    ]


def get_pacote_completo(db: Session, pacote_id: int) -> PacoteCompletoRead:
    pacote = pacote_repository.get_complete_by_id(db, pacote_id)
    if pacote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacote não encontrado")
    return PacoteCompletoRead(**pacote)
