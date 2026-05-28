import importlib
import os
from datetime import timedelta

import pytest

import controle_ativos.utils.security as security_utils

from controle_ativos.utils.security import CSRF_SESSION_KEY


os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-security")
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


def _login_dummy(monkeypatch):
    class _UsuarioFake:
        id = 9
        email = "tester@example.com"

    monkeypatch.setattr(app_module.auth_service, "autenticar", lambda **kwargs: _UsuarioFake())


class _Clock:
    def __init__(self, current=1_000.0):
        self.current = current

    def monotonic(self):
        return self.current

    def advance(self, seconds):
        self.current += seconds


def test_login_cleans_old_session(client, monkeypatch):
    _login_dummy(monkeypatch)

    # Preenche a sessão com dados antigos
    with client.session_transaction() as sess:
        sess["old_key"] = "to-be-cleared"

    response = client.post(
        "/login",
        json={"email": "a@b.com", "senha": "x"},
        headers=_csrf_headers(client),
    )
    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert "old_key" not in sess
        assert sess["user_id"] == 9
        assert sess["email"] == "tester@example.com"


def test_logout_clears_session(client):
    # Preenche a sessão com dados e depois desloga
    with client.session_transaction() as sess:
        sess["user_id"] = 5
        sess["email"] = "x@x.com"

    response = client.post("/logout", headers=_csrf_headers(client))
    assert response.status_code == 200

    with client.session_transaction() as sess:
        # A sessão deve estar limpa após logout
        assert sess.keys() == set()


def test_logout_without_csrf_is_rejected(client):
    response = client.post("/logout")

    assert response.status_code == 400
    assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


def test_login_without_csrf_is_rejected(client, monkeypatch):
    _login_dummy(monkeypatch)

    response = client.post("/login", json={"email": "a@b.com", "senha": "x"})

    assert response.status_code == 400
    assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


def test_login_with_invalid_csrf_is_rejected(client, monkeypatch):
    _login_dummy(monkeypatch)

    response = client.post(
        "/login",
        json={"email": "a@b.com", "senha": "x"},
        headers=_csrf_headers(client, token_override="token-invalido"),
    )

    assert response.status_code == 400
    assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


def test_login_with_valid_csrf_continues_working(client, monkeypatch):
    _login_dummy(monkeypatch)

    response = client.post(
        "/login",
        json={"email": "a@b.com", "senha": "x"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200
    assert response.get_json() == {"ok": True, "email": "tester@example.com"}


@pytest.mark.parametrize(
    "erro_publico",
    [
        app_module.UsuarioNaoEncontrado("usuario ausente"),
        app_module.CredenciaisInvalidas("senha incorreta"),
    ],
)
def test_login_exibe_mensagem_generica_para_falhas_distintas(client, monkeypatch, erro_publico):
    def _fake_autenticar(**kwargs):
        raise erro_publico

    monkeypatch.setattr(app_module.auth_service, "autenticar", _fake_autenticar)

    response = client.post(
        "/login",
        json={"email": "tester@example.com", "senha": "Senha@12345"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 401
    assert response.get_json() == {"ok": False, "erro": "E-mail ou senha inválidos."}


def test_login_bloqueia_temporariamente_apos_multiplas_falhas(client, monkeypatch):
    clock = _Clock()
    monkeypatch.setattr(security_utils.time, "monotonic", clock.monotonic)

    def _fake_autenticar(**kwargs):
        raise app_module.CredenciaisInvalidas("senha incorreta")

    monkeypatch.setattr(app_module.auth_service, "autenticar", _fake_autenticar)

    headers = _csrf_headers(client)
    payload = {"email": "tester@example.com", "senha": "Senha@12345"}

    for _ in range(security_utils.AUTH_RATE_LIMIT_MAX_FAILURES):
        response = client.post("/login", json=payload, headers=headers)
        assert response.status_code == 401
        assert response.get_json() == {"ok": False, "erro": "E-mail ou senha inválidos."}

    response = client.post("/login", json=payload, headers=headers)
    assert response.status_code == 429
    assert response.get_json() == {
        "ok": False,
        "erro": security_utils.AUTH_RATE_LIMIT_MESSAGE,
    }

    clock.advance(security_utils.AUTH_RATE_LIMIT_BLOCK_SECONDS + 1)

    class _UsuarioLiberado:
        id = 15
        email = "tester@example.com"

    monkeypatch.setattr(app_module.auth_service, "autenticar", lambda **kwargs: _UsuarioLiberado())

    response = client.post("/login", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.get_json() == {"ok": True, "email": "tester@example.com"}


@pytest.mark.parametrize(
    "erro_publico",
    [
        app_module.UsuarioNaoEncontrado("usuario ausente"),
        app_module.RecuperacaoInvalida("resposta incorreta"),
    ],
)
def test_recuperacao_exibe_mensagem_generica_sem_enumerar_usuario(
    client,
    monkeypatch,
    erro_publico,
):
    def _fake_redefinir_senha(**kwargs):
        raise erro_publico

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

    assert response.status_code == 401
    assert response.get_json() == {
        "ok": False,
        "erro": "Não foi possível confirmar seus dados de recuperação.",
    }


def test_recuperacao_bloqueia_temporariamente_apos_multiplas_falhas(client, monkeypatch):
    clock = _Clock()
    monkeypatch.setattr(security_utils.time, "monotonic", clock.monotonic)

    def _fake_redefinir_senha(**kwargs):
        raise app_module.RecuperacaoInvalida("resposta incorreta")

    monkeypatch.setattr(app_module.auth_service, "redefinir_senha", _fake_redefinir_senha)

    headers = _csrf_headers(client)
    payload = {
        "email": "tester@example.com",
        "resposta_recuperacao": "Azul",
        "nova_senha": "Senha@12345",
    }

    for _ in range(security_utils.AUTH_RATE_LIMIT_MAX_FAILURES):
        response = client.post("/forgot-password", json=payload, headers=headers)
        assert response.status_code == 401
        assert response.get_json() == {
            "ok": False,
            "erro": "Não foi possível confirmar seus dados de recuperação.",
        }

    response = client.post("/forgot-password", json=payload, headers=headers)
    assert response.status_code == 429
    assert response.get_json() == {
        "ok": False,
        "erro": security_utils.AUTH_RATE_LIMIT_MESSAGE,
    }


def test_session_cookie_configured_explicitly():
    cfg = app_module.app.config
    assert cfg["SESSION_COOKIE_HTTPONLY"] is True
    assert cfg["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert isinstance(cfg["PERMANENT_SESSION_LIFETIME"], timedelta)


def test_get_routes_do_not_require_csrf(client):
    response = client.get("/")
    assert response.status_code == 200
