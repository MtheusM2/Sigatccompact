from contextlib import contextmanager

import pytest

from controle_ativos.models.usuario import Usuario
from controle_ativos.services import auth_service as auth_module
from controle_ativos.services.auth_service import (
    AuthErro,
    AuthService,
    CredenciaisInvalidas,
    RecuperacaoInvalida,
    UsuarioJaExiste,
    UsuarioNaoEncontrado,
)


class _FakeCursor:
    def __init__(self, fetchone_results=None, lastrowid=10):
        self.fetchone_results = list(fetchone_results or [])
        self.lastrowid = lastrowid
        self.executed = []

    def execute(self, sql, params):
        self.executed.append((sql, params))

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None


def _patch_cursor(monkeypatch, cursor):
    """Substitui o cursor MySQL por um fake controlado pelo teste."""
    @contextmanager
    def _fake_cursor_mysql(*args, **kwargs):
        yield object(), cursor

    monkeypatch.setattr(auth_module, "cursor_mysql", _fake_cursor_mysql)
    return cursor


def test_registrar_usuario_rejeita_email_invalido():
    service = AuthService()

    with pytest.raises(AuthErro, match="E-mail"):
        service.registrar_usuario("email-invalido", "Senha@12345", "Pergunta?", "Resposta")


def test_registrar_usuario_rejeita_senha_invalida():
    service = AuthService()

    with pytest.raises(AuthErro, match="senha"):
        service.registrar_usuario("tester@example.com", "curta", "Pergunta?", "Resposta")


def test_registrar_usuario_rejeita_pergunta_vazia():
    service = AuthService()

    with pytest.raises(AuthErro, match="pergunta"):
        service.registrar_usuario("tester@example.com", "Senha@12345", "   ", "Resposta")


def test_registrar_usuario_traduz_email_duplicado(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[{"id": 1}]))
    service = AuthService()

    with pytest.raises(UsuarioJaExiste):
        service.registrar_usuario("Tester@Example.com", "Senha@12345", "Pergunta?", "Resposta")

    assert cursor.executed[0][1] == ("tester@example.com",)


def test_registrar_usuario_insere_email_normalizado(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[None], lastrowid=42))
    monkeypatch.setattr(auth_module, "gerar_hash", lambda valor: f"hash::{valor}")
    service = AuthService()

    user_id = service.registrar_usuario(
        " Tester@Example.com ",
        "Senha@12345",
        " Pergunta? ",
        " Resposta Azul ",
    )

    assert user_id == 42
    assert cursor.executed[0][1] == ("tester@example.com",)
    assert cursor.executed[1][1][0] == "tester@example.com"
    assert cursor.executed[1][1][2] == "Pergunta?"


def test_autenticar_rejeita_usuario_inexistente(monkeypatch):
    _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[None]))
    service = AuthService()

    with pytest.raises(UsuarioNaoEncontrado):
        service.autenticar("tester@example.com", "Senha@12345")


def test_autenticar_rejeita_senha_incorreta(monkeypatch):
    row = {
        "id": 1,
        "email": "tester@example.com",
        "senha_hash": "hash",
        "pergunta_recuperacao": "Pergunta?",
        "resposta_recuperacao_hash": "resp-hash",
    }
    _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[row]))
    monkeypatch.setattr(auth_module, "verificar_hash", lambda valor, hash_salvo: False)
    service = AuthService()

    with pytest.raises(CredenciaisInvalidas):
        service.autenticar("tester@example.com", "senha-errada")


def test_autenticar_retorna_usuario_quando_credenciais_validas(monkeypatch):
    row = {
        "id": 7,
        "email": "tester@example.com",
        "senha_hash": "hash",
        "pergunta_recuperacao": "Pergunta?",
        "resposta_recuperacao_hash": "resp-hash",
    }
    _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[row]))
    monkeypatch.setattr(auth_module, "verificar_hash", lambda valor, hash_salvo: True)
    service = AuthService()

    usuario = service.autenticar("tester@example.com", "Senha@12345")

    assert isinstance(usuario, Usuario)
    assert usuario.id == 7
    assert usuario.email == "tester@example.com"


def test_obter_pergunta_recuperacao_rejeita_usuario_inexistente(monkeypatch):
    _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[None]))
    service = AuthService()

    with pytest.raises(UsuarioNaoEncontrado):
        service.obter_pergunta_recuperacao("tester@example.com")


def test_obter_pergunta_recuperacao_retorna_pergunta(monkeypatch):
    _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[{"pergunta_recuperacao": "Cor favorita?"}]))
    service = AuthService()

    assert service.obter_pergunta_recuperacao("tester@example.com") == "Cor favorita?"


def test_redefinir_senha_rejeita_nova_senha_invalida():
    service = AuthService()

    with pytest.raises(AuthErro, match="senha"):
        service.redefinir_senha("tester@example.com", "azul", "curta")


def test_redefinir_senha_rejeita_usuario_inexistente(monkeypatch):
    _patch_cursor(monkeypatch, _FakeCursor(fetchone_results=[None]))
    service = AuthService()

    with pytest.raises(UsuarioNaoEncontrado):
        service.redefinir_senha("tester@example.com", "azul", "Senha@12345")


def test_redefinir_senha_rejeita_resposta_incorreta(monkeypatch):
    _patch_cursor(
        monkeypatch,
        _FakeCursor(fetchone_results=[{"id": 1, "resposta_recuperacao_hash": "resp-hash"}]),
    )
    monkeypatch.setattr(auth_module, "verificar_hash", lambda valor, hash_salvo: False)
    service = AuthService()

    with pytest.raises(RecuperacaoInvalida):
        service.redefinir_senha("tester@example.com", "errada", "Senha@12345")


def test_redefinir_senha_atualiza_hash_quando_resposta_correta(monkeypatch):
    cursor = _patch_cursor(
        monkeypatch,
        _FakeCursor(fetchone_results=[{"id": 5, "resposta_recuperacao_hash": "resp-hash"}]),
    )
    monkeypatch.setattr(auth_module, "verificar_hash", lambda valor, hash_salvo: True)
    monkeypatch.setattr(auth_module, "gerar_hash", lambda valor: f"hash::{valor}")
    service = AuthService()

    service.redefinir_senha("tester@example.com", "azul", "Senha@12345")

    assert cursor.executed[-1][1] == ("hash::Senha@12345", 5)
