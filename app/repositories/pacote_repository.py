from sqlalchemy import Select, case, func, select
from sqlalchemy.orm import Session

from app.models.correcao import Correcao
from app.models.pacote import Pacote
from app.models.produto import Produto
from app.models.setor import Setor


def get_by_id(db: Session, pacote_id: int) -> Pacote | None:
    return db.get(Pacote, pacote_id)


def list_all(db: Session) -> list[Pacote]:
    return list(db.scalars(select(Pacote)).all())


def create(db: Session, pacote: Pacote) -> Pacote:
    db.add(pacote)
    db.commit()
    db.refresh(pacote)
    return pacote


def update(db: Session, pacote: Pacote) -> Pacote:
    db.commit()
    db.refresh(pacote)
    return pacote


def delete(db: Session, pacote: Pacote) -> None:
    db.delete(pacote)
    db.commit()


def _apply_filters(
    statement: Select,
    id_cliente: int,
    nm_pacote: str | None = None,
    id_produto: int | None = None,
    versao_correcao: str | None = None,
    sn_mergeado: str | None = None,
    sn_aprovado_gerente: str | None = None,
    ticket: str | None = None,
    ticket_bug: str | None = None,
    id_setor: int | None = None,
    sn_aplicado: str | None = None,
) -> Select:
    statement = statement.where(Correcao.id_cliente == id_cliente)
    for column, value in (
        (Pacote.nm_pacote, nm_pacote),
        (Correcao.versao_correcao, versao_correcao),
        (Correcao.ticket, ticket),
        (Correcao.ticket_bug, ticket_bug),
    ):
        if value is not None:
            statement = statement.where(column.icontains(value, autoescape=True))
    for column, value in (
        (Correcao.id_produto, id_produto),
        (Correcao.sn_mergeado, sn_mergeado),
        (Pacote.sn_aprovado_gerente, sn_aprovado_gerente),
        (Pacote.sn_aplicado, sn_aplicado),
        (Correcao.id_setor, id_setor),
    ):
        if value is not None:
            statement = statement.where(column == value)
    return statement


def count_by_cliente(
    db: Session,
    id_cliente: int,
    nm_pacote: str | None = None,
    id_produto: int | None = None,
    versao_correcao: str | None = None,
    sn_mergeado: str | None = None,
    sn_aprovado_gerente: str | None = None,
    ticket: str | None = None,
    ticket_bug: str | None = None,
    id_setor: int | None = None,
    sn_aplicado: str | None = None,
) -> dict[str, int]:
    statement = (
        select(
            func.count(Pacote.id).label("total_pacotes"),
            func.count(case((Pacote.sn_aplicado == "S", 1))).label("total_aplicados"),
            func.count(case((Pacote.sn_aplicado == "N", 1))).label("total_pendentes"),
        )
        .select_from(Pacote)
        .join(Correcao, Pacote.id_correcao == Correcao.id)
    )
    statement = _apply_filters(
        statement, id_cliente=id_cliente, nm_pacote=nm_pacote, id_produto=id_produto,
        versao_correcao=versao_correcao, sn_mergeado=sn_mergeado,
        sn_aprovado_gerente=sn_aprovado_gerente, ticket=ticket, ticket_bug=ticket_bug,
        id_setor=id_setor, sn_aplicado=sn_aplicado,
    )
    return dict(db.execute(statement).mappings().one())


def list_detailed_by_cliente(
    db: Session,
    id_cliente: int,
    nm_pacote: str | None = None,
    id_produto: int | None = None,
    versao_correcao: str | None = None,
    sn_mergeado: str | None = None,
    sn_aprovado_gerente: str | None = None,
    ticket: str | None = None,
    ticket_bug: str | None = None,
    id_setor: int | None = None,
    sn_aplicado: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[dict]:
    statement = (
        select(
            Pacote.id, Pacote.id_correcao, Pacote.nm_pacote,
            Correcao.versao_correcao, Correcao.id_produto, Produto.nm_produto,
            Correcao.id_setor, Setor.nm_setor, Setor.sg_setor,
            Correcao.ticket, Correcao.ticket_bug, Correcao.sn_mergeado,
            Pacote.sn_aprovado_gerente, Pacote.sn_aplicado,
        )
        .select_from(Pacote)
        .join(Correcao, Pacote.id_correcao == Correcao.id)
        .join(Produto, Correcao.id_produto == Produto.id)
        .join(Setor, Correcao.id_setor == Setor.id)
    )
    statement = _apply_filters(
        statement, id_cliente=id_cliente, nm_pacote=nm_pacote, id_produto=id_produto,
        versao_correcao=versao_correcao, sn_mergeado=sn_mergeado,
        sn_aprovado_gerente=sn_aprovado_gerente, ticket=ticket, ticket_bug=ticket_bug,
        id_setor=id_setor, sn_aplicado=sn_aplicado,
    )
    statement = statement.order_by(Pacote.id).offset(skip).limit(limit)
    return [dict(row) for row in db.execute(statement).mappings().all()]
