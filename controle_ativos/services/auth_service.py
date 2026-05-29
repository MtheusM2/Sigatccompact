import mysql.connector

from controle_ativos.database.connection import cursor_mysql
from controle_ativos.models.usuario import Usuario
from controle_ativos.utils.crypto import gerar_hash, normalizar_resposta_recuperacao, verificar_hash
from controle_ativos.utils.validators import validar_email, validar_senha, validar_texto_obrigatorio


class AuthErro(Exception):
    """Erro base de autenticação."""


class UsuarioJaExiste(AuthErro):
    """Erro para usuário duplicado."""


class UsuarioNaoEncontrado(AuthErro):
    """Erro para usuário inexistente."""


class CredenciaisInvalidas(AuthErro):
    """Erro para login inválido."""


class RecuperacaoInvalida(AuthErro):
    """Erro para recuperação inválida."""


class UsuarioInativo(AuthErro):
    """Erro para usuário inativo ou bloqueado."""


def _normalizar_email(email: str) -> str:
    """
    Normaliza o e-mail para comparação e armazenamento.
    """
    return (email or "").strip().lower()


class AuthService:
    """
    Serviço responsável por cadastro, autenticação e recuperação de senha.
    """

    def registrar_usuario(self, email: str, senha: str, pergunta: str, resposta: str) -> int:
        email_norm = _normalizar_email(email)

        if not validar_email(email_norm):
            raise AuthErro("E-mail inválido.")

        ok, msg = validar_senha(senha)
        if not ok:
            raise AuthErro(msg)

        ok, msg = validar_texto_obrigatorio(pergunta, "pergunta de recuperação", 255)
        if not ok:
            raise AuthErro(msg)

        ok, msg = validar_texto_obrigatorio(resposta, "resposta de recuperação", 255)
        if not ok:
            raise AuthErro(msg)

        senha_hash = gerar_hash(senha)
        resposta_hash = gerar_hash(normalizar_resposta_recuperacao(resposta))

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "SELECT id FROM usuarios WHERE email = %s",
                (email_norm,)
            )
            if cur.fetchone() is not None:
                raise UsuarioJaExiste("Já existe um usuário cadastrado com este e-mail.")

            cur.execute(
                """
                INSERT INTO usuarios (email, senha_hash, pergunta_recuperacao, resposta_recuperacao_hash)
                VALUES (%s, %s, %s, %s)
                """,
                (email_norm, senha_hash, pergunta.strip(), resposta_hash)
            )

            return int(cur.lastrowid)

    def autenticar(self, email: str, senha: str) -> Usuario:
        email_norm = _normalizar_email(email)

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "SELECT * FROM usuarios WHERE email = %s",
                (email_norm,)
            )
            row = cur.fetchone()

        if row is None:
            raise UsuarioNaoEncontrado("Usuário não encontrado.")

        if not verificar_hash(senha, row["senha_hash"]):
            raise CredenciaisInvalidas("E-mail ou senha inválidos.")

        if not bool(row.get("ativo", 1)):
            raise UsuarioInativo("Usuário inativo.")

        if row.get("bloqueado_ate"):
            raise UsuarioInativo("Usuário bloqueado temporariamente.")

        return Usuario(
            usuario_id=row["id"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            pergunta_recuperacao=row["pergunta_recuperacao"],
            resposta_recuperacao_hash=row["resposta_recuperacao_hash"],
            perfil=row.get("perfil", "USUARIO"),
            ativo=row.get("ativo", True),
            ultimo_login=row.get("ultimo_login"),
            bloqueado_ate=row.get("bloqueado_ate"),
            criado_em=row.get("criado_em"),
            atualizado_em=row.get("atualizado_em"),
        )

    def obter_usuario_por_id(self, usuario_id: int) -> Usuario | None:
        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
            row = cur.fetchone()

        if row is None:
            return None

        return Usuario(
            usuario_id=row["id"],
            email=row["email"],
            senha_hash=row["senha_hash"],
            pergunta_recuperacao=row["pergunta_recuperacao"],
            resposta_recuperacao_hash=row["resposta_recuperacao_hash"],
            perfil=row.get("perfil", "USUARIO"),
            ativo=row.get("ativo", True),
            ultimo_login=row.get("ultimo_login"),
            bloqueado_ate=row.get("bloqueado_ate"),
            criado_em=row.get("criado_em"),
            atualizado_em=row.get("atualizado_em"),
        )

    def registrar_ultimo_login(self, usuario_id: int) -> None:
        try:
            with cursor_mysql(dictionary=True) as (_conn, cur):
                cur.execute(
                    "UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP WHERE id = %s",
                    (usuario_id,),
                )
        except mysql.connector.Error as erro:
            if getattr(erro, "errno", None) == 1054:
                return
            raise

    def obter_pergunta_recuperacao(self, email: str) -> str:
        email_norm = _normalizar_email(email)

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "SELECT pergunta_recuperacao FROM usuarios WHERE email = %s",
                (email_norm,)
            )
            row = cur.fetchone()

        if row is None:
            raise UsuarioNaoEncontrado("Usuário não encontrado.")

        return row["pergunta_recuperacao"]

    def redefinir_senha(self, email: str, resposta: str, nova_senha: str) -> None:
        email_norm = _normalizar_email(email)

        ok, msg = validar_senha(nova_senha)
        if not ok:
            raise AuthErro(msg)

        with cursor_mysql(dictionary=True) as (_conn, cur):
            cur.execute(
                "SELECT id, resposta_recuperacao_hash FROM usuarios WHERE email = %s",
                (email_norm,)
            )
            row = cur.fetchone()

            if row is None:
                raise UsuarioNaoEncontrado("Usuário não encontrado.")

            if not verificar_hash(
                normalizar_resposta_recuperacao(resposta),
                row["resposta_recuperacao_hash"]
            ):
                raise RecuperacaoInvalida("Resposta de recuperação incorreta.")

            nova_hash = gerar_hash(nova_senha)

            cur.execute(
                "UPDATE usuarios SET senha_hash = %s WHERE id = %s",
                (nova_hash, row["id"])
            )