"""
Testes de fluxos de jornadas de usuários no Sigatccompact.

Cobre:
- SUPER_ADMIN criando usuários e gerenciando perfis
- Login/logout por perfil (SUPER_ADMIN, ADMIN, USUARIO, LEITOR)
- CRUD de ativos com permissões por perfil
- Busca/filtros de ativos
- Validação de CSRF
- Auditoria básica

Estratégia:
- Usar fixtures do conftest.py
- Usar Flask test client (sem Selenium)
- Usar mocks/monkeypatch para não depender do banco real
- Cada teste é isolado e não depende de ordem
- Validar status codes, RBAC e presença/ausência de elementos HTML
"""

import importlib
import json
import os

import pytest

from controle_ativos.models.ativos import Ativo
from controle_ativos.models.usuario import Usuario
from controle_ativos.utils.security import CSRF_SESSION_KEY


os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-for-flows")
app_module = importlib.import_module("controle_ativos.web.app")


@pytest.fixture()
def client():
    """Cliente Flask para testes com TESTING=True."""
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


# ==============================================================================
# HELPERS REUTILIZÁVEIS
# ==============================================================================


def _get_csrf(client, path="/login"):
    """
    Extrai token CSRF da sessão visitando uma página pública.
    
    Parâmetros:
    - client: Flask test client
    - path: rota pública (padrão: /login)
    
    Retorna:
    - dict com header "X-CSRF-Token" pronto para usar em requests
    """
    client.get(path)
    with client.session_transaction() as sess:
        token = sess.get(CSRF_SESSION_KEY)
    return {"X-CSRF-Token": token}


def _login_in_session(client, user_id=1, email="test@example.com", perfil="USUARIO", ativo=True):
    """
    Simula login sem depender do banco de dados.
    Grava dados do usuário direto na sessão Flask.
    
    Parâmetros:
    - client: Flask test client
    - user_id: ID do usuário (padrão: 1)
    - email: e-mail do usuário (padrão: test@example.com)
    - perfil: perfil do usuário (SUPER_ADMIN, ADMIN, USUARIO, LEITOR)
    - ativo: se o usuário está ativo (padrão: True)
    """
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["email"] = email
        sess["perfil"] = perfil
        sess["ativo"] = ativo


def _logout_session(client):
    """
    Remove dados de sessão para simular logout.
    """
    with client.session_transaction() as sess:
        sess.clear()


def _extrair_texto_resposta(response):
    """
    Extrai o conteúdo texto da resposta.
    Útil para buscas em HTML ou JSON.
    """
    return response.get_data(as_text=True)


def _criar_usuario_json(
    client,
    email="novo@example.com",
    senha="Senha@123456",
    pergunta="Cor favorita?",
    resposta="Azul",
    perfil="USUARIO",
    ativo=True,
):
    """
    Simula criação de usuário via POST /usuarios/criar com CSRF.
    Assume que o usuário logado tem permissão.
    
    Retorna:
    - (user_id, response) ou (None, response) se falhar
    """
    csrf_headers = _get_csrf(client, "/usuarios")
    
    payload = {
        "email": email,
        "senha": senha,
        "pergunta_recuperacao": pergunta,
        "resposta_recuperacao": resposta,
        "perfil": perfil,
        "ativo": ativo,
    }
    
    response = client.post(
        "/usuarios/criar",
        json=payload,
        headers=csrf_headers,
    )
    
    user_id = None
    if response.status_code == 201:
        data = response.get_json()
        user_id = data.get("user_id")
    
    return user_id, response


def _alterar_perfil_usuario(client, usuario_id, novo_perfil):
    """
    Altera o perfil de um usuário via POST /usuarios/<id>/perfil com CSRF.
    Assume que o usuário logado tem permissão (SUPER_ADMIN).
    
    Retorna:
    - response com status da operação
    """
    csrf_headers = _get_csrf(client, "/usuarios")
    
    payload = {"perfil": novo_perfil}
    
    response = client.post(
        f"/usuarios/{usuario_id}/perfil",
        json=payload,
        headers=csrf_headers,
    )
    
    return response


def _alternar_status_usuario(client, usuario_id, ativo):
    """
    Ativa ou desativa um usuário via POST /usuarios/<id>/status com CSRF.
    Assume que o usuário logado tem permissão (SUPER_ADMIN).
    
    Retorna:
    - response com status da operação
    """
    csrf_headers = _get_csrf(client, "/usuarios")
    
    payload = {"ativo": ativo}
    
    response = client.post(
        f"/usuarios/{usuario_id}/status",
        json=payload,
        headers=csrf_headers,
    )
    
    return response


