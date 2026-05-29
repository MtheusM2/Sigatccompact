from contextlib import contextmanager

import pytest

from controle_ativos.services import usuarios_service as usuarios_module
from controle_ativos.services.usuarios_service import (
    AlteracaoNaoPermitida,
    PerfilInvalido,
    UsuarioNaoEncontrado,
    UsuariosService,
)


class _RecordingCursor:
    def __init__(self, fetchone_results=None, fetchall_result=None, rowcount=1):
        self.fetchone_results = list(fetchone_results or [])
        self.fetchall_result = list(fetchall_result or [])
        self.rowcount = rowcount
        self.executed = []

    def execute(self, sql, params=()):
        self.executed.append((sql, params))

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None

    def fetchall(self):
        return self.fetchall_result


def _patch_cursor(monkeypatch, cursor):
    @contextmanager
    def _fake_cursor_mysql(*_args, **_kwargs):
        yield object(), cursor

    monkeypatch.setattr(usuarios_module, "cursor_mysql", _fake_cursor_mysql)
    return cursor


def _row_usuario(usuario_id=1, email="tester@example.com", perfil="USUARIO", ativo=1):
    return {
        "id": usuario_id,
        "email": email,
        "senha_hash": "hash",
        "pergunta_recuperacao": "Pergunta?",
        "resposta_recuperacao_hash": "resp-hash",
        "perfil": perfil,
        "ativo": ativo,
        "ultimo_login": None,
        "bloqueado_ate": None,
        "criado_em": None,
        "atualizado_em": None,
    }


def test_listar_usuarios_retorna_lista_global(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(fetchall_result=[_row_usuario(1), _row_usuario(2, email="outro@example.com", perfil="ADMIN")]))
    service = UsuariosService()

    usuarios = service.listar_usuarios()

    assert [usuario.email for usuario in usuarios] == ["tester@example.com", "outro@example.com"]
    assert cursor.executed[0][1] == ()


def test_atualizar_perfil_de_outro_usuario(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[_row_usuario(2, perfil="LEITOR"), _row_usuario(2, perfil="ADMIN")]))
    service = UsuariosService()

    usuario = service.atualizar_perfil(2, "ADMIN", usuario_logado_id=1)

    assert usuario.perfil == "ADMIN"
    assert cursor.executed[0][1] == (2,)
    assert cursor.executed[1][1] == ("ADMIN", 2)


def test_alternar_status_de_outro_usuario(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[_row_usuario(2, ativo=1), _row_usuario(2, ativo=0)]))
    service = UsuariosService()

    usuario = service.alternar_status(2, False, usuario_logado_id=1)

    assert usuario.ativo is False
    assert cursor.executed[1][1] == (0, 2)


def test_super_admin_nao_pode_rebaixar_a_si_mesmo(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[_row_usuario(1, perfil="SUPER_ADMIN")]))
    service = UsuariosService()

    with pytest.raises(AlteracaoNaoPermitida):
        service.atualizar_perfil(1, "ADMIN", usuario_logado_id=1)


def test_super_admin_nao_pode_desativar_a_si_mesmo(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[_row_usuario(1, perfil="SUPER_ADMIN")]))
    service = UsuariosService()

    with pytest.raises(AlteracaoNaoPermitida):
        service.alternar_status(1, False, usuario_logado_id=1)


def test_atualizar_perfil_rejeita_perfil_invalido():
    service = UsuariosService()

    with pytest.raises(PerfilInvalido):
        service.atualizar_perfil(2, "GUEST", usuario_logado_id=1)


def test_buscar_usuario_por_id_traduz_nao_encontrado(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[None]))
    service = UsuariosService()

    with pytest.raises(UsuarioNaoEncontrado):
        service.buscar_usuario_por_id(99)