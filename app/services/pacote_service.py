from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.cargo import CARGOS_APROVADOR_PAR_ESTAGIARIO
from app.core.constantes import SG_SETOR_FABRICA, SG_SETOR_SERVICOS_TECNICOS
from app.core.produto import produto_atende
from app.models.pacote import Pacote
from app.models.usuario import CargoUsuario, Usuario
from app.repositories import correcao_repository, pacote_repository, tipo_pacote_repository, usuario_repository
from app.schemas.pacote import PacoteAplicarRequest, PacoteCreate, PacoteUpdate


def _validar_tipo_pacote(db: Session, id_correcao: int, tp_pacote: int) -> None:
    correcao = correcao_repository.get_by_id(db, id_correcao)
    if correcao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Correção não encontrada")
    tipo_pacote = tipo_pacote_repository.get_by_id(db, tp_pacote)
    if tipo_pacote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de pacote não encontrado")
    if tipo_pacote.nm_grupo != correcao.produto.nm_grupo_tipo_pacote:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Tipo de pacote '{tipo_pacote.nm_tipo}' não é válido para o produto {correcao.produto.nm_produto}",
        )


def create_pacote(db: Session, data: PacoteCreate) -> Pacote:
    _validar_tipo_pacote(db, data.id_correcao, data.tp_pacote)
    pacote = Pacote(**data.model_dump(), sn_aplicado="N", sn_aprovado_gerente="N")
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
    changes = data.model_dump(exclude_unset=True)

    if "tp_pacote" in changes:
        _validar_tipo_pacote(db, pacote.id_correcao, changes["tp_pacote"])

    for field, value in changes.items():
        setattr(pacote, field, value)
    return pacote_repository.update(db, pacote)


def delete_pacote(db: Session, pacote_id: int) -> None:
    pacote = get_pacote(db, pacote_id)
    pacote_repository.delete(db, pacote)


def aprovar_pacote_gerente(db: Session, pacote_id: int, usuario_atual: Usuario) -> Pacote:
    pacote = get_pacote(db, pacote_id)

    if pacote.correcao.sn_aprovado_code_review != "S":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O pacote só pode ser aprovado pelo Gerente de Projeto após a aprovação do code review da correção",
        )

    pacote.sn_aprovado_gerente = "S"
    pacote.id_usuario_aprovador_gerente = usuario_atual.id
    return pacote_repository.update(db, pacote)


def aplicar_pacote(db: Session, pacote_id: int, usuario_atual: Usuario, data: PacoteAplicarRequest) -> Pacote:
    pacote = get_pacote(db, pacote_id)

    if pacote.sn_aplicado == "S":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pacote já foi aplicado")
    if pacote.correcao.sn_aprovado_code_review != "S":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Pacote ainda não foi aprovado no code review da correção",
        )
    if pacote.sn_aprovado_gerente != "S":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Pacote ainda não foi aprovado pelo Gerente de Projeto",
        )

    if usuario_atual.cargo != CargoUsuario.GERENTE_PROJETO:
        nm_produto_correcao = pacote.correcao.produto.nm_produto
        nm_produto_usuario = usuario_atual.produto.nm_produto if usuario_atual.produto is not None else None
        if nm_produto_usuario is None or not produto_atende(nm_produto_usuario, nm_produto_correcao):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário não pode aplicar pacotes do produto {nm_produto_correcao}",
            )

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
        if aprovador.cargo not in CARGOS_APROVADOR_PAR_ESTAGIARIO:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O aprovador deve ter cargo Pleno, Senior, Especialista ou Coordenador",
            )
        pacote.id_usuario_aprovador_par = aprovador.id

    pacote.sn_aplicado = "S"
    pacote.id_usuario_aplicacao = usuario_atual.id
    return pacote_repository.update(db, pacote)
