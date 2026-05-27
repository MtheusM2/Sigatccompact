# Importa funções para ler variáveis de ambiente.
import os
from threading import Lock

# Importa utilitário para trabalhar com caminhos de forma segura.
from pathlib import Path

# Importa o decorador para criar context managers com "with".
from contextlib import contextmanager

from mysql.connector.pooling import MySQLConnectionPool

# Importa o carregador de variáveis de ambiente do arquivo .env.
from dotenv import load_dotenv


# =========================
# CARREGAMENTO DO ARQUIVO .ENV
# =========================
# Descobre a raiz do repositório a partir deste arquivo:
# controle_ativos/database/connection.py -> sobe dois níveis até controle_ativos
# e mais um nível até a raiz do projeto, onde o .env local deve ficar.
BASE_DIR = Path(__file__).resolve().parents[2]

# Monta o caminho absoluto do arquivo .env.
ENV_FILE = BASE_DIR / ".env"

# Carrega o arquivo .env de forma explícita.
# Isso evita depender do diretório atual do terminal.
load_dotenv(dotenv_path=ENV_FILE)

_POOL_LOCK = Lock()
_CONNECTION_POOLS = {}


def _db_config(com_database: bool = True) -> dict:
    """
    Monta o dicionário de configuração da conexão MySQL.

    Parâmetros:
    - com_database:
      Se True, inclui o nome do banco na conexão.
      Se False, conecta apenas ao servidor MySQL.

    Retorno:
    - dicionário com os parâmetros da conexão.
    """
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "controle_ativos")

    cfg = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
    }

    if com_database:
        cfg["database"] = database

    return cfg


def _obter_pool(com_database: bool = True):
    """
    Retorna um pool de conexões MySQL reutilizável.
    """
    chave = "com_db" if com_database else "sem_db"
    pool = _CONNECTION_POOLS.get(chave)

    if pool is not None:
        return pool

    with _POOL_LOCK:
        pool = _CONNECTION_POOLS.get(chave)
        if pool is None:
            cfg = _db_config(com_database=com_database)
            pool_nome = os.getenv("DB_POOL_NAME", "controle_ativos")
            pool_tamanho = int(os.getenv("DB_POOL_SIZE", "5"))

            pool = MySQLConnectionPool(
                pool_name=f"{pool_nome}_{chave}",
                pool_size=pool_tamanho,
                **cfg
            )
            _CONNECTION_POOLS[chave] = pool

    return pool


@contextmanager
def conexao_mysql(com_database: bool = True):
    """
    Abre uma conexão MySQL e controla commit/rollback automaticamente.
    """
    conn = None

    try:
        conn = _obter_pool(com_database=com_database).get_connection()
        conn.autocommit = False
        yield conn
        conn.commit()

    except Exception:
        if conn is not None and conn.is_connected():
            conn.rollback()
        raise

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


@contextmanager
def cursor_mysql(dictionary: bool = True):
    """
    Abre conexão e cursor padronizados para uso no projeto.
    """
    with conexao_mysql(com_database=True) as conn:
        cur = conn.cursor(dictionary=dictionary)

        try:
            yield conn, cur
        finally:
            cur.close()
