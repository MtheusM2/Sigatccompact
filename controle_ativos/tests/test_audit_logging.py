import importlib
import os
import mysql.connector

import pytest

app_module = importlib.import_module("controle_ativos.web.app")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-audit")


@pytest.fixture()
def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def _csrf_headers(client, token_override=None):
    client.get("/")
    with client.session_transaction() as sess:
        token = token_override if token_override is not None else sess["_csrf_token"]
    return {"X-CSRF-Token": token}


def _login(client, user_id=1, perfil="USUARIO", ativo=True):
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["email"] = "tester@example.com"
        sess["perfil"] = perfil
        sess["ativo"] = ativo


def _capture_event(caplog, name_contains: str):
    for r in caplog.records:
        if r.name == "controle_ativos.audit" and name_contains in r.getMessage():
            return True
    return False


def test_login_success_generates_event(client, monkeypatch, caplog):
    class _UsuarioFake:
        id = 9
        email = "tester@example.com"

    monkeypatch.setattr(app_module.auth_service, "autenticar", lambda **kwargs: _UsuarioFake())

    caplog.set_level("INFO", logger="controle_ativos.audit")

    response = client.post(
        "/login",
        json={"email": "tester@example.com", "senha": "Senha@12345"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200
    assert _capture_event(caplog, '"event": "login_success"')
    assert "Senha@12345" not in caplog.text


def test_login_failure_generates_event_without_password(client, monkeypatch, caplog):
    def _raise_invalid(**kwargs):
        raise app_module.CredenciaisInvalidas("invalid")

    monkeypatch.setattr(app_module.auth_service, "autenticar", _raise_invalid)
    caplog.set_level("INFO", logger="controle_ativos.audit")

    response = client.post(
        "/login",
        json={"email": "tester@example.com", "senha": "Senha@12345"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 401
    assert _capture_event(caplog, '"event": "login_failed"')
    assert "Senha@12345" not in caplog.text


def test_rate_limit_generates_event(client, monkeypatch, caplog):
    monkeypatch.setattr(app_module, "is_auth_rate_limited", lambda *args, **kwargs: True)
    caplog.set_level("INFO", logger="controle_ativos.audit")

    response = client.post(
        "/login",
        json={"email": "tester@example.com", "senha": "x"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 429
    assert _capture_event(caplog, '"event": "rate_limit_blocked"')


def test_csrf_invalid_generates_event(client, caplog):
    caplog.set_level("INFO", logger="controle_ativos.audit")

    response = client.post(
        "/login",
        json={"email": "a@b.com", "senha": "x"},
        headers={"X-CSRF-Token": "invalido"},
    )

    assert response.status_code == 400
    assert _capture_event(caplog, '"event": "csrf_invalid"')


def test_internal_error_generates_event(client, monkeypatch, caplog):
    def _raise_db_error(*args, **kwargs):
        raise mysql.connector.Error("boom")

    monkeypatch.setattr(app_module.auth_service, "registrar_usuario", _raise_db_error)
    caplog.set_level("INFO", logger="controle_ativos.audit")

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

    assert response.status_code == 500
    assert _capture_event(caplog, '"event": "internal_error"')


def test_asset_crud_generates_events_and_no_sensitive_data(client, monkeypatch, caplog):
    _login(client, user_id=7, perfil="ADMIN")
    caplog.set_level("INFO", logger="controle_ativos.audit")

    # Create
    monkeypatch.setattr(app_module, "_gerar_id_ativo", lambda: "AT-GERADO")
    monkeypatch.setattr(app_module.ativos_service, "criar_ativo", lambda ativo, user_id: None)
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
    assert _capture_event(caplog, '"event": "asset_created"')

    # Update
    from controle_ativos.models.ativos import Ativo

    def _fake_ativo(**kwargs):
        return Ativo(
            id_ativo="AT-001",
            tipo="Notebook",
            marca="Dell",
            modelo="Latitude",
            usuario_responsavel="Joao Silva",
            departamento="TI",
            status="Disponível",
            data_entrada="2026-05-27",
            data_saida=None,
            criado_por=7,
        )

    monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", lambda **kwargs: _fake_ativo())
    response = client.put(
        "/ativos/AT-001",
        json={"modelo": "XPS"},
        headers=_csrf_headers(client),
    )
    assert response.status_code == 200
    assert _capture_event(caplog, '"event": "asset_updated"')
    assert '"id_ativo": "AT-001"' in caplog.text
    assert '"edited_by": "tester@example.com"' in caplog.text

    # Delete
    monkeypatch.setattr(app_module.ativos_service, "remover_ativo", lambda id_ativo, user_id: None)
    response = client.delete("/ativos/AT-001", headers=_csrf_headers(client))
    assert response.status_code == 200
    assert _capture_event(caplog, '"event": "asset_deleted"')

    # Ensure no sensitive data leaked
    assert "Senha@12345" not in caplog.text
    assert "resposta_recuperacao" not in caplog.text
    assert "csrf_token" not in caplog.text
