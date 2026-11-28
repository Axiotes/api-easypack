from app.models.usuario import CargoUsuario


def _criar_correcao(client, headers, **overrides):
    payload = {
        "ticket": "SOUL-1",
        "id_cliente": 1,
        "id_produto": 1,
        "id_usuario": 1,
        "id_setor": 1,
        "versao_correcao": "1.0.0",
    }
    payload.update(overrides)
    return client.post("/api/v1/correcoes", json=payload, headers=headers)


def test_criar_correcao_exige_produto_compativel_com_responsavel(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique.id)
    headers = auth_headers("henrique.melo")

    response = _criar_correcao(client, headers, id_usuario=henrique.id, id_produto=seed["produtos"]["PEP"].id)

    assert response.status_code == 422


def test_criar_correcao_permite_soul_responsavel_por_pagu(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique.id)
    headers = auth_headers("henrique.melo")

    response = _criar_correcao(client, headers, id_usuario=henrique.id, id_produto=seed["produtos"]["Pagu"].id)

    assert response.status_code == 201


def test_aprovar_code_review_exige_cargo_de_desenvolvimento(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    diego = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, diego.id)
    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique.id).json()["id"]

    response_gp = client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("diego.lima"))
    assert response_gp.status_code == 403

    response_dev = client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    assert response_dev.status_code == 200
    assert response_dev.json()["sn_aprovado_code_review"] == "S"


def test_aprovar_code_review_exige_setor_fabrica(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique_fb = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    felipe_st = usuario_factory("felipe.rocha", CargoUsuario.ESPECIALISTA, seed["subsetores"]["dev_soul_st"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique_fb.id)
    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique_fb.id).json()["id"]

    response = client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("felipe.rocha"))

    assert response.status_code == 403


def test_alterar_mergeado_restrito_ao_mesmo_setor(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique_fb = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    felipe_st = usuario_factory("felipe.rocha", CargoUsuario.ESPECIALISTA, seed["subsetores"]["dev_soul_st"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique_fb.id)
    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique_fb.id, id_setor=seed["setores"]["FB"].id).json()["id"]

    response_outro_setor = client.post(
        f"/api/v1/correcoes/{correcao_id}/merge", json={"sn_mergeado": "S"}, headers=auth_headers("felipe.rocha")
    )
    assert response_outro_setor.status_code == 403

    response_mesmo_setor = client.post(
        f"/api/v1/correcoes/{correcao_id}/merge", json={"sn_mergeado": "N"}, headers=auth_headers("henrique.melo")
    )
    assert response_mesmo_setor.status_code == 200


def test_nao_pode_marcar_mergeado_sem_code_review_aprovado(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique.id)
    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique.id, id_setor=seed["setores"]["FB"].id).json()["id"]

    response = client.post(
        f"/api/v1/correcoes/{correcao_id}/merge", json={"sn_mergeado": "S"}, headers=auth_headers("henrique.melo")
    )

    assert response.status_code == 422

    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    response_apos_aprovacao = client.post(
        f"/api/v1/correcoes/{correcao_id}/merge", json={"sn_mergeado": "S"}, headers=auth_headers("henrique.melo")
    )
    assert response_apos_aprovacao.status_code == 200


def test_excluir_correcao_restrito_ao_mesmo_produto_do_coordenador(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    maria_soul = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id, seed["produtos"]["Soul"].id)
    lucas_pep = usuario_factory("lucas.barros", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id, seed["produtos"]["PEP"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique.id)
    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique.id).json()["id"]

    response_produto_errado = client.delete(f"/api/v1/correcoes/{correcao_id}", headers=auth_headers("lucas.barros"))
    assert response_produto_errado.status_code == 403

    response_produto_certo = client.delete(f"/api/v1/correcoes/{correcao_id}", headers=auth_headers("maria.silva"))
    assert response_produto_certo.status_code == 204
