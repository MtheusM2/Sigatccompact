from functools import wraps
from flask import session, request, render_template, jsonify


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
