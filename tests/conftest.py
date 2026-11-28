import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  registra todas as entidades em Base.metadata
from app.core.security import hash_password
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.setor import Setor
from app.models.subsetor import Subsetor
from app.models.tipo_pacote import TipoPacote
from app.models.usuario import Usuario

SENHA_PADRAO = "senha123456"


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def seed(db_session):
    """Catálogo base: setores FB/ST, produtos (com grupo de tipo de pacote), tipos de pacote e subsetores."""
    fb = Setor(id=1, nm_setor="Fábrica", sg_setor="FB")
    st = Setor(id=2, nm_setor="Serviços Técnicos", sg_setor="ST")
    db_session.add_all([fb, st])

    soul = Produto(id=1, nm_produto="Soul", nm_grupo_tipo_pacote="FORMS_REPORTS")
    pep = Produto(id=2, nm_produto="PEP", nm_grupo_tipo_pacote="FRONT_BACK")
    pagu = Produto(id=3, nm_produto="Pagu", nm_grupo_tipo_pacote="FORMS_REPORTS")
    sacr = Produto(id=4, nm_produto="SACR", nm_grupo_tipo_pacote="FRONT_BACK")
    portaria = Produto(id=5, nm_produto="Portaria", nm_grupo_tipo_pacote="FRONT_BACK")
    db_session.add_all([soul, pep, pagu, sacr, portaria])

    forms = TipoPacote(id=1, nm_tipo="Forms", nm_grupo="FORMS_REPORTS")
    reports = TipoPacote(id=2, nm_tipo="Reports", nm_grupo="FORMS_REPORTS")
    front = TipoPacote(id=3, nm_tipo="Front", nm_grupo="FRONT_BACK")
    back = TipoPacote(id=4, nm_tipo="Back", nm_grupo="FRONT_BACK")
    db_session.add_all([forms, reports, front, back])

    dev_soul_fb = Subsetor(id=1, id_setor=1, nm_subsetor="Dev Soul FB", id_produto=1)
    dev_pep_fb = Subsetor(id=2, id_setor=1, nm_subsetor="Dev PEP FB", id_produto=2)
    dev_soul_st = Subsetor(id=3, id_setor=2, nm_subsetor="Dev Soul ST", id_produto=1)
    dev_pep_st = Subsetor(id=4, id_setor=2, nm_subsetor="Dev PEP ST", id_produto=2)
    gerencia_fb = Subsetor(id=5, id_setor=1, nm_subsetor="Gerencia FB", id_produto=None, sn_gerencia="S")
    gerencia_st = Subsetor(id=6, id_setor=2, nm_subsetor="Gerencia ST", id_produto=None, sn_gerencia="S")
    db_session.add_all([dev_soul_fb, dev_pep_fb, dev_soul_st, dev_pep_st, gerencia_fb, gerencia_st])

    db_session.commit()
    return {
        "setores": {"FB": fb, "ST": st},
        "produtos": {"Soul": soul, "PEP": pep, "Pagu": pagu, "SACR": sacr, "Portaria": portaria},
        "tipos_pacote": {"Forms": forms, "Reports": reports, "Front": front, "Back": back},
        "subsetores": {
            "dev_soul_fb": dev_soul_fb,
            "dev_pep_fb": dev_pep_fb,
            "dev_soul_st": dev_soul_st,
            "dev_pep_st": dev_pep_st,
            "gerencia_fb": gerencia_fb,
            "gerencia_st": gerencia_st,
        },
    }


@pytest.fixture()
def usuario_factory(db_session):
    def _criar(nm_usuario, cargo, id_subsetor, id_produto=None, nm_completo=None, senha=SENHA_PADRAO):
        usuario = Usuario(
            nm_usuario=nm_usuario,
            nm_completo=nm_completo or nm_usuario,
            senha=hash_password(senha),
            cargo=cargo,
            id_subsetor=id_subsetor,
            id_produto=id_produto,
        )
        db_session.add(usuario)
        db_session.commit()
        db_session.refresh(usuario)
        return usuario

    return _criar


@pytest.fixture()
def cliente_factory(db_session):
    def _criar(nm_cliente, id_setor_atendimento, id_usuario):
        cliente = Cliente(nm_cliente=nm_cliente, id_setor_atendimento=id_setor_atendimento, id_usuario=id_usuario)
        db_session.add(cliente)
        db_session.commit()
        db_session.refresh(cliente)
        return cliente

    return _criar


@pytest.fixture()
def login(client):
    def _login(nm_usuario, senha=SENHA_PADRAO):
        response = client.post("/api/v1/auth/login", json={"nm_usuario": nm_usuario, "senha": senha})
        assert response.status_code == 200, response.text
        return response.json()["token"]

    return _login


@pytest.fixture()
def auth_headers(login):
    def _headers(nm_usuario, senha=SENHA_PADRAO):
        return {"Authorization": f"Bearer {login(nm_usuario, senha)}"}

    return _headers
