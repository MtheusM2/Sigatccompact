import mysql.connector

from controle_ativos.database.connection import cursor_mysql
from controle_ativos.models.usuario import Usuario


PERFIS_EDITAVEIS = {"ADMIN", "USUARIO", "LEITOR"}


class UsuarioErro(Exception):
    """Erro base relacionado à gestão de usuários."""


class UsuarioNaoEncontrado(UsuarioErro):
    """Erro para usuário inexistente."""


class PerfilInvalido(UsuarioErro):
    """Erro para perfil inválido."""


class AlteracaoNaoPermitida(UsuarioErro):
    """Erro para alterações que violam a regra de super admin."""


def _row_para_usuario(row: dict) -> Usuario:
    return Usuario(
        usuario_id=row["id"],
        email=row["email"],
        senha_hash=row.get("senha_hash", ""),
        pergunta_recuperacao=row.get("pergunta_recuperacao", ""),
        resposta_recuperacao_hash=row.get("resposta_recuperacao_hash", ""),
        perfil=row.get("perfil", "USUARIO"),
        ativo=row.get("ativo", True),
        ultimo_login=row.get("ultimo_login"),
        bloqueado_ate=row.get("bloqueado_ate"),
        criado_em=row.get("criado_em"),
        atualizado_em=row.get("atualizado_em"),
    )


class UsuariosService:
    """Serviço simples para listagem e atualização de usuários."""

    def listar_usuarios(self) -> list[Usuario]:
        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                """
                SELECT id, email, senha_hash, pergunta_recuperacao,
                       resposta_recuperacao_hash, perfil, ativo,
                       ultimo_login, bloqueado_ate, criado_em, atualizado_em
                FROM usuarios
                ORDER BY id
                """
            )
            rows = cur.fetchall()

        return [_row_para_usuario(row) for row in rows]

    def buscar_usuario_por_id(self, usuario_id: int) -> Usuario:
        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                """
                SELECT id, email, senha_hash, pergunta_recuperacao,
                       resposta_recuperacao_hash, perfil, ativo,
                       ultimo_login, bloqueado_ate, criado_em, atualizado_em
                FROM usuarios
                WHERE id = %s
                """,
                (usuario_id,),
            )
            row = cur.fetchone()

        if row is None:
            raise UsuarioNaoEncontrado("Usuário não encontrado.")

        return _row_para_usuario(row)

    def atualizar_perfil(self, usuario_id: int, novo_perfil: str, usuario_logado_id: int) -> Usuario:
        novo_perfil_normalizado = (novo_perfil or "").strip().upper()
        if novo_perfil_normalizado not in PERFIS_EDITAVEIS:
            raise PerfilInvalido("Perfil inválido.")

        usuario_atual = self.buscar_usuario_por_id(usuario_id)
        if int(usuario_atual.id) == int(usuario_logado_id) and usuario_atual.perfil == "SUPER_ADMIN" and novo_perfil_normalizado != "SUPER_ADMIN":
            raise AlteracaoNaoPermitida("SUPER_ADMIN não pode remover o próprio perfil SUPER_ADMIN.")

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "UPDATE usuarios SET perfil = %s WHERE id = %s",
                (novo_perfil_normalizado, usuario_id),
            )

            if cur.rowcount == 0:
                raise UsuarioNaoEncontrado("Usuário não encontrado.")

        return self.buscar_usuario_por_id(usuario_id)

    def alternar_status(self, usuario_id: int, ativo: bool, usuario_logado_id: int) -> Usuario:
        usuario_atual = self.buscar_usuario_por_id(usuario_id)
        ativo_normalizado = bool(ativo)

        if int(usuario_atual.id) == int(usuario_logado_id) and usuario_atual.perfil == "SUPER_ADMIN" and not ativo_normalizado:
            raise AlteracaoNaoPermitida("SUPER_ADMIN não pode desativar a própria conta.")

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "UPDATE usuarios SET ativo = %s WHERE id = %s",
                (1 if ativo_normalizado else 0, usuario_id),
            )

            if cur.rowcount == 0:
                raise UsuarioNaoEncontrado("Usuário não encontrado.")

        return self.buscar_usuario_por_id(usuario_id)