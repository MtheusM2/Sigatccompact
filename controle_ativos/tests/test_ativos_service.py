from contextlib import contextmanager

import pytest

from controle_ativos.models.ativos import Ativo
from controle_ativos.services import ativos_service as ativos_module
from controle_ativos.services.ativos_service import (
    AtivoErro,
    AtivoJaExiste,
    AtivoNaoEncontrado,
    AtivosService,
    PermissaoNegada,
)


class _FakeIntegrityError(Exception):
    def __init__(self, errno: int):
        super().__init__("integrity error")
        self.errno = errno


class _FakeCursor:
    def execute(self, sql, params):
        raise _FakeIntegrityError(1062)


class _RecordingCursor:
    def __init__(self, fetchone_results=None, fetchall_result=None, rowcount=1):
        self.fetchone_results = list(fetchone_results or [])
        self.fetchall_result = list(fetchall_result or [])
        self.rowcount = rowcount
        self.executed = []

    def execute(self, sql, params):
        self.executed.append((sql, params))

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None

    def fetchall(self):
        return self.fetchall_result


@contextmanager
def _fake_cursor_mysql(*args, **kwargs):
    yield object(), _FakeCursor()


def _patch_cursor(monkeypatch, cursor):
    """Substitui a conexao real por um cursor fake para testar servicos isolados."""
    @contextmanager
    def _fake_recording_cursor_mysql(*args, **kwargs):
        yield object(), cursor

    monkeypatch.setattr(ativos_module, "cursor_mysql", _fake_recording_cursor_mysql)
    return cursor


def _row_ativo(id_ativo="AT-001", criado_por=1):
    return {
        "id": id_ativo,
        "tipo": "Notebook",
        "marca": "Dell",
        "modelo": "LATITUDE",
        "usuario_responsavel": "Joao Silva",
        "departamento": "TI",
        "status": "Disponível",
        "data_entrada": "2026-05-27",
        "data_saida": None,
        "criado_por": criado_por,
    }


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


def test_criar_ativo_traduz_duplicidade_do_banco(monkeypatch):
    monkeypatch.setattr(ativos_module.mysql.connector, "IntegrityError", _FakeIntegrityError)
    monkeypatch.setattr(ativos_module, "cursor_mysql", _fake_cursor_mysql)

    service = AtivosService()
    ativo = Ativo(
        id_ativo="ATIVO-001",
        tipo="Notebook",
        marca="Dell",
        modelo="Latitude",
        usuario_responsavel="Joao Silva",
        departamento="TI",
        status="Disponível",
        data_entrada="2026-05-27",
        data_saida=None,
        criado_por=1,
    )

    with pytest.raises(AtivoJaExiste):
        service.criar_ativo(ativo, user_id=1)


def test_listar_ativos_retorna_apenas_linhas_do_usuario(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(fetchall_result=[_row_ativo()]))
    service = AtivosService()

    ativos = service.listar_ativos(user_id=1)

    assert len(ativos) == 1
    assert ativos[0].id_ativo == "AT-001"
    assert cursor.executed[0][1] == (1,)


def test_buscar_ativo_rejeita_id_invalido():
    service = AtivosService()

    with pytest.raises(AtivoErro, match="ID"):
        service.buscar_ativo(" ", user_id=1)


def test_buscar_ativo_traduz_nao_encontrado(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[None]))
    service = AtivosService()

    with pytest.raises(AtivoNaoEncontrado):
        service.buscar_ativo("AT-404", user_id=1)


def test_buscar_ativo_traduz_permissao_negada(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[_row_ativo(criado_por=99)]))
    service = AtivosService()

    with pytest.raises(PermissaoNegada):
        service.buscar_ativo("AT-001", user_id=1)


def test_buscar_ativo_retorna_ativo_do_usuario(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(fetchone_results=[_row_ativo()]))
    service = AtivosService()

    ativo = service.buscar_ativo(" AT-001 ", user_id=1)

    assert ativo.id_ativo == "AT-001"
    assert ativo.criado_por == 1
    assert cursor.executed[0][1] == ("AT-001",)


