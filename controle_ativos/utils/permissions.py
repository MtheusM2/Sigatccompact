from functools import wraps

from flask import abort, jsonify, render_template, request, session

from controle_ativos.models.usuario import Usuario
from controle_ativos.utils.audit import audit_event


PERFIS_VALIDOS = ("SUPER_ADMIN", "ADMIN", "USUARIO", "LEITOR")

PERMISSOES_POR_PERFIL = {
    "SUPER_ADMIN": {
        "dashboard.acessar",
        "ativos.ver",
        "ativos.criar",
        "ativos.editar",
        "ativos.excluir",
        "auditoria.ver",
        "usuarios.gerenciar",
        "usuarios.alterar_perfil",
    },
    "ADMIN": {
        "dashboard.acessar",
        "ativos.ver",
        "ativos.criar",
        "ativos.editar",
        "ativos.excluir",
        "auditoria.ver",
    },
    "USUARIO": {
        "dashboard.acessar",
        "ativos.ver",
        "ativos.criar",
        "ativos.editar",
    },
    "LEITOR": {
        "dashboard.acessar",
        "ativos.ver",
    },
}


def _valor_usuario(usuario, chave, padrao=None):
    if usuario is None:
        return padrao
    if isinstance(usuario, dict):
        return usuario.get(chave, padrao)
    return getattr(usuario, chave, padrao)


def _perfil_normalizado(usuario) -> str:
    perfil = (_valor_usuario(usuario, "perfil", "USUARIO") or "USUARIO").strip()
    return perfil


def _usuario_da_sessao() -> Usuario | None:
    user_id = session.get("user_id")
    if user_id is None:
        return None

    return Usuario(
        usuario_id=user_id,
        email=session.get("email", ""),
        senha_hash="",
        pergunta_recuperacao="",
        resposta_recuperacao_hash="",
        perfil=session.get("perfil", "USUARIO"),
        ativo=session.get("ativo", True),
        ultimo_login=session.get("ultimo_login"),
        bloqueado_ate=session.get("bloqueado_ate"),
    )


def _carregar_usuario_atual() -> Usuario | None:
    return _usuario_da_sessao()


def has_role(usuario, *roles) -> bool:
    perfil = _perfil_normalizado(usuario)
    if perfil not in PERFIS_VALIDOS:
        return False
    return perfil in roles


def has_permission(usuario, permissao: str) -> bool:
    perfil = _perfil_normalizado(usuario)
    if perfil not in PERFIS_VALIDOS:
        return False
    return permissao in PERMISSOES_POR_PERFIL.get(perfil, set())


def is_super_admin(usuario) -> bool:
    return has_role(usuario, "SUPER_ADMIN")


def can_manage_user(usuario_logado, usuario_alvo) -> bool:
    if not is_super_admin(usuario_logado):
        return False
    return usuario_alvo is not None


def _resposta_sem_autenticacao():
    if request.method == "GET" and (request.path or "").startswith("/dashboard"):
        return render_template("auth/login.html", erro="Faça login para acessar o dashboard.")
    return jsonify({"ok": False, "erro": "Não autenticado."}), 401


def _registrar_acesso_negado(usuario, permissao: str | None = None, roles=None, motivo: str = "forbidden"):
    try:
        audit_event(
            event="access_denied",
            result="denied",
            user_id=_valor_usuario(usuario, "id"),
            email=_valor_usuario(usuario, "email"),
            ip=(request.remote_addr or "") if request else None,
            route=request.path if request else None,
            method=request.method if request else None,
            extra={
                "reason": motivo,
                "required_permission": permissao,
                "required_roles": list(roles or []),
                "perfil": _valor_usuario(usuario, "perfil"),
            },
        )
    except Exception:
        pass


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = _carregar_usuario_atual()
            if usuario is None:
                return _resposta_sem_autenticacao()

            if not has_role(usuario, *roles):
                _registrar_acesso_negado(usuario, roles=roles, motivo="role_not_allowed")
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def permission_required(permissao: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = _carregar_usuario_atual()
            if usuario is None:
                return _resposta_sem_autenticacao()

            if not getattr(usuario, "ativo", True):
                _registrar_acesso_negado(usuario, permissao=permissao, motivo="inactive_user")
                abort(403)

            if not has_permission(usuario, permissao):
                _registrar_acesso_negado(usuario, permissao=permissao, motivo="permission_not_allowed")
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator