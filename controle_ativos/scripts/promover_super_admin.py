import argparse
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from controle_ativos.database.connection import cursor_mysql


def _obter_email(args) -> str | None:
    return args.email or os.getenv("SUPER_ADMIN_EMAIL") or os.getenv("PROMOVER_SUPER_ADMIN_EMAIL")


def promover_super_admin(email: str) -> int:
    email_norm = (email or "").strip().lower()
    if not email_norm:
        raise ValueError("Informe um e-mail valido para promover o SUPER_ADMIN.")

    with cursor_mysql(dictionary=True) as (_conn, cur):
        cur.execute("SELECT id, email FROM usuarios WHERE email = %s", (email_norm,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"Usuario nao encontrado para o e-mail {email_norm}.")

        cur.execute(
            "UPDATE usuarios SET perfil = 'SUPER_ADMIN' WHERE id = %s",
            (row["id"],),
        )

    return int(row["id"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Promove um usuario existente para SUPER_ADMIN.")
    parser.add_argument("--email", help="E-mail do usuario que sera promovido.")
    args = parser.parse_args()

    email = _obter_email(args)
    if not email:
        print("ERRO: informe --email ou a variavel de ambiente SUPER_ADMIN_EMAIL.")
        return 1

    try:
        usuario_id = promover_super_admin(email)
    except LookupError as erro:
        print(f"ERRO: {erro}")
        return 1
    except Exception as erro:
        print(f"ERRO inesperado ao promover SUPER_ADMIN: {erro}")
        return 1

    print(f"Usuario {email.strip().lower()} promovido para SUPER_ADMIN (id={usuario_id}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())