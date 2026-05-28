from dataclasses import dataclass
from functools import wraps
import secrets
import time

from flask import session, request, render_template, jsonify


CSRF_SESSION_KEY = "_csrf_token"
AUTH_RATE_LIMIT_MAX_FAILURES = 5
AUTH_RATE_LIMIT_WINDOW_SECONDS = 5 * 60
AUTH_RATE_LIMIT_BLOCK_SECONDS = 10 * 60
AUTH_RATE_LIMIT_MESSAGE = "Muitas tentativas. Tente novamente mais tarde."


@dataclass
class _AuthRateLimitState:
    failures: int = 0
    window_start: float = 0.0
    blocked_until: float = 0.0


_AUTH_RATE_LIMIT_STATE: dict[tuple[str, ...], _AuthRateLimitState] = {}


def normalize_email_for_rate_limit(email: str | None) -> str:
    return (email or "").strip().lower()


def client_ip() -> str:
    return (request.remote_addr or "").strip() or "unknown"


def _auth_rate_limit_keys(scope: str, ip: str, email: str | None = None):
    ip_normalized = (ip or "").strip() or "unknown"
    keys = [(scope, ip_normalized)]

    email_normalized = normalize_email_for_rate_limit(email)
    if email_normalized:
        keys.append((scope, ip_normalized, email_normalized))

    return keys


def _auth_rate_limit_state(key: tuple[str, ...], now: float, create: bool = False):
    state = _AUTH_RATE_LIMIT_STATE.get(key)
    if state is None and create:
        state = _AuthRateLimitState(window_start=now)
        _AUTH_RATE_LIMIT_STATE[key] = state
    return state


def _purge_expired_auth_rate_limit_state(key: tuple[str, ...], state: _AuthRateLimitState, now: float):
    if state.blocked_until <= now and now - state.window_start > AUTH_RATE_LIMIT_WINDOW_SECONDS:
        _AUTH_RATE_LIMIT_STATE.pop(key, None)


def is_auth_rate_limited(scope: str, ip: str, email: str | None = None) -> bool:
    now = time.monotonic()

    for key in _auth_rate_limit_keys(scope, ip, email):
        state = _AUTH_RATE_LIMIT_STATE.get(key)
        if state is None:
            continue

        if state.blocked_until > now:
            return True

        _purge_expired_auth_rate_limit_state(key, state, now)

    return False


def register_auth_rate_limit_failure(scope: str, ip: str, email: str | None = None):
    now = time.monotonic()

    for key in _auth_rate_limit_keys(scope, ip, email):
        state = _auth_rate_limit_state(key, now, create=True)

        if now - state.window_start > AUTH_RATE_LIMIT_WINDOW_SECONDS:
            state.failures = 0
            state.window_start = now
            state.blocked_until = 0.0

        if state.blocked_until > now:
            continue

        state.failures += 1
        if state.failures >= AUTH_RATE_LIMIT_MAX_FAILURES:
            state.blocked_until = now + AUTH_RATE_LIMIT_BLOCK_SECONDS


def clear_auth_rate_limit(scope: str, ip: str, email: str | None = None):
    for key in _auth_rate_limit_keys(scope, ip, email):
        _AUTH_RATE_LIMIT_STATE.pop(key, None)


def reset_auth_rate_limits():
    _AUTH_RATE_LIMIT_STATE.clear()


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