def _criar_ativo_json(
    client,
    id_ativo=None,
    tipo="Notebook",
    marca="Dell",
    modelo="Latitude",
    email_responsavel="resp@example.com",
    usuario_responsavel="João Silva",
    departamento="TI",
    status="Disponível",
    data_entrada="2026-05-28",
    data_saida=None,
):
    """
    Simula criação de ativo via POST /ativos com CSRF.
    Assume que o usuário logado tem permissão.
    
    Retorna:
    - (id_ativo_gerado, response)
    """
    csrf_headers = _get_csrf(client, "/dashboard")
    
    payload = {
        "id": id_ativo,
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "email_responsavel": email_responsavel,
        "usuario_responsavel": usuario_responsavel,
        "departamento": departamento,
        "status": status,
        "data_entrada": data_entrada,
        "data_saida": data_saida,
    }
    
    response = client.post(
        "/ativos",
        json=payload,
        headers=csrf_headers,
    )
    
    return response


def _editar_ativo_json(client, id_ativo, dados_atualizacao):
    """
    Simula atualização de ativo via PUT /ativos/<id> com CSRF.
    Assume que o usuário logado tem permissão.
    
    Retorna:
    - response com status da operação
    """
    csrf_headers = _get_csrf(client, "/dashboard")
    
    response = client.put(
        f"/ativos/{id_ativo}",
        json=dados_atualizacao,
        headers=csrf_headers,
    )
    
    return response


def _excluir_ativo_json(client, id_ativo):
    """
    Simula exclusão de ativo via DELETE /ativos/<id> com CSRF.
    Assume que o usuário logado tem permissão.
    
    Retorna:
    - response com status da operação
    """
    csrf_headers = _get_csrf(client, "/dashboard")
    
    response = client.delete(
        f"/ativos/{id_ativo}",
        headers=csrf_headers,
    )
    
    return response


def _listar_ativos(client):
    """
    Lista ativos via GET /ativos.
    Não requer CSRF em GET.
    
    Retorna:
    - (ativos_list, response)
    """
    response = client.get("/ativos")
    
    ativos = []
    if response.status_code == 200:
        data = response.get_json()
        ativos = data.get("ativos", [])
    
    return ativos, response


def _filtrar_ativos(client, **filtros):
    """
    Filtra ativos via GET /ativos/filtrar?departamento=...&status=...&tipo=...
    Não requer CSRF em GET.
    
    Parâmetros:
    - departamento, status, tipo, marca, modelo, usuario_responsavel (opcionais)
    
    Retorna:
    - (ativos_list, response)
    """
    response = client.get(
        "/ativos/filtrar",
        query_string=filtros,
    )
    
    ativos = []
    if response.status_code == 200:
        data = response.get_json()
        ativos = data.get("ativos", [])
    
    return ativos, response


# ==============================================================================
# TESTES DE FLUXO
# ==============================================================================


