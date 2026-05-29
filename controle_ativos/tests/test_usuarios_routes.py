import importlib
import os

import pytest

from controle_ativos.models.usuario import Usuario
from controle_ativos.utils.security import CSRF_SESSION_KEY


os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-users")
app_module = importlib.import_module("controle_ativos.web.app")


@pytest.fixture()
def app_client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def _csrf_headers(app_client, token_override=None):
    app_client.get("/")
    with app_client.session_transaction() as sess:
        token = token_override if token_override is not None else sess[CSRF_SESSION_KEY]
    return {"X-CSRF-Token": token}


def _login(app_client, user_id=1, perfil="SUPER_ADMIN", ativo=True):
    with app_client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["email"] = "super@example.com"
        sess["perfil"] = perfil
        sess["ativo"] = ativo


def _usuario(usuario_id=1, email="super@example.com", perfil="SUPER_ADMIN", ativo=True):
    return Usuario(
        usuario_id=usuario_id,
        email=email,
        senha_hash="hash",
        pergunta_recuperacao="Pergunta?",
        resposta_recuperacao_hash="resp-hash",
        perfil=perfil,
        ativo=ativo,
    )


def test_super_admin_acessa_gestao_de_usuarios(app_client, monkeypatch):
    _login(app_client, perfil="SUPER_ADMIN")
    monkeypatch.setattr(
        app_module.usuarios_service,
        "listar_usuarios",
        lambda: [_usuario(1, "super@example.com", "SUPER_ADMIN"), _usuario(2, "admin@example.com", "ADMIN")],
    )

    response = app_client.get("/usuarios")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Gestão de usuários" in html
    assert "super@example.com" in html
    assert "admin@example.com" in html


@pytest.mark.parametrize("perfil", ["ADMIN", "USUARIO", "LEITOR"])
def test_perfis_sem_permissao_recebem_403_em_usuarios(app_client, perfil):
    _login(app_client, perfil=perfil)

    response = app_client.get("/usuarios")

    assert response.status_code == 403


def test_super_admin_altera_perfil_de_outro_usuario(app_client, monkeypatch):
    _login(app_client, perfil="SUPER_ADMIN")
    captured = {}

    def _fake_atualizar_perfil(usuario_id, novo_perfil, usuario_logado_id):
        captured.update({"usuario_id": usuario_id, "novo_perfil": novo_perfil, "usuario_logado_id": usuario_logado_id})
        return _usuario(usuario_id, "alvo@example.com", novo_perfil, True)

    monkeypatch.setattr(app_module.usuarios_service, "atualizar_perfil", _fake_atualizar_perfil)

    response = app_client.post(
        "/usuarios/2/perfil",
        json={"perfil": "ADMIN"},
        headers=_csrf_headers(app_client),
    )

    assert response.status_code == 200
    assert response.get_json()["ok"] is True
    assert captured == {"usuario_id": 2, "novo_perfil": "ADMIN", "usuario_logado_id": 1}


def test_super_admin_atualiza_status_de_outro_usuario(app_client, monkeypatch):
    _login(app_client, perfil="SUPER_ADMIN")
    captured = {}

    def _fake_alternar_status(usuario_id, ativo, usuario_logado_id):
        captured.update({"usuario_id": usuario_id, "ativo": ativo, "usuario_logado_id": usuario_logado_id})
        return _usuario(usuario_id, "alvo@example.com", "USUARIO", ativo)

    monkeypatch.setattr(app_module.usuarios_service, "alternar_status", _fake_alternar_status)

    response = app_client.post(
        "/usuarios/2/status",
        json={"ativo": False},
        headers=_csrf_headers(app_client),
    )

    assert response.status_code == 200
    assert response.get_json()["ok"] is True
    assert captured == {"usuario_id": 2, "ativo": False, "usuario_logado_id": 1}


def test_super_admin_cria_usuario(app_client, monkeypatch):
    _login(app_client, perfil="SUPER_ADMIN")
    captured = {}

    def _fake_registrar_usuario(email, senha, pergunta, resposta, perfil="USUARIO", ativo=True):
        captured.update(
            {
                "email": email,
                "senha": senha,
                "pergunta": pergunta,
                "resposta": resposta,
                "perfil": perfil,
                "ativo": ativo,
            }
        )
        return 44

    monkeypatch.setattr(app_module.auth_service, "registrar_usuario", _fake_registrar_usuario)

    response = app_client.post(
        "/usuarios/criar",
        json={
            "email": "novo@example.com",
            "senha": "Senha@12345",
            "pergunta_recuperacao": "Cor favorita?",
            "resposta_recuperacao": "Azul",
            "perfil": "USUARIO",
            "ativo": True,
        },
        headers=_csrf_headers(app_client),
    )

    assert response.status_code == 201
    assert response.get_json() == {"ok": True, "user_id": 44}
    assert captured["email"] == "novo@example.com"
    assert captured["perfil"] == "USUARIO"


def test_admin_nao_acessa_criacao_de_usuario(app_client):
    _login(app_client, perfil="ADMIN")

    response = app_client.post(
        "/usuarios/criar",
        json={
            "email": "novo@example.com",
            "senha": "Senha@12345",
            "pergunta_recuperacao": "Cor favorita?",
            "resposta_recuperacao": "Azul",
        },
        headers=_csrf_headers(app_client),
    )

    assert response.status_code == 403
