from app.models.usuario import CargoUsuario


def test_apenas_gerente_projeto_gerencia_clientes(client, seed, usuario_factory, auth_headers):
    maria_coordenadora = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id)
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)

    payload = {"nm_cliente": "Cliente Novo", "id_setor_atendimento": seed["setores"]["FB"].id, "id_usuario": diego_gp.id}

    response_coordenador = client.post("/api/v1/clientes", json=payload, headers=auth_headers("maria.silva"))
    assert response_coordenador.status_code == 403

    response_gp = client.post("/api/v1/clientes", json=payload, headers=auth_headers("diego.lima"))
    assert response_gp.status_code == 201


def test_responsavel_do_cliente_deve_ser_gerente_projeto(client, seed, usuario_factory, auth_headers):
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    henrique_dev = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)

    response = client.post(
        "/api/v1/clientes",
        json={"nm_cliente": "Cliente Novo", "id_setor_atendimento": seed["setores"]["FB"].id, "id_usuario": henrique_dev.id},
        headers=auth_headers("diego.lima"),
    )

    assert response.status_code == 422


def test_exclusao_de_cliente_restrita_a_gerente_projeto(client, seed, usuario_factory, cliente_factory, auth_headers):
    diego_gp = usuario_factory("diego.lima", CargoUsuario.GERENTE_PROJETO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    maria_coordenadora = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id)
    cliente = cliente_factory("Cliente A", seed["setores"]["FB"].id, diego_gp.id)

    response_coordenador = client.delete(f"/api/v1/clientes/{cliente.id}", headers=auth_headers("maria.silva"))
    assert response_coordenador.status_code == 403

    response_gp = client.delete(f"/api/v1/clientes/{cliente.id}", headers=auth_headers("diego.lima"))
    assert response_gp.status_code == 204