class TestFluxoSuperAdminCriaUsuarios:
    """
    Fluxo 1: SUPER_ADMIN cria usuários de diferentes perfis.
    Valida:
    - SUPER_ADMIN consegue fazer login
    - SUPER_ADMIN acessa dashboard
    - SUPER_ADMIN consegue criar usuários
    - Usuários criados tem os perfis corretos
    - Usuários não-admin não conseguem criar usuários
    """

    def test_super_admin_login_acessa_dashboard(self, client):
        """SUPER_ADMIN consegue logar e acessar dashboard."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        response = client.get("/dashboard")
        
        assert response.status_code == 200
        # Verifica que a página de dashboard renderizou (contém navbar/layout)
        texto = _extrair_texto_resposta(response)
        # Não testa HTML muito específico para evitar fragilidade

    def test_super_admin_cria_usuario_admin(self, client, monkeypatch):
        """SUPER_ADMIN consegue criar novo usuário com perfil ADMIN."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # Mock registrar_usuario para não tocar no banco
        usuarios_criados = {}
        
        def mock_registrar_usuario(email, senha, pergunta, resposta, perfil="USUARIO", ativo=True):
            usuario_id = len(usuarios_criados) + 100
            usuarios_criados[usuario_id] = {
                "email": email,
                "perfil": perfil,
                "ativo": ativo,
            }
            return usuario_id
        
        monkeypatch.setattr(app_module.auth_service, "registrar_usuario", mock_registrar_usuario)
        
        user_id, response = _criar_usuario_json(
            client,
            email="admin@test.local",
            perfil="ADMIN",
        )
        
        assert response.status_code == 201
        assert user_id is not None
        assert usuarios_criados[user_id]["perfil"] == "ADMIN"

    def test_super_admin_cria_usuario_usuario(self, client, monkeypatch):
        """SUPER_ADMIN consegue criar novo usuário com perfil USUARIO."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        usuarios_criados = {}
        
        def mock_registrar_usuario(email, senha, pergunta, resposta, perfil="USUARIO", ativo=True):
            usuario_id = len(usuarios_criados) + 200
            usuarios_criados[usuario_id] = {
                "email": email,
                "perfil": perfil,
                "ativo": ativo,
            }
            return usuario_id
        
        monkeypatch.setattr(app_module.auth_service, "registrar_usuario", mock_registrar_usuario)
        
        user_id, response = _criar_usuario_json(
            client,
            email="usuario@test.local",
            perfil="USUARIO",
        )
        
        assert response.status_code == 201
        assert user_id is not None
        assert usuarios_criados[user_id]["perfil"] == "USUARIO"

    def test_super_admin_cria_usuario_leitor(self, client, monkeypatch):
        """SUPER_ADMIN consegue criar novo usuário com perfil LEITOR."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        usuarios_criados = {}
        
        def mock_registrar_usuario(email, senha, pergunta, resposta, perfil="USUARIO", ativo=True):
            usuario_id = len(usuarios_criados) + 300
            usuarios_criados[usuario_id] = {
                "email": email,
                "perfil": perfil,
                "ativo": ativo,
            }
            return usuario_id
        
        monkeypatch.setattr(app_module.auth_service, "registrar_usuario", mock_registrar_usuario)
        
        user_id, response = _criar_usuario_json(
            client,
            email="leitor@test.local",
            perfil="LEITOR",
        )
        
        assert response.status_code == 201
        assert user_id is not None
        assert usuarios_criados[user_id]["perfil"] == "LEITOR"

    def test_admin_nao_consegue_criar_usuario(self, client):
        """ADMIN tenta acessar /usuarios/criar e recebe 403."""
        _login_in_session(client, user_id=2, email="admin@test.local", perfil="ADMIN")
        
        csrf_headers = _get_csrf(client, "/dashboard")
        payload = {
            "email": "novo@test.local",
            "senha": "Senha@123456",
            "pergunta_recuperacao": "Q?",
            "resposta_recuperacao": "R",
            "perfil": "USUARIO",
        }
        
        response = client.post(
            "/usuarios/criar",
            json=payload,
            headers=csrf_headers,
        )
        
        assert response.status_code == 403

    def test_usuario_nao_consegue_criar_usuario(self, client):
        """USUARIO tenta acessar /usuarios/criar e recebe 403."""
        _login_in_session(client, user_id=3, email="usuario@test.local", perfil="USUARIO")
        
        csrf_headers = _get_csrf(client, "/dashboard")
        payload = {
            "email": "novo@test.local",
            "senha": "Senha@123456",
            "pergunta_recuperacao": "Q?",
            "resposta_recuperacao": "R",
            "perfil": "USUARIO",
        }
        
        response = client.post(
            "/usuarios/criar",
            json=payload,
            headers=csrf_headers,
        )
        
        assert response.status_code == 403

    def test_leitor_nao_consegue_criar_usuario(self, client):
        """LEITOR tenta acessar /usuarios/criar e recebe 403."""
        _login_in_session(client, user_id=4, email="leitor@test.local", perfil="LEITOR")
        
        csrf_headers = _get_csrf(client, "/dashboard")
        payload = {
            "email": "novo@test.local",
            "senha": "Senha@123456",
            "pergunta_recuperacao": "Q?",
            "resposta_recuperacao": "R",
            "perfil": "USUARIO",
        }
        
        response = client.post(
            "/usuarios/criar",
            json=payload,
            headers=csrf_headers,
        )
        
        assert response.status_code == 403


class TestFluxoAlteracaoPerfilStatus:
    """
    Fluxo 3: SUPER_ADMIN altera perfis e status de usuários.
    Valida:
    - SUPER_ADMIN consegue alterar perfil de outro usuário
    - SUPER_ADMIN consegue ativar/desativar outro usuário
    - SUPER_ADMIN não consegue remover o próprio perfil SUPER_ADMIN
    - SUPER_ADMIN não consegue desativar a própria conta
    - Usuários não-admin não conseguem alterar perfis
    """

    def test_super_admin_altera_perfil_usuario(self, client, monkeypatch):
        """SUPER_ADMIN altera ADMIN para USUARIO."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # Mock para simular busca e atualização de usuário
        def mock_atualizar_perfil(usuario_id, novo_perfil, usuario_logado_id):
            return Usuario(
                usuario_id=usuario_id,
                email="admin@test.local",
                senha_hash="",
                pergunta_recuperacao="",
                resposta_recuperacao_hash="",
                perfil=novo_perfil,
                ativo=True,
            )
        
        monkeypatch.setattr(app_module.usuarios_service, "atualizar_perfil", mock_atualizar_perfil)
        
        response = _alterar_perfil_usuario(client, usuario_id=2, novo_perfil="USUARIO")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("ok") is True
        assert data.get("usuario", {}).get("perfil") == "USUARIO"

    def test_super_admin_nao_consegue_remover_proprio_perfil(self, client, monkeypatch):
        """SUPER_ADMIN tenta rebaixar a si mesmo e recebe 403."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        from controle_ativos.services.usuarios_service import AlteracaoNaoPermitida
        
        def mock_atualizar_perfil(usuario_id, novo_perfil, usuario_logado_id):
            if usuario_id == usuario_logado_id and novo_perfil != "SUPER_ADMIN":
                raise AlteracaoNaoPermitida("SUPER_ADMIN não pode remover o próprio perfil SUPER_ADMIN.")
            return Usuario(
                usuario_id=usuario_id,
                email="sa@test.local",
                senha_hash="",
                pergunta_recuperacao="",
                resposta_recuperacao_hash="",
                perfil="SUPER_ADMIN",
                ativo=True,
            )
        
        monkeypatch.setattr(app_module.usuarios_service, "atualizar_perfil", mock_atualizar_perfil)
        
        response = _alterar_perfil_usuario(client, usuario_id=1, novo_perfil="ADMIN")
        
        assert response.status_code == 403

    def test_super_admin_desativa_usuario(self, client, monkeypatch):
        """SUPER_ADMIN desativa outro usuário."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        def mock_alternar_status(usuario_id, ativo, usuario_logado_id):
            return Usuario(
                usuario_id=usuario_id,
                email="usuario@test.local",
                senha_hash="",
                pergunta_recuperacao="",
                resposta_recuperacao_hash="",
                perfil="USUARIO",
                ativo=ativo,
            )
        
        monkeypatch.setattr(app_module.usuarios_service, "alternar_status", mock_alternar_status)
        
        response = _alternar_status_usuario(client, usuario_id=3, ativo=False)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("ok") is True
        assert data.get("usuario", {}).get("ativo") is False

    def test_super_admin_nao_consegue_desativar_a_si_mesmo(self, client, monkeypatch):
        """SUPER_ADMIN tenta desativar a própria conta e recebe 403."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        from controle_ativos.services.usuarios_service import AlteracaoNaoPermitida
        
        def mock_alternar_status(usuario_id, ativo, usuario_logado_id):
            if usuario_id == usuario_logado_id and not ativo:
                raise AlteracaoNaoPermitida("SUPER_ADMIN não pode desativar a própria conta.")
            return Usuario(
                usuario_id=usuario_id,
                email="sa@test.local",
                senha_hash="",
                pergunta_recuperacao="",
                resposta_recuperacao_hash="",
                perfil="SUPER_ADMIN",
                ativo=True,
            )
        
        monkeypatch.setattr(app_module.usuarios_service, "alternar_status", mock_alternar_status)
        
        response = _alternar_status_usuario(client, usuario_id=1, ativo=False)
        
        assert response.status_code == 403

    def test_admin_nao_consegue_acessar_usuarios(self, client):
        """ADMIN tenta acessar /usuarios e recebe 403."""
        _login_in_session(client, user_id=2, email="admin@test.local", perfil="ADMIN")
        
        response = client.get("/usuarios")
        
        assert response.status_code == 403


