import importlib
import os

import pytest

from controle_ativos.models.ativos import Ativo
from controle_ativos.utils.security import CSRF_SESSION_KEY


os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-routes")
app_module = importlib.import_module("controle_ativos.web.app")


@pytest.fixture()
def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def _csrf_headers(client, token_override=None):
    client.get("/")
    with client.session_transaction() as sess:
        token = token_override if token_override is not None else sess[CSRF_SESSION_KEY]
    return {"X-CSRF-Token": token}


def _login(client, user_id=1, perfil="USUARIO", ativo=True):
    """Cria uma sessão autenticada sem depender do banco de dados."""
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["email"] = "tester@example.com"
        sess["perfil"] = perfil
        sess["ativo"] = ativo


def _ativo(id_ativo="AT-001", criado_por=1):
    return Ativo(
        id_ativo=id_ativo,
        tipo="Notebook",
        marca="Dell",
        modelo="Latitude",
        usuario_responsavel="Joao Silva",
        departamento="TI",
        status="Disponível",
        data_entrada="2026-05-27",
        data_saida=None,
        criado_por=criado_por,
    )


def test_dashboard_exige_sessao(client):
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_dashboard_autenticado_renderiza_pagina(client):
    _login(client)

    response = client.get("/dashboard")

    assert response.status_code == 200


