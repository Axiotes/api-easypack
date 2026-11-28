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
    response = client.post("/api/v1/correcoes", json=payload, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()["id"]


def _criar_pacote(client, headers, id_correcao, tp_pacote=1, nm_pacote="pacote-teste"):
    return client.post(
        "/api/v1/pacotes", json={"id_correcao": id_correcao, "tp_pacote": tp_pacote, "nm_pacote": nm_pacote}, headers=headers
    )


def test_tipo_pacote_deve_bater_com_grupo_do_produto(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique.id)
    headers = auth_headers("henrique.melo")
    correcao_id = _criar_correcao(client, headers, id_usuario=henrique.id)

    response_errado = _criar_pacote(client, headers, correcao_id, tp_pacote=seed["tipos_pacote"]["Front"].id)
    assert response_errado.status_code == 422

    response_certo = _criar_pacote(client, headers, correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id)
    assert response_certo.status_code == 201


def test_aprovar_gerente_exige_code_review_aprovado(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    diego = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, diego.id)
    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique.id)
    pacote_id = _criar_pacote(client, auth_headers("henrique.melo"), correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id).json()["id"]

    response_sem_review = client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))
    assert response_sem_review.status_code == 422

    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    response_com_review = client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))
    assert response_com_review.status_code == 200


def test_aplicar_pacote_apenas_do_proprio_produto(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique_soul = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    gabriela_pep = usuario_factory("gabriela.alves", CargoUsuario.SENIOR, seed["subsetores"]["dev_pep_fb"].id, seed["produtos"]["PEP"].id)
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, diego_gp.id)

    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique_soul.id, id_produto=seed["produtos"]["Soul"].id)
    pacote_id = _criar_pacote(client, auth_headers("henrique.melo"), correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id).json()["id"]
    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))

    response_produto_errado = client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=auth_headers("gabriela.alves"))
    assert response_produto_errado.status_code == 403

    response_produto_certo = client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=auth_headers("henrique.melo"))
    assert response_produto_certo.status_code == 200


def test_gerente_projeto_aplica_pacote_sem_produto_definido(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, id_produto=None)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, diego_gp.id)

    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique.id)
    pacote_id = _criar_pacote(client, auth_headers("henrique.melo"), correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id).json()["id"]
    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))

    response = client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=auth_headers("diego.lima"))

    assert response.status_code == 200


def test_setor_st_nao_aplica_em_cliente_fb(client, seed, usuario_factory, cliente_factory, auth_headers):
    # Aprovar code review exige setor FB; por isso quem cria/aprova aqui é um dev FB,
    # e o usuário ST (mesmo produto, para passar a checagem de produto) tenta aplicar.
    henrique_fb = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    felipe_st = usuario_factory("felipe.rocha", CargoUsuario.ESPECIALISTA, seed["subsetores"]["dev_soul_st"].id, seed["produtos"]["Soul"].id)
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente FB", seed["setores"]["FB"].id, diego_gp.id)

    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique_fb.id)
    pacote_id = _criar_pacote(client, auth_headers("henrique.melo"), correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id).json()["id"]
    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))

    response = client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=auth_headers("felipe.rocha"))

    assert response.status_code == 403


def test_estagiario_precisa_de_aprovador_par_valido(client, seed, usuario_factory, cliente_factory, auth_headers):
    joao_estagiario = usuario_factory("joao.freitas", CargoUsuario.ESTAGIARIO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    rafael_pleno = usuario_factory("rafael.pires", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    isabela_junior = usuario_factory("isabela.nunes", CargoUsuario.JUNIOR, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    gabriela_outro_subsetor = usuario_factory(
        "gabriela.alves", CargoUsuario.SENIOR, seed["subsetores"]["dev_soul_st"].id, seed["produtos"]["Soul"].id
    )
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, diego_gp.id)

    correcao_id = _criar_correcao(client, auth_headers("joao.freitas"), id_usuario=joao_estagiario.id)
    pacote_id = _criar_pacote(client, auth_headers("joao.freitas"), correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id).json()["id"]
    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("rafael.pires"))
    client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))
    joao_headers = auth_headers("joao.freitas")

    sem_aprovador = client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=joao_headers)
    assert sem_aprovador.status_code == 422

    aprovador_eh_ele_mesmo = client.post(
        f"/api/v1/pacotes/{pacote_id}/aplicar", json={"id_usuario_aprovador_par": joao_estagiario.id}, headers=joao_headers
    )
    assert aprovador_eh_ele_mesmo.status_code == 422

    aprovador_outro_subsetor = client.post(
        f"/api/v1/pacotes/{pacote_id}/aplicar", json={"id_usuario_aprovador_par": gabriela_outro_subsetor.id}, headers=joao_headers
    )
    assert aprovador_outro_subsetor.status_code == 422

    aprovador_cargo_invalido = client.post(
        f"/api/v1/pacotes/{pacote_id}/aplicar", json={"id_usuario_aprovador_par": isabela_junior.id}, headers=joao_headers
    )
    assert aprovador_cargo_invalido.status_code == 422

    aprovador_gp_tambem_invalido = client.post(
        f"/api/v1/pacotes/{pacote_id}/aplicar", json={"id_usuario_aprovador_par": diego_gp.id}, headers=joao_headers
    )
    assert aprovador_gp_tambem_invalido.status_code == 422

    aprovador_valido = client.post(
        f"/api/v1/pacotes/{pacote_id}/aplicar", json={"id_usuario_aprovador_par": rafael_pleno.id}, headers=joao_headers
    )
    assert aprovador_valido.status_code == 200
    assert aprovador_valido.json()["id_usuario_aprovador_par"] == rafael_pleno.id


def test_pacote_ja_aplicado_nao_pode_ser_reaplicado(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, diego_gp.id)

    correcao_id = _criar_correcao(client, auth_headers("henrique.melo"), id_usuario=henrique.id)
    pacote_id = _criar_pacote(client, auth_headers("henrique.melo"), correcao_id, tp_pacote=seed["tipos_pacote"]["Forms"].id).json()["id"]
    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    client.post(f"/api/v1/pacotes/{pacote_id}/aprovar-gerente", headers=auth_headers("diego.lima"))
    client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=auth_headers("henrique.melo"))

    response = client.post(f"/api/v1/pacotes/{pacote_id}/aplicar", json={}, headers=auth_headers("henrique.melo"))

    assert response.status_code == 409