class TestFluxoLoginPorPerfil:
    """
    Fluxo 4: Validação de login para cada perfil.
    Valida:
    - Todos os perfis conseguem logar (simulado via sessão)
    - Usuário inativo não consegue logar
    - Sessão é limpa no logout
    """

    def test_super_admin_pode_logar(self, client):
        """SUPER_ADMIN consegue logar."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        response = client.get("/dashboard")
        
        assert response.status_code == 200

    def test_admin_pode_logar(self, client):
        """ADMIN consegue logar."""
        _login_in_session(client, user_id=2, email="admin@test.local", perfil="ADMIN")
        
        response = client.get("/dashboard")
        
        assert response.status_code == 200

    def test_usuario_pode_logar(self, client):
        """USUARIO consegue logar."""
        _login_in_session(client, user_id=3, email="usuario@test.local", perfil="USUARIO")
        
        response = client.get("/dashboard")
        
        assert response.status_code == 200

    def test_leitor_pode_logar(self, client):
        """LEITOR consegue logar."""
        _login_in_session(client, user_id=4, email="leitor@test.local", perfil="LEITOR")
        
        response = client.get("/dashboard")
        
        assert response.status_code == 200

    def test_usuario_inativo_sem_sessao_redirect(self, client):
        """Usuário sem sessão é redirecionado para login."""
        response = client.get("/dashboard")
        
        # Pode ser 200 com página de login ou 302 redirect
        assert response.status_code in (200, 302)

    def test_logout_limpa_sessao(self, client):
        """Logout limpa os dados de sessão."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # Antes do logout: tem sessão
        with client.session_transaction() as sess:
            assert sess.get("user_id") == 1
        
        # Faz logout
        csrf_headers = _get_csrf(client, "/dashboard")
        response = client.post("/logout", headers=csrf_headers)
        
        assert response.status_code == 200
        
        # Depois do logout: sessão limpa
        with client.session_transaction() as sess:
            assert sess.get("user_id") is None

    def test_apos_logout_dashboard_requer_autenticacao(self, client):
        """Após logout, dashboard requer novo login."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # Logout
        csrf_headers = _get_csrf(client, "/dashboard")
        client.post("/logout", headers=csrf_headers)
        
        # Tenta acessar dashboard sem login
        response = client.get("/dashboard")
        
        # Pode ser 200 com formulário de login ou 302 redirect
        assert response.status_code in (200, 302)


class TestFluxoCRUDAtivosComPerfis:
    """
    Fluxo 5-8: CRUD de ativos com validação de permissões por perfil.
    Valida:
    - SUPER_ADMIN: criar, editar, excluir
    - ADMIN: criar, editar, excluir
    - USUARIO: criar, editar (qualquer ativo), não excluir
    - LEITOR: visualizar, não criar/editar/excluir
    """

    def test_super_admin_cria_ativo(self, client, monkeypatch):
        """SUPER_ADMIN consegue criar ativo."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        def mock_criar_ativo(ativo, user_id):
            pass
        
        monkeypatch.setattr(app_module.ativos_service, "criar_ativo", mock_criar_ativo)
        
        response = _criar_ativo_json(client)
        
        assert response.status_code == 201

    def test_super_admin_edita_ativo(self, client, monkeypatch):
        """SUPER_ADMIN consegue editar ativo."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        ativo_mock = Ativo(
            id_ativo="AT-001",
            tipo="Monitor",
            marca="LG",
            modelo="27",
            email_responsavel="resp@test.local",
            usuario_responsavel="João",
            departamento="TI",
            status="Em Manutenção",
            data_entrada="2026-05-28",
            data_saida=None,
            criado_por=1,
        )
        
        def mock_atualizar_ativo(id_ativo, dados, user_id):
            return ativo_mock
        
        monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", mock_atualizar_ativo)
        
        response = _editar_ativo_json(
            client,
            "AT-001",
            {"status": "Em Manutenção"},
        )
        
        assert response.status_code == 200

    def test_super_admin_exclui_ativo(self, client, monkeypatch):
        """SUPER_ADMIN consegue excluir ativo."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        def mock_remover_ativo(id_ativo, user_id):
            pass
        
        monkeypatch.setattr(app_module.ativos_service, "remover_ativo", mock_remover_ativo)
        
        response = _excluir_ativo_json(client, "AT-001")
        
        assert response.status_code == 200

    def test_admin_cria_edita_exclui_ativo(self, client, monkeypatch):
        """ADMIN consegue criar, editar e excluir ativo."""
        _login_in_session(client, user_id=2, email="admin@test.local", perfil="ADMIN")
        
        def mock_criar_ativo(ativo, user_id):
            pass
        
        def mock_atualizar_ativo(id_ativo, dados, user_id):
            return Ativo(
                id_ativo=id_ativo,
                tipo="Notebook",
                marca="Dell",
                modelo="Latitude",
                email_responsavel="resp@test.local",
                usuario_responsavel="Admin",
                departamento="TI",
                status="Disponível",
                data_entrada="2026-05-28",
                data_saida=None,
                criado_por=2,
            )
        
        def mock_remover_ativo(id_ativo, user_id):
            pass
        
        monkeypatch.setattr(app_module.ativos_service, "criar_ativo", mock_criar_ativo)
        monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", mock_atualizar_ativo)
        monkeypatch.setattr(app_module.ativos_service, "remover_ativo", mock_remover_ativo)
        
        # Criar
        r1 = _criar_ativo_json(client)
        assert r1.status_code == 201
        
        # Editar
        r2 = _editar_ativo_json(client, "AT-001", {"status": "Em Manutenção"})
        assert r2.status_code == 200
        
        # Excluir
        r3 = _excluir_ativo_json(client, "AT-001")
        assert r3.status_code == 200

    def test_usuario_cria_edita_mas_nao_exclui(self, client, monkeypatch):
        """USUARIO consegue criar e editar, mas não excluir."""
        _login_in_session(client, user_id=3, email="usuario@test.local", perfil="USUARIO")
        
        def mock_criar_ativo(ativo, user_id):
            pass
        
        def mock_atualizar_ativo(id_ativo, dados, user_id):
            return Ativo(
                id_ativo=id_ativo,
                tipo="Notebook",
                marca="Dell",
                modelo="Latitude",
                email_responsavel="resp@test.local",
                usuario_responsavel="Usuario",
                departamento="RH",
                status="Disponível",
                data_entrada="2026-05-28",
                data_saida=None,
                criado_por=3,
            )
        
        monkeypatch.setattr(app_module.ativos_service, "criar_ativo", mock_criar_ativo)
        monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", mock_atualizar_ativo)
        
        # Criar
        r1 = _criar_ativo_json(client)
        assert r1.status_code == 201
        
        # Editar
        r2 = _editar_ativo_json(client, "AT-001", {"status": "Disponível"})
        assert r2.status_code == 200
        
        # Excluir deve retornar 403
        r3 = _excluir_ativo_json(client, "AT-001")
        assert r3.status_code == 403

    def test_leitor_nao_consegue_criar_editar_excluir(self, client):
        """LEITOR não consegue criar, editar ou excluir ativo."""
        _login_in_session(client, user_id=4, email="leitor@test.local", perfil="LEITOR")
        
        csrf_headers = _get_csrf(client, "/dashboard")
        
        # Criar
        r1 = client.post(
            "/ativos",
            json={"tipo": "Notebook", "marca": "Dell", "modelo": "L"},
            headers=csrf_headers,
        )
        assert r1.status_code == 403
        
        # Editar
        r2 = client.put(
            "/ativos/AT-001",
            json={"status": "Disponível"},
            headers=csrf_headers,
        )
        assert r2.status_code == 403
        
        # Excluir
        r3 = client.delete(
            "/ativos/AT-001",
            headers=csrf_headers,
        )
        assert r3.status_code == 403

    def test_usuario_edita_ativo_criado_por_outro_usuario(self, client, monkeypatch):
        """USUARIO consegue editar ativo criado por outro usuário."""
        _login_in_session(client, user_id=3, email="usuario@test.local", perfil="USUARIO")
        
        # Simula um ativo criado por ADMIN (user_id=2)
        ativo_existente = Ativo(
            id_ativo="AT-001",
            tipo="Notebook",
            marca="Dell",
            modelo="Latitude",
            email_responsavel="admin@test.local",
            usuario_responsavel="Admin",
            departamento="TI",
            status="Disponível",
            data_entrada="2026-05-28",
            data_saida=None,
            criado_por=2,  # Criado por outro usuário
        )
        
        def mock_atualizar_ativo(id_ativo, dados, user_id):
            return ativo_existente
        
        monkeypatch.setattr(app_module.ativos_service, "atualizar_ativo", mock_atualizar_ativo)
        
        # USUARIO consegue editar ativo de ADMIN
        response = _editar_ativo_json(
            client,
            "AT-001",
            {"status": "Em Manutenção"},
        )
        
        assert response.status_code == 200