def test_register_rejeita_payload_sem_email(client):
    response = client.post(
        "/register",
        json={"senha": "Senha@12345"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 400
    assert response.get_json()["ok"] is False
    assert "email" in response.get_json()["erro"]


def test_register_caminho_sucesso_delega_para_auth_service(client, monkeypatch):
    captured = {}

    def _fake_registrar_usuario(email, senha, pergunta, resposta):
        captured.update(
            {
                "email": email,
                "senha": senha,
                "pergunta": pergunta,
                "resposta": resposta,
            }
        )
        return 33

    monkeypatch.setattr(app_module.auth_service, "registrar_usuario", _fake_registrar_usuario)

    response = client.post(
        "/register",
        json={
            "email": "tester@example.com",
            "senha": "Senha@12345",
            "pergunta_recuperacao": "Cor?",
            "resposta_recuperacao": "Azul",
        },
        headers=_csrf_headers(client),
    )

    assert response.status_code == 201
    assert response.get_json() == {"ok": True, "user_id": 33}
    assert captured["email"] == "tester@example.com"


def test_login_rejeita_payload_sem_senha(client):
    response = client.post(
        "/login",
        json={"email": "tester@example.com"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 400
    assert response.get_json()["ok"] is False
    assert "senha" in response.get_json()["erro"]


def test_login_caminho_sucesso_grava_sessao(client, monkeypatch):
    class _UsuarioFake:
        id = 9
        email = "tester@example.com"

    monkeypatch.setattr(app_module.auth_service, "autenticar", lambda **kwargs: _UsuarioFake())

    response = client.post(
        "/login",
        json={"email": "tester@example.com", "senha": "Senha@12345"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200
    assert response.get_json() == {"ok": True, "email": "tester@example.com"}
    with client.session_transaction() as sess:
        assert sess["user_id"] == 9
        assert sess["email"] == "tester@example.com"
        assert sess["perfil"] == "USUARIO"
        assert sess["ativo"] is True


def test_forgot_password_rejeita_payload_incompleto(client):
    response = client.post(
        "/forgot-password",
        json={"email": "tester@example.com", "resposta_recuperacao": "azul"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 400
    assert response.get_json()["ok"] is False
    assert "nova_senha" in response.get_json()["erro"]


def test_forgot_password_caminho_sucesso_delega_para_auth_service(client, monkeypatch):
    captured = {}

    def _fake_redefinir_senha(email, resposta, nova_senha):
        captured.update({"email": email, "resposta": resposta, "nova_senha": nova_senha})

    monkeypatch.setattr(app_module.auth_service, "redefinir_senha", _fake_redefinir_senha)

    response = client.post(
        "/forgot-password",
        json={
            "email": "tester@example.com",
            "resposta_recuperacao": "Azul",
            "nova_senha": "Senha@12345",
        },
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200
    assert response.get_json() == {"ok": True}
    assert captured == {
        "email": "tester@example.com",
        "resposta": "Azul",
        "nova_senha": "Senha@12345",
    }


@pytest.mark.parametrize(
    "method,path",
    [
        ("get", "/ativos"),
        ("post", "/ativos"),
        ("get", "/ativos/AT-001"),
        ("put", "/ativos/AT-001"),
        ("delete", "/ativos/AT-001"),
    ],
)
def test_rotas_de_ativos_exigem_usuario_autenticado(client, method, path):
    if method == "get":
        response = getattr(client, method)(path, json={})
        assert response.status_code == 401
        assert response.get_json() == {"ok": False, "erro": "Não autenticado."}
    else:
        response = getattr(client, method)(path, json={})
        assert response.status_code == 400
        assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


def test_rotas_mutaveis_sem_token_rejeitam_csrf(client):
    response = client.post("/register", json={"email": "a@b.com"})
    assert response.status_code == 400
    assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


def test_rotas_mutaveis_com_token_invalido_rejeitam_csrf(client):
    response = client.post(
        "/login",
        json={"email": "tester@example.com", "senha": "Senha@12345"},
        headers=_csrf_headers(client, token_override="invalido"),
    )
    assert response.status_code == 400
    assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


def test_criar_ativo_rejeita_campo_obrigatorio_ausente(client):
    _login(client)

    response = client.post(
        "/ativos",
        json={
            "marca": "Dell",
            "modelo": "Latitude",
            "usuario_responsavel": "Joao Silva",
            "departamento": "TI",
            "status": "Disponível",
            "data_entrada": "2026-05-27",
        },
        headers=_csrf_headers(client),
    )

    assert response.status_code == 400
    assert response.get_json()["ok"] is False
    assert "tipo" in response.get_json()["erro"]


def test_listar_ativos_caminho_sucesso_serializa_ativos(client, monkeypatch):
    _login(client)
    monkeypatch.setattr(app_module.ativos_service, "listar_ativos", lambda user_id: [_ativo()])

    response = client.get("/ativos")

    assert response.status_code == 200
    assert response.get_json()["ativos"][0] == {
        "id": "AT-001",
        "tipo": "Notebook",
        "marca": "Dell",
        "modelo": "Latitude",
        "usuario_responsavel": "Joao Silva",
        "departamento": "TI",
        "status": "Disponível",
        "data_entrada": "2026-05-27",
        "data_saida": None,
        "criado_por": 1,
    }


def test_criar_ativo_caminho_sucesso_delega_para_service(client, monkeypatch):
    _login(client, user_id=7)
    captured = {}

    def _fake_criar_ativo(ativo, user_id):
        captured["ativo"] = ativo
        captured["user_id"] = user_id

    monkeypatch.setattr(app_module, "_gerar_id_ativo", lambda: "AT-GERADO")
    monkeypatch.setattr(app_module.ativos_service, "criar_ativo", _fake_criar_ativo)

    response = client.post(
        "/ativos",
        json={
            "tipo": "Notebook",
            "marca": "Dell",
            "modelo": "Latitude",
            "usuario_responsavel": "Joao Silva",
            "departamento": "TI",
            "status": "Disponível",
            "data_entrada": "2026-05-27",
        },
        headers=_csrf_headers(client),
    )

    assert response.status_code == 201
    assert response.get_json() == {"ok": True}
    assert captured["user_id"] == 7
    assert captured["ativo"].id_ativo == "AT-GERADO"
    assert captured["ativo"].criado_por == 7


def test_buscar_ativo_caminho_sucesso_serializa_ativo(client, monkeypatch):
    _login(client)
    monkeypatch.setattr(app_module.ativos_service, "buscar_ativo", lambda **kwargs: _ativo())

    response = client.get("/ativos/AT-001")

    assert response.status_code == 200
    assert response.get_json()["ativo"]["id"] == "AT-001"


def test_atualizar_ativo_caminho_sucesso_serializa_ativo(client, monkeypatch):
    _login(client)
    monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", lambda **kwargs: _ativo())

    response = client.put(
        "/ativos/AT-001",
        json={"modelo": "XPS"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200
    assert response.get_json()["ativo"]["id"] == "AT-001"


def test_atualizar_ativo_traduz_erro_do_servico(client, monkeypatch):
    _login(client)

    def _fake_atualizar_ativo(*args, **kwargs):
        raise app_module.AtivoErro("Status inválido para atualização.")

    monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", _fake_atualizar_ativo)

    response = client.put(
        "/ativos/AT-001",
        json={"status": "Inexistente"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "ok": False,
        "erro": "Status inválido para atualização.",
    }


def test_buscar_ativo_nao_encontrado_retorna_404(client, monkeypatch):
    _login(client)

    def _fake_buscar_ativo(*args, **kwargs):
        raise app_module.AtivoNaoEncontrado("Ativo não encontrado.")

    monkeypatch.setattr(app_module.ativos_service, "buscar_ativo", _fake_buscar_ativo)

    response = client.get("/ativos/AT-404")

    assert response.status_code == 404
    assert response.get_json() == {"ok": False, "erro": "Ativo não encontrado."}


def test_remover_ativo_traduz_erro_do_servico(client, monkeypatch):
    _login(client, perfil="ADMIN")

    def _fake_remover_ativo(*args, **kwargs):
        raise app_module.AtivoErro("Não foi possível remover o ativo.")

    monkeypatch.setattr(app_module.ativos_service, "remover_ativo", _fake_remover_ativo)

    response = client.delete(
        "/ativos/AT-001",
        headers=_csrf_headers(client),
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "ok": False,
        "erro": "Não foi possível remover o ativo.",
    }


def test_remover_ativo_caminho_sucesso_delega_para_service(client, monkeypatch):
    _login(client, user_id=7, perfil="ADMIN")
    captured = {}

    def _fake_remover_ativo(id_ativo, user_id):
        captured["id_ativo"] = id_ativo
        captured["user_id"] = user_id

    monkeypatch.setattr(app_module.ativos_service, "remover_ativo", _fake_remover_ativo)

    response = client.delete(
        "/ativos/AT-001",
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200
    assert response.get_json() == {"ok": True}
    assert captured == {"id_ativo": "AT-001", "user_id": 7}
