import importlib
import os
import time
import uuid

from mysql.connector import Error as MySQLError

import pytest

from controle_ativos.database.connection import cursor_mysql
from controle_ativos.models.ativos import Ativo
from controle_ativos.services.ativos_service import AtivosService


if os.getenv("RUN_PERF_TESTS") != "1":
    pytest.skip("Benchmarks desativados. Defina RUN_PERF_TESTS=1 para executar.", allow_module_level=True)


BENCHMARK_PREFIX = f"B{uuid.uuid4().hex[:8].upper()}"
BENCHMARK_EMAIL = f"{BENCHMARK_PREFIX.lower()}@example.com"
BENCHMARK_PASSWORD = "Senha@12345"
BENCHMARK_COUNT = int(os.getenv("PERF_INSERTS", "50"))
BENCHMARK_ROUTE_COUNT = int(os.getenv("PERF_ROUTE_INSERTS", "25"))


def _garantir_banco_disponivel() -> None:
    try:
        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute("SELECT 1")
            cur.fetchone()
    except MySQLError as erro:
        pytest.skip(f"Benchmark ignorado: MySQL local indisponível ou credenciais inválidas ({erro})")


def _garantir_schema_compativel() -> None:
    with cursor_mysql(dictionary=True) as (_conn, cur):
        cur.execute(
            """
            SELECT IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'ativos'
              AND COLUMN_NAME = 'empresa_id'
            """
        )
        row = cur.fetchone()

    if row and row["IS_NULLABLE"] == "NO" and row["COLUMN_DEFAULT"] is None:
        pytest.skip("Benchmark ignorado: o schema local ainda exige empresa_id em ativos.")


def _obter_contexto_benchmark() -> int:
    with cursor_mysql(dictionary=True) as (_conn, cur):
        cur.execute("SELECT id FROM usuarios ORDER BY id LIMIT 1")
        row = cur.fetchone()

    if row is None:
        pytest.skip("Benchmark ignorado: não há usuários cadastrados no banco local.")

    return int(row["id"])


def _novo_ativo(prefix: str, indice: int, user_id: int) -> Ativo:
    return Ativo(
        id_ativo=f"{prefix}-{indice:05d}",
        tipo="Notebook",
        marca="Dell",
        modelo="Latitude",
        usuario_responsavel="Joao Silva",
        departamento="TI",
        status="Disponível",
        data_entrada="2026-05-27",
        data_saida=None,
        criado_por=user_id,
    )


def _limpar_dados_benchmark(user_id: int, prefix: str) -> None:
    with cursor_mysql(dictionary=True) as (_conn, cur):
        cur.execute(
            "DELETE FROM ativos WHERE criado_por = %s AND id LIKE %s",
            (user_id, f"{prefix}%"),
        )


def _medir_throughput_servico(user_id: int, prefix: str, quantidade: int) -> float:
    service = AtivosService()
    inicio = time.perf_counter()

    for indice in range(quantidade):
        ativo = _novo_ativo(prefix, indice, user_id)
        service.criar_ativo(ativo, user_id=user_id)

    elapsed = time.perf_counter() - inicio
    return quantidade / elapsed if elapsed > 0 else float("inf")


def _medir_throughput_rota(prefix: str, quantidade: int) -> float:
    os.environ.setdefault("FLASK_SECRET_KEY", "perf-secret-key")
    app_module = importlib.import_module("controle_ativos.web.app")
    client = app_module.app.test_client()

    user_id = _obter_contexto_benchmark()

    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["email"] = "benchmark@local"

    inicio = time.perf_counter()

    for indice in range(quantidade):
        ativo = _novo_ativo(prefix, indice, user_id)
        response = client.post(
            "/ativos",
            json={
                "id": ativo.id_ativo,
                "tipo": ativo.tipo,
                "marca": ativo.marca,
                "modelo": ativo.modelo,
                "usuario_responsavel": ativo.usuario_responsavel,
                "departamento": ativo.departamento,
                "status": ativo.status,
                "data_entrada": ativo.data_entrada,
                "data_saida": ativo.data_saida,
            },
        )
        assert response.status_code == 201, response.get_json()

    elapsed = time.perf_counter() - inicio
    return quantidade / elapsed if elapsed > 0 else float("inf")


def test_throughput_inserts_no_servico():
    _garantir_banco_disponivel()
    _garantir_schema_compativel()
    user_id = _obter_contexto_benchmark()
    prefix = f"SRV{BENCHMARK_PREFIX}"

    try:
        throughput = _medir_throughput_servico(user_id, prefix, BENCHMARK_COUNT)
        print(
            f"[perf] service inserts/sec={throughput:.2f} "
            f"count={BENCHMARK_COUNT} prefix={prefix}"
        )
        assert throughput > 0
    finally:
        _limpar_dados_benchmark(user_id, prefix)


def test_throughput_inserts_na_rota_flask():
    _garantir_banco_disponivel()
    _garantir_schema_compativel()
    user_id = _obter_contexto_benchmark()
    prefix = f"API{BENCHMARK_PREFIX}"

    try:
        throughput = _medir_throughput_rota(prefix, BENCHMARK_ROUTE_COUNT)
        print(
            f"[perf] route inserts/sec={throughput:.2f} "
            f"count={BENCHMARK_ROUTE_COUNT} prefix={prefix}"
        )
        assert throughput > 0
    finally:
        _limpar_dados_benchmark(user_id, prefix)