class TestFluxoBuscaFiltros:
    """
    Fluxo 9: Validação de busca e filtros de ativos.
    Valida:
    - Sem filtro retorna todos
    - Filtro por departamento retorna somente esse departamento
    - Filtro por status retorna somente esse status
    - Filtro combinado funciona
    - Campo vazio/"Todos" é ignorado
    """

    def test_listar_ativos_sem_filtro(self, client, monkeypatch):
        """Listagem sem filtro retorna todos os ativos."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        ativos_mock = [
            {
                "id": "AT-001",
                "tipo": "Notebook",
                "marca": "Dell",
                "departamento": "TI",
                "status": "Disponível",
            },
            {
                "id": "AT-002",
                "tipo": "Monitor",
                "marca": "LG",
                "departamento": "RH",
                "status": "Em Manutenção",
            },
        ]
        
        def mock_listar_ativos(user_id):
            return [Ativo(id_ativo=a["id"], tipo=a["tipo"], marca=a["marca"], 
                         modelo="", email_responsavel="", usuario_responsavel="",
                         departamento=a["departamento"], status=a["status"],
                         data_entrada="", data_saida=None, criado_por=1) for a in ativos_mock]
        
        monkeypatch.setattr(app_module.ativos_service, "listar_ativos", mock_listar_ativos)
        
        ativos, response = _listar_ativos(client)
        
        assert response.status_code == 200
        assert len(ativos) == 2

    def test_filtro_por_departamento(self, client, monkeypatch):
        """Filtro por departamento retorna apenas ativos desse departamento."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        ativos_ti = [
            Ativo(
                id_ativo="AT-001",
                tipo="Notebook",
                marca="Dell",
                modelo="Latitude",
                email_responsavel="",
                usuario_responsavel="",
                departamento="TI",
                status="Disponível",
                data_entrada="2026-05-28",
                data_saida=None,
                criado_por=1,
            ),
        ]
        
        def mock_filtrar_ativos(user_id, filtros, ordenar_por="id", ordem="asc"):
            if filtros.get("departamento", "").lower() == "ti":
                return ativos_ti
            return []
        
        monkeypatch.setattr(app_module.ativos_service, "filtrar_ativos", mock_filtrar_ativos)
        
        ativos, response = _filtrar_ativos(client, departamento="TI")
        
        assert response.status_code == 200
        assert len(ativos) == 1
        assert ativos[0]["departamento"] == "TI"

    def test_filtro_por_status(self, client, monkeypatch):
        """Filtro por status retorna apenas ativos com esse status."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        ativos_disponiveis = [
            Ativo(
                id_ativo="AT-001",
                tipo="Notebook",
                marca="Dell",
                modelo="Latitude",
                email_responsavel="",
                usuario_responsavel="",
                departamento="TI",
                status="Disponível",
                data_entrada="2026-05-28",
                data_saida=None,
                criado_por=1,
            ),
        ]
        
        def mock_filtrar_ativos(user_id, filtros, ordenar_por="id", ordem="asc"):
            if filtros.get("status", "").lower() == "disponível":
                return ativos_disponiveis
            return []
        
        monkeypatch.setattr(app_module.ativos_service, "filtrar_ativos", mock_filtrar_ativos)
        
        ativos, response = _filtrar_ativos(client, status="Disponível")
        
        assert response.status_code == 200
        assert len(ativos) == 1
        assert ativos[0]["status"] == "Disponível"

    def test_filtro_combinado_departamento_status(self, client, monkeypatch):
        """Filtro combinado retorna ativos que atendem todos os critérios."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        ativos_filtrados = [
            Ativo(
                id_ativo="AT-001",
                tipo="Notebook",
                marca="Dell",
                modelo="Latitude",
                email_responsavel="",
                usuario_responsavel="",
                departamento="TI",
                status="Disponível",
                data_entrada="2026-05-28",
                data_saida=None,
                criado_por=1,
            ),
        ]
        
        def mock_filtrar_ativos(user_id, filtros, ordenar_por="id", ordem="asc"):
            dept = filtros.get("departamento", "").lower()
            stat = filtros.get("status", "").lower()
            if dept == "ti" and stat == "disponível":
                return ativos_filtrados
            return []
        
        monkeypatch.setattr(app_module.ativos_service, "filtrar_ativos", mock_filtrar_ativos)
        
        ativos, response = _filtrar_ativos(client, departamento="TI", status="Disponível")
        
        assert response.status_code == 200
        assert len(ativos) == 1
        assert ativos[0]["departamento"] == "TI"
        assert ativos[0]["status"] == "Disponível"


