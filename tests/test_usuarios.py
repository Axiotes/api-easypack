from app.models.usuario import CargoUsuario


def test_coordenador_gerencia_apenas_proprio_subsetor(client, seed, usuario_factory, auth_headers):
    maria = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    headers = auth_headers("maria.silva")

    response_outro_subsetor = client.post(
        "/api/v1/usuarios",
        json={
            "nm_usuario": "novo.dev",
            "nm_completo": "Novo Dev",
            "senha": "senha123456",
            "cargo": "PLENO",
            "id_subsetor": seed["subsetores"]["dev_pep_fb"].id,
            "id_produto": seed["produtos"]["PEP"].id,
        },
        headers=headers,
    )
    assert response_outro_subsetor.status_code == 403

    response_proprio_subsetor = client.post(
        "/api/v1/usuarios",
        json={
            "nm_usuario": "novo.dev",
            "nm_completo": "Novo Dev",
            "senha": "senha123456",
            "cargo": "PLENO",
            "id_subsetor": seed["subsetores"]["dev_soul_fb"].id,
            "id_produto": seed["produtos"]["Soul"].id,
        },
        headers=headers,
    )
    assert response_proprio_subsetor.status_code == 201


def test_coordenador_nao_gerencia_cargo_igual_ou_superior(client, seed, usuario_factory, auth_headers):
    maria = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    headers = auth_headers("maria.silva")

    response = client.post(
        "/api/v1/usuarios",
        json={
            "nm_usuario": "outro.coordenador",
            "nm_completo": "Outro Coordenador",
            "senha": "senha123456",
            "cargo": "COORDENADOR",
            "id_subsetor": seed["subsetores"]["dev_soul_fb"].id,
            "id_produto": seed["produtos"]["Soul"].id,
        },
        headers=headers,
    )

    assert response.status_code == 403


def test_produto_obrigatorio_exceto_para_gerente_projeto(client, seed, usuario_factory, auth_headers):
    maria = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    headers = auth_headers("maria.silva")

    response_sem_produto = client.post(
        "/api/v1/usuarios",
        json={
            "nm_usuario": "novo.dev",
            "nm_completo": "Novo Dev",
            "senha": "senha123456",
            "cargo": "PLENO",
            "id_subsetor": seed["subsetores"]["dev_soul_fb"].id,
        },
        headers=headers,
    )
    assert response_sem_produto.status_code == 422


def test_listagem_de_usuarios_restrita_ao_subsetor_do_coordenador(client, seed, usuario_factory, auth_headers):
    maria = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    isabela = usuario_factory("isabela.nunes", CargoUsuario.JUNIOR, seed["subsetores"]["dev_pep_fb"].id, seed["produtos"]["PEP"].id)

    response = client.get("/api/v1/usuarios", headers=auth_headers("maria.silva"))

    assert response.status_code == 200
    nomes = {usuario["nm_usuario"] for usuario in response.json()}
    assert nomes == {"maria.silva", "henrique.melo"}


def test_listagem_de_usuarios_nao_e_restrita_para_outros_cargos(client, seed, usuario_factory, auth_headers):
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    usuario_factory("isabela.nunes", CargoUsuario.JUNIOR, seed["subsetores"]["dev_pep_fb"].id, seed["produtos"]["PEP"].id)

    response = client.get("/api/v1/usuarios", headers=auth_headers("diego.lima"))

    assert response.status_code == 200
    assert len(response.json()) == 2
