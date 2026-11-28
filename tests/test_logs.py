from app.models.usuario import CargoUsuario


def test_logs_restrito_a_coordenador_e_gerente_projeto(client, seed, usuario_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)

    response = client.get("/api/v1/logs", headers=auth_headers("henrique.melo"))

    assert response.status_code == 403


def test_operacoes_registram_historico_que_sobrevive_a_exclusao(client, seed, usuario_factory, cliente_factory, auth_headers):
    henrique = usuario_factory("henrique.melo", CargoUsuario.PLENO, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    maria = usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["dev_soul_fb"].id, seed["produtos"]["Soul"].id)
    cliente_factory("Cliente A", seed["setores"]["FB"].id, henrique.id)

    correcao_id = client.post(
        "/api/v1/correcoes",
        json={
            "ticket": "SOUL-1",
            "id_cliente": 1,
            "id_produto": seed["produtos"]["Soul"].id,
            "id_usuario": henrique.id,
            "id_setor": seed["setores"]["FB"].id,
            "versao_correcao": "1.0.0",
        },
        headers=auth_headers("henrique.melo"),
    ).json()["id"]
    client.post(f"/api/v1/correcoes/{correcao_id}/aprovar", headers=auth_headers("henrique.melo"))
    client.delete(f"/api/v1/correcoes/{correcao_id}", headers=auth_headers("maria.silva"))

    response = client.get(f"/api/v1/logs?nm_entidade=Correcao&id_entidade={correcao_id}", headers=auth_headers("maria.silva"))

    assert response.status_code == 200
    acoes = [log["ds_acao"] for log in response.json()]
    assert acoes == ["EXCLUIR", "APROVAR_CODE_REVIEW", "CRIAR"]
    assert all(log["nm_usuario"] in {"henrique.melo", "maria.silva"} for log in response.json())
