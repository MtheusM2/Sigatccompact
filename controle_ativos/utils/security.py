from functools import wraps
import secrets

from flask import session, request, render_template, jsonify


CSRF_SESSION_KEY = "_csrf_token"


def ensure_csrf_token():
    """Garante que a sessão tenha um token CSRF persistente."""
    token = session.get(CSRF_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = token
        session.modified = True
    return token


def csrf_token():
    """Token CSRF exposto aos templates."""
    return ensure_csrf_token()


def _extract_csrf_token():
    token = request.headers.get("X-CSRF-Token") or request.headers.get("X-CSRFToken")
    if token:
        return token

    json_data = request.get_json(silent=True) or {}
    if isinstance(json_data, dict):
        token = json_data.get("csrf_token")
        if token:
            return token

    return request.form.get("csrf_token")


def validate_csrf_request():
    """Valida o token CSRF em requisições mutáveis.

    Retorna None quando a requisição é válida; caso contrário, retorna a
    resposta JSON padronizada com erro 400.
    """
    if request.method not in {"POST", "PUT", "PATCH", "DELETE"}:
        return None

    expected_token = ensure_csrf_token()
    provided_token = _extract_csrf_token()

    if not provided_token or not secrets.compare_digest(provided_token, expected_token):
        return jsonify({"ok": False, "erro": "CSRF inválido."}), 400

    return None


def login_required(func):
    """Decorator central para garantir que o usuário esteja autenticado.

    Comportamento:
    - Se `session['user_id']` existe, permite a chamada da view.
    - Se a rota começa com `/dashboard`, redireciona/renderiza a página de login.
    - Caso contrário (APIs), retorna JSON padronizado de erro 401.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id"):
            return func(*args, **kwargs)

        path = (request.path or "")
        # Páginas do frontend usam /dashboard/* no projeto atual
        if path.startswith("/dashboard"):
            return render_template("auth/login.html", erro="Faça login para acessar o dashboard.")

        # Resposta padrão para APIs
        return jsonify({"ok": False, "erro": "Não autenticado."}), 401

    return wrapper