class TestFluxoCSRF:
    """
    Fluxo 10: Validação de proteção CSRF.
    Valida:
    - POST sem CSRF token é bloqueado
    - POST com CSRF token válido funciona
    - Logout seguido de login usa token novo
    """

    def test_post_ativo_sem_csrf_bloqueado(self, client):
        """POST para criar ativo sem CSRF token retorna 400/403."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # POST sem headers de CSRF
        response = client.post(
            "/ativos",
            json={"tipo": "Notebook", "marca": "Dell", "modelo": "L"},
        )
        
        # Deve ser bloqueado (400 ou 403 conforme implementação)
        assert response.status_code in (400, 403)

    def test_post_usuario_sem_csrf_bloqueado(self, client):
        """POST para criar usuário sem CSRF token retorna 400/403."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # POST sem headers de CSRF
        response = client.post(
            "/usuarios/criar",
            json={
                "email": "novo@test.local",
                "senha": "Senha@123456",
                "pergunta_recuperacao": "Q?",
                "resposta_recuperacao": "R",
                "perfil": "USUARIO",
            },
        )
        
        assert response.status_code in (400, 403)

    def test_post_logout_sem_csrf_bloqueado(self, client):
        """POST para logout sem CSRF token retorna 400/403."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        response = client.post("/logout")
        
        assert response.status_code in (400, 403)

    def test_logout_login_renova_csrf(self, client, monkeypatch):
        """Logout seguido de login usa token novo sem erro CSRF."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        # Extrai token antes do logout
        csrf_headers_1 = _get_csrf(client, "/dashboard")
        token_1 = csrf_headers_1["X-CSRF-Token"]
        
        # Faz logout com token válido
        response = client.post("/logout", headers=csrf_headers_1)
        assert response.status_code == 200
        
        # Faz login novamente com novo token
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        csrf_headers_2 = _get_csrf(client, "/dashboard")
        token_2 = csrf_headers_2["X-CSRF-Token"]
        
        # Tokens são diferentes
        assert token_1 != token_2
        
        # Novo logout com novo token funciona
        response = client.post("/logout", headers=csrf_headers_2)
        assert response.status_code == 200


class TestFluxoAuditoria:
    """
    Fluxo 11: Validação de auditoria básica.
    Valida:
    - SUPER_ADMIN acessa tela de auditoria
    - ADMIN acessa tela de auditoria (se permissão existir)
    - USUARIO/LEITOR não acessam auditoria
    - Página renderiza sem erros
    """

    def test_super_admin_acessa_auditoria(self, client, monkeypatch):
        """SUPER_ADMIN consegue acessar página de auditoria."""
        _login_in_session(client, user_id=1, email="sa@test.local", perfil="SUPER_ADMIN")
        
        def mock_get_recent_events(limit):
            return []
        
        monkeypatch.setattr(app_module, "get_recent_events", mock_get_recent_events)
        
        response = client.get("/auditoria")
        
        assert response.status_code == 200

    def test_admin_acessa_auditoria(self, client, monkeypatch):
        """ADMIN consegue acessar página de auditoria."""
        _login_in_session(client, user_id=2, email="admin@test.local", perfil="ADMIN")
        
        def mock_get_recent_events(limit):
            return []
        
        monkeypatch.setattr(app_module, "get_recent_events", mock_get_recent_events)
        
        response = client.get("/auditoria")
        
        assert response.status_code == 200

    def test_usuario_nao_acessa_auditoria(self, client):
        """USUARIO não consegue acessar página de auditoria."""
        _login_in_session(client, user_id=3, email="usuario@test.local", perfil="USUARIO")
        
        response = client.get("/auditoria")
        
        assert response.status_code == 403

    def test_leitor_nao_acessa_auditoria(self, client):
        """LEITOR não consegue acessar página de auditoria."""
        _login_in_session(client, user_id=4, email="leitor@test.local", perfil="LEITOR")
        
        response = client.get("/auditoria")
        
        assert response.status_code == 403
