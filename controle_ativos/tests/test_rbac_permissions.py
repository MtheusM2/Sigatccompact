import importlib
import os
from types import SimpleNamespace

import pytest

from controle_ativos.models.ativos import Ativo
from controle_ativos.utils.permissions import can_manage_user, has_permission, has_role


os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-rbac")
app_module = importlib.import_module("controle_ativos.web.app")


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


def test_leitor_acessa_dashboard_e_listagem(client, monkeypatch):
    _login(client, perfil="LEITOR")
    monkeypatch.setattr(app_module.ativos_service, "listar_ativos", lambda user_id: [_ativo()])

    response_dashboard = client.get("/dashboard")
    response_listagem = client.get("/ativos")

    assert response_dashboard.status_code == 200
    assert response_listagem.status_code == 200
    assert response_listagem.get_json()["ativos"][0]["id"] == "AT-001"
    assert b"Cadastrar ativos" not in response_dashboard.data
    assert b"Editar ativos" not in response_dashboard.data
    assert b"Excluir ativos" not in response_dashboard.data


def test_dashboard_exibe_dados_do_usuario(client):
    _login(client, perfil="USUARIO")

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"tester@example.com" in response.data
    assert b"USUARIO" in response.data


@pytest.mark.parametrize("perfil", ["LEITOR", "GUEST"])
def test_perfil_sem_permissao_nao_cria_ativo(client, perfil):
    _login(client, perfil=perfil)

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

    assert response.status_code == 403


@pytest.mark.parametrize("perfil", ["LEITOR", "GUEST"])
def test_perfil_sem_permissao_nao_edita_ativo(client, perfil):
    _login(client, perfil=perfil)

    response = client.put(
        "/ativos/AT-001",
        json={"modelo": "XPS"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 403


@pytest.mark.parametrize("perfil", ["USUARIO", "LEITOR", "GUEST"])
def test_perfil_sem_permissao_nao_exclui_ativo(client, perfil):
    _login(client, perfil=perfil)

    response = client.delete("/ativos/AT-001", headers=_csrf_headers(client))

    assert response.status_code == 403


@pytest.mark.parametrize("perfil", ["USUARIO", "ADMIN", "SUPER_ADMIN"])
def test_perfil_autorizado_cria_ativo(client, monkeypatch, perfil):
    _login(client, perfil=perfil)
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
    assert captured["user_id"] == 1
    assert captured["ativo"].id_ativo == "AT-GERADO"


@pytest.mark.parametrize("perfil", ["USUARIO", "ADMIN", "SUPER_ADMIN"])
def test_perfil_autorizado_edita_ativo(client, monkeypatch, perfil):
    _login(client, perfil=perfil)
    monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", lambda **kwargs: _ativo())

    response = client.put(
        "/ativos/AT-001",
        json={"modelo": "XPS"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 200


@pytest.mark.parametrize("perfil", ["ADMIN", "SUPER_ADMIN"])
def test_perfil_autorizado_exclui_ativo(client, monkeypatch, perfil):
    _login(client, perfil=perfil)
    captured = {}

    def _fake_remover_ativo(id_ativo, user_id):
        captured["id_ativo"] = id_ativo
        captured["user_id"] = user_id

    monkeypatch.setattr(app_module.ativos_service, "remover_ativo", _fake_remover_ativo)

    response = client.delete("/ativos/AT-001", headers=_csrf_headers(client))

    assert response.status_code == 200
    assert captured == {"id_ativo": "AT-001", "user_id": 1}


@pytest.mark.parametrize(
    "perfil,espera_excluir",
    [
        ("LEITOR", False),
        ("USUARIO", False),
        ("ADMIN", True),
        ("SUPER_ADMIN", True),
    ],
)
def test_dashboard_exibe_excluir_apenas_para_perfis_admin(client, perfil, espera_excluir):
    _login(client, perfil=perfil)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Excluir ativos" not in response.data


@pytest.mark.parametrize("perfil", ["SUPER_ADMIN", "ADMIN", "USUARIO", "LEITOR"])
def test_todos_os_perfis_autenticados_visualizam_ativos_globais(client, monkeypatch, perfil):
    _login(client, perfil=perfil)
    monkeypatch.setattr(
        app_module.ativos_service,
        "listar_ativos",
        lambda user_id: [_ativo(id_ativo="AT-001", criado_por=1), _ativo(id_ativo="AT-002", criado_por=2)],
    )

    response = client.get("/ativos")

    assert response.status_code == 200
    ativos = response.get_json()["ativos"]
    assert [ativo["id"] for ativo in ativos] == ["AT-001", "AT-002"]
    assert {ativo["criado_por"] for ativo in ativos} == {1, 2}


@pytest.mark.parametrize("perfil", ["ADMIN", "USUARIO", "LEITOR"])
def test_gestao_de_usuarios_rejeita_perfis_nao_super_admin(client, perfil):
    _login(client, perfil=perfil)

    response = client.get("/usuarios")

    assert response.status_code == 403
    assert b"Acesso negado" in response.data


def test_usuario_inativo_nao_autentica(client, monkeypatch):
    class _UsuarioInativo:
        id = 9
        email = "inativo@example.com"
        perfil = "USUARIO"
        ativo = False
        bloqueado_ate = None

    monkeypatch.setattr(app_module.auth_service, "autenticar", lambda **kwargs: _UsuarioInativo())

    response = client.post(
        "/login",
        json={"email": "inativo@example.com", "senha": "Senha@12345"},
        headers=_csrf_headers(client),
    )

    assert response.status_code == 401
    assert response.get_json() == {"ok": False, "erro": "E-mail ou senha inválidos."}
    with client.session_transaction() as sess:
        assert sess.get("user_id") is None


def test_rbac_nao_override_csrf(client):
    _login(client, perfil="LEITOR")

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
        headers={"X-CSRF-Token": "invalido"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"ok": False, "erro": "CSRF inválido."}


@pytest.mark.parametrize("perfil,esperado", [("ADMIN", False), ("SUPER_ADMIN", True)])
def test_can_manage_user_admin_nao_altera_super_admin(perfil, esperado):
    usuario_logado = SimpleNamespace(id=1, perfil=perfil)
    usuario_alvo = SimpleNamespace(id=2, perfil="SUPER_ADMIN")

    assert can_manage_user(usuario_logado, usuario_alvo) is esperado


@pytest.mark.parametrize(
    "perfil,permissao,esperado",
    [
        ("LEITOR", "ativos.criar", False),
        ("USUARIO", "ativos.criar", True),
        ("ADMIN", "ativos.excluir", True),
        ("GUEST", "ativos.ver", False),
    ],
)
def test_permissoes_basicas_por_perfil(perfil, permissao, esperado):
    usuario = SimpleNamespace(perfil=perfil)

    assert has_role(usuario, perfil) is (perfil in {"LEITOR", "USUARIO", "ADMIN", "SUPER_ADMIN"})
    assert has_permission(usuario, permissao) is esperado
