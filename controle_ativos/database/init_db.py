import sys
from pathlib import Path

# Garante imports absolutos quando o script é executado diretamente.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from controle_ativos.database.connection import conexao_mysql


def _coluna(cur, tabela: str, coluna: str):
    """
    Retorna metadados de uma coluna no banco atual, se ela existir.
    """
    cur.execute(
        """
        SELECT COLUMN_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
          AND COLUMN_NAME = %s
        """,
        (tabela, coluna),
    )
    return cur.fetchone()


def _permitir_null_se_existir(cur, tabela: str, coluna: str) -> None:
    """
    Remove obrigatoriedade de colunas legadas sem apagar dados.

    Alguns bancos locais podem ter sido criados com `empresa_id` ou `nome`
    obrigatórios. O fluxo atual não envia esses campos, então eles precisam
    aceitar NULL enquanto a evolução multi-tenant não for implementada.
    """
    row = _coluna(cur, tabela, coluna)
    if row is None:
        return

    column_type, is_nullable = row
    if is_nullable == "NO":
        cur.execute(f"ALTER TABLE {tabela} MODIFY COLUMN {coluna} {column_type} NULL")


def _compatibilizar_schema_legado(cur) -> None:
    """
    Ajusta bancos já existentes para não depender de campos fora do fluxo atual.
    """
    _permitir_null_se_existir(cur, "usuarios", "empresa_id")
    _permitir_null_se_existir(cur, "ativos", "empresa_id")
    _permitir_null_se_existir(cur, "usuarios", "nome")


def _executar_sql_texto(cur, sql_texto: str) -> None:
    comandos = [cmd.strip() for cmd in sql_texto.split(";") if cmd.strip()]
    for comando in comandos:
        cur.execute(comando)


def _aplicar_migracoes(cur) -> None:
    migrations_dir = Path(__file__).with_name("migrations")
    if not migrations_dir.exists():
        return

    for migration_path in sorted(migrations_dir.glob("*.sql")):
        sql = migration_path.read_text(encoding="utf-8")
        _executar_sql_texto(cur, sql)


def inicializar_banco():
    schema_path = Path(__file__).with_name("schema.sql")
    sql = schema_path.read_text(encoding="utf-8")

    with conexao_mysql(com_database=False) as conn:
        cur = conn.cursor()
        try:
            _executar_sql_texto(cur, sql)
            _compatibilizar_schema_legado(cur)
            _aplicar_migracoes(cur)
            print("Banco e tabelas criados com sucesso.")
        except Exception as e:
            print("Erro ao criar banco/tabelas:")
            print(e)
            raise
        finally:
            cur.close()


if __name__ == "__main__":
    inicializar_banco()
