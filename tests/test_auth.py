from app.models.usuario import CargoUsuario


def test_login_sucesso(client, seed, usuario_factory):
    usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id)

    response = client.post("/api/v1/auth/login", json={"nm_usuario": "maria.silva", "senha": "senha123456"})

    assert response.status_code == 200
    assert response.json()["token"]


def test_login_senha_incorreta(client, seed, usuario_factory):
    usuario_factory("maria.silva", CargoUsuario.COORDENADOR, seed["subsetores"]["gerencia_fb"].id)

    response = client.post("/api/v1/auth/login", json={"nm_usuario": "maria.silva", "senha": "senha-errada"})

    assert response.status_code == 401


def test_rota_protegida_sem_token(client, seed):
    response = client.get("/api/v1/usuarios")

    assert response.status_code == 403


def test_rota_protegida_com_token_invalido(client, seed):
    response = client.get("/api/v1/usuarios", headers={"Authorization": "Bearer token-invalido"})

    assert response.status_code == 401