def test_filtrar_ativos_rejeita_campo_de_ordenacao_invalido():
    service = AtivosService()

    with pytest.raises(AtivoErro, match="ordenação|ordena"):
        service.filtrar_ativos(user_id=1, filtros={}, ordenar_por="campo_inexistente")


def test_filtrar_ativos_rejeita_status_invalido():
    service = AtivosService()

    with pytest.raises(AtivoErro, match="Status"):
        service.filtrar_ativos(user_id=1, filtros={"status": "quebrado"})


def test_filtrar_ativos_rejeita_data_invalida():
    service = AtivosService()

    with pytest.raises(AtivoErro, match="Data"):
        service.filtrar_ativos(user_id=1, filtros={"data_entrada_inicial": "27/05/2026"})


def test_filtrar_ativos_monta_filtros_parametrizados(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(fetchall_result=[_row_ativo()]))
    service = AtivosService()

    ativos = service.filtrar_ativos(
        user_id=1,
        filtros={
            "id_ativo": " AT-001 ",
            "usuario_responsavel": "Joao",
            "departamento": "TI",
            "status": "disponível",
            "data_entrada_inicial": "2026-01-01",
            "data_entrada_final": "2026-12-31",
            "data_saida_inicial": "2026-01-01",
            "data_saida_final": "2026-12-31",
        },
        ordenar_por="data_entrada",
        ordem="desc",
    )

    sql, params = cursor.executed[0]
    assert len(ativos) == 1
    assert "ORDER BY data_entrada DESC" in sql
    assert params == (
        1,
        "AT-001",
        "%Joao%",
        "%TI%",
        "Disponível",
        "2026-01-01",
        "2026-12-31",
        "2026-01-01",
        "2026-12-31",
    )


def test_atualizar_ativo_rejeita_dados_invalidos(monkeypatch):
    service = AtivosService()
    monkeypatch.setattr(service, "buscar_ativo", lambda *args, **kwargs: _ativo())

    with pytest.raises(AtivoErro, match="Status"):
        service.atualizar_ativo("AT-001", {"status": "quebrado"}, user_id=1)


def test_atualizar_ativo_traduz_update_sem_linhas(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(rowcount=0))
    service = AtivosService()
    monkeypatch.setattr(service, "buscar_ativo", lambda *args, **kwargs: _ativo())

    with pytest.raises(AtivoNaoEncontrado):
        service.atualizar_ativo("AT-001", {"modelo": "xps"}, user_id=1)


def test_atualizar_ativo_retorna_ativo_padronizado(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(rowcount=1))
    service = AtivosService()
    monkeypatch.setattr(service, "buscar_ativo", lambda *args, **kwargs: _ativo())

    ativo = service.atualizar_ativo(
        "AT-001",
        {"marca": " dell ", "modelo": "xps 13", "status": "em uso"},
        user_id=1,
    )

    assert ativo.marca == "Dell"
    assert ativo.modelo == "XPS 13"
    assert ativo.status == "Em Uso"
    assert cursor.executed[0][1][-2:] == ("AT-001", 1)


def test_remover_ativo_rejeita_id_invalido():
    service = AtivosService()

    with pytest.raises(AtivoErro, match="ID"):
        service.remover_ativo(" ", user_id=1)


def test_remover_ativo_traduz_delete_sem_linhas(monkeypatch):
    _patch_cursor(monkeypatch, _RecordingCursor(rowcount=0))
    service = AtivosService()

    with pytest.raises(AtivoNaoEncontrado):
        service.remover_ativo("AT-404", user_id=1)


def test_remover_ativo_executa_delete_parametrizado(monkeypatch):
    cursor = _patch_cursor(monkeypatch, _RecordingCursor(rowcount=1))
    service = AtivosService()

    service.remover_ativo(" AT-001 ", user_id=1)

    assert cursor.executed[0][1] == ("AT-001", 1)
