import importlib
import os

import mysql.connector
import pytest
from werkzeug.exceptions import Forbidden

from controle_ativos.utils.security import CSRF_SESSION_KEY


os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-errors")
app_module = importlib.import_module("controle_ativos.web.app")


@pytest.fixture()
def client():
    app_module.app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)
    return app_module.app.test_client()


def _csrf_headers(client):
    client.get("/")
    with client.session_transaction() as sess:
        token = sess[CSRF_SESSION_KEY]
    return {"X-CSRF-Token": token}


def test_404_api_retorna_resposta_controlada(client):
    response = client.get("/nao-existe")

    assert response.status_code == 404
    assert response.get_json() == {"ok": False, "erro": "Página não encontrada."}


def test_404_html_retorna_pagina_controlada(client):
    response = client.get("/dashboard/nao-existe")

    assert response.status_code == 404
    assert response.content_type.startswith("text/html")
    assert "Página não encontrada" in response.get_data(as_text=True)


def test_403_html_retorna_pagina_controlada(client, monkeypatch):
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["email"] = "tester@example.com"
        sess["perfil"] = "ADMIN"
        sess["ativo"] = True

    def _raise_forbidden():
        raise Forbidden()

    monkeypatch.setitem(app_module.app.view_functions, "dashboard_page", _raise_forbidden)

    response = client.get("/dashboard")

    assert response.status_code == 403
    assert response.content_type.startswith("text/html")
    assert b"Acesso negado. Seu perfil n" in response.data
    assert b"Voltar ao dashboard" in response.data


def test_405_api_retorna_resposta_controlada(client):
    response = client.get("/login")

    assert response.status_code == 405
    assert response.get_json() == {"ok": False, "erro": "Método não permitido."}


def test_500_simulado_nao_expoe_traceback(client, monkeypatch):
    def _raise_unexpected(**kwargs):
        raise ValueError("traceback secret")

    monkeypatch.setattr(app_module.auth_service, "registrar_usuario", _raise_unexpected)

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
    assert response.get_json() == {
        "ok": False,
        "erro": "Erro interno. Tente novamente mais tarde.",
    }
    assert b"Traceback" not in response.data
    assert b"traceback secret" not in response.data


def test_mysql_erro_no_cadastro_nao_revela_detalhe(client, monkeypatch):
    def _raise_mysql_error(**kwargs):
        raise mysql.connector.Error("mysql detail exposed")

    monkeypatch.setattr(app_module.auth_service, "registrar_usuario", _raise_mysql_error)

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
    assert response.get_json() == {
        "ok": False,
        "erro": "Erro interno. Tente novamente mais tarde.",
    }
    assert b"mysql detail exposed" not in response.data
