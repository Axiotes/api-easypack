from app.models.usuario import CargoUsuario


def test_opencl_info_endpoint_responde(client, seed, usuario_factory, auth_headers):
    usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id)

    response = client.get("/api/v1/opencl/info", headers=auth_headers("maria.silva"))

    assert response.status_code == 200
    body = response.json()
    assert "disponivel" in body
    assert "dispositivo" in body


def test_listagem_inclui_checksum_quando_opencl_disponivel(client, seed, usuario_factory, auth_headers):
    usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id)
    info = client.get("/api/v1/opencl/info", headers=auth_headers("maria.silva")).json()

    response = client.get("/api/v1/usuarios", headers=auth_headers("maria.silva"))

    assert response.status_code == 200
    if info["disponivel"]:
        assert "x-gpu-checksum" in {chave.lower() for chave in response.headers.keys()}
