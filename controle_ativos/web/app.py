# Importa os recursos principais do Flask para criar a API,
# ler JSON da requisição, responder JSON e controlar sessão.
import os
import sys
import secrets
from pathlib import Path
import mysql.connector
from flask import Flask, request, jsonify, session
from flask import render_template
from datetime import timedelta

# Garante imports absolutos quando o app é importado ou executado de dentro da pasta web.
# O import `controle_ativos...` precisa da raiz do repositório no sys.path,
# não da própria pasta `controle_ativos`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Importa os helpers de segurança centralizados (depois de garantir sys.path)
from controle_ativos.utils.security import (
    login_required,
    csrf_token,
    validate_csrf_request,
)

# Importa o serviço de autenticação e suas exceções específicas.
from controle_ativos.services.auth_service import (
    AuthService,
    AuthErro,
    UsuarioJaExiste,
    UsuarioNaoEncontrado,
    CredenciaisInvalidas,
    RecuperacaoInvalida,
)

# Importa o serviço de ativos e suas exceções específicas.
from controle_ativos.services.ativos_service import (
    AtivosService,
    AtivoErro,
    AtivoJaExiste,
    AtivoNaoEncontrado,
    PermissaoNegada,
)

# Importa o model de domínio do ativo.
from controle_ativos.models.ativos import Ativo

# Cria a aplicação Flask.
app = Flask(__name__)

# Define a chave de sessão a partir de variável de ambiente.
# A aplicação não inicia sem uma chave explícita para evitar sessão previsível.
secret_key = os.getenv("FLASK_SECRET_KEY")
if not secret_key:
    raise RuntimeError("Defina FLASK_SECRET_KEY no ambiente para iniciar a aplicação Flask.")
app.secret_key = secret_key

# Configurações explícitas de cookies de sessão (Fase 1.1 de segurança)
debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
app.config.update(
    {
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        # Em produção/HTTPS habilitar Secure; durante desenvolvimento costuma ser False
        "SESSION_COOKIE_SECURE": not debug_mode,
        "PERMANENT_SESSION_LIFETIME": timedelta(minutes=30),
    }
)


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": csrf_token}


@app.before_request
def protect_csrf():
    csrf_error = validate_csrf_request()
    if csrf_error is not None:
        return csrf_error


@app.get("/")
def home():
    return render_template("auth/login.html")


@app.get("/register")
def registro_form():
    """Retorna a página de cadastro."""
    return render_template("auth/register.html")


@app.get("/recovery")
def recovery_form():
    """Retorna a página de recuperação de senha."""
    return render_template("auth/recovery.html")


@app.get("/dashboard")
@login_required
def dashboard_page():
    """Retorna a página do dashboard, que lista os ativos."""
    return _render_pagina_sistema("dashboard.html")


def _render_pagina_sistema(template_name: str):
    if "user_id" not in session:
        return render_template("auth/login.html", erro="Faça login para acessar o dashboard.")
    return render_template(template_name)


@app.get("/dashboard/status")
@login_required
def dashboard_status():
    return _render_pagina_sistema("sistema/status_ativos.html")


@app.get("/dashboard/buscar")
@login_required
def dashboard_buscar():
    return _render_pagina_sistema("sistema/buscar_ativos.html")


@app.get("/dashboard/cadastrar")
@login_required
def dashboard_cadastrar():
    return _render_pagina_sistema("sistema/cadastrar_ativos.html")


@app.get("/dashboard/editar")
@login_required
def dashboard_editar():
    return _render_pagina_sistema("sistema/editar_ativos.html")


@app.get("/dashboard/excluir")
@login_required
def dashboard_excluir():
    return _render_pagina_sistema("sistema/excluir_ativos.html")


auth_service = AuthService()
ativos_service = AtivosService()


def usuario_logado_id():
    """
    Retorna o ID do usuário atualmente autenticado na sessão.
    """
    return session.get("user_id")


def _erro_json(mensagem: str, status_code: int):
    """
    Padroniza respostas de erro da API para reduzir repetição.
    """
    return jsonify({"ok": False, "erro": mensagem}), status_code


def _ativo_para_dict(ativo: Ativo) -> dict:
    """
    Converte a entidade Ativo em dicionário compatível com a API.

    Observação:
    Aqui seguimos o contrato do domínio atual:
    - usuario_responsavel
    - data_entrada
    - data_saida
    """
    return {
        "id": ativo.id_ativo,
        "tipo": ativo.tipo,
        "marca": ativo.marca,
        "modelo": ativo.modelo,
        "usuario_responsavel": ativo.usuario_responsavel,
        "departamento": ativo.departamento,
        "status": ativo.status,
        "data_entrada": ativo.data_entrada,
        "data_saida": ativo.data_saida,
        "criado_por": ativo.criado_por,
    }


def _gerar_id_ativo() -> str:
    """Gera um identificador curto para o ativo respeitando o limite do banco."""
    return secrets.token_hex(10)


@app.post("/register")
def register():
    """
    Cadastra um novo usuário.
    """
    data = request.get_json() or {}

    try:
        user_id = auth_service.registrar_usuario(
            email=data["email"],
            senha=data["senha"],
            pergunta=data["pergunta_recuperacao"],
            resposta=data["resposta_recuperacao"],
        )
        return jsonify({"ok": True, "user_id": user_id}), 201
    except KeyError as erro:
        return _erro_json(f"Campo obrigatório ausente: {erro.args[0]}", 400)
    except UsuarioJaExiste as erro:
        return _erro_json(str(erro), 409)
    except AuthErro as erro:
        return _erro_json(str(erro), 400)
    except mysql.connector.Error as erro:
        print(f"Erro no registro: {erro}")
        return _erro_json(f"Erro ao cadastrar usuário: {str(erro)}", 500)


@app.post("/login")
def login():
    """
    Autentica um usuário e grava seus dados básicos na sessão.
    """
    data = request.get_json() or {}

    try:
        usuario = auth_service.autenticar(
            email=data["email"],
            senha=data["senha"],
        )

        # Limpa qualquer dado de sessão existente antes de gravar novo usuário
        session.clear()
        session["user_id"] = usuario.id
        session["email"] = usuario.email
        # session["empresa_id"] = usuario.empresa_id  # reservado para futura multi-tenant

        return jsonify({"ok": True, "email": usuario.email})
    except KeyError as erro:
        return _erro_json(f"Campo obrigatório ausente: {erro.args[0]}", 400)
    except (UsuarioNaoEncontrado, CredenciaisInvalidas) as erro:
        return _erro_json(str(erro), 401)
    except AuthErro as erro:
        return _erro_json(str(erro), 400)


@app.post("/logout")
def logout():
    """
    Encerra a sessão do usuário autenticado.
    """
    session.clear()
    return jsonify({"ok": True})


@app.post("/forgot-password")
def forgot_password():
    """
    Redefine a senha do usuário mediante resposta correta da recuperação.
    """
    data = request.get_json() or {}

    try:
        auth_service.redefinir_senha(
            email=data["email"],
            resposta=data["resposta_recuperacao"],
            nova_senha=data["nova_senha"],
        )
        return jsonify({"ok": True})
    except KeyError as erro:
        return _erro_json(f"Campo obrigatório ausente: {erro.args[0]}", 400)
    except RecuperacaoInvalida as erro:
        return _erro_json(str(erro), 401)
    except AuthErro as erro:
        return _erro_json(str(erro), 400)


@app.get("/ativos")
@login_required
def listar_ativos():
    """
    Lista todos os ativos do usuário autenticado.
    """
    # Validação de autenticação centralizada pelo decorator
    user_id = usuario_logado_id()
    ativos = ativos_service.listar_ativos(user_id=user_id)

    return jsonify({"ok": True, "ativos": [_ativo_para_dict(ativo) for ativo in ativos]})


@app.post("/ativos")
@login_required
def criar_ativo():
    """
    Cria um novo ativo para o usuário autenticado.
    """
    # Validação de autenticação centralizada pelo decorator
    user_id = usuario_logado_id()
    data = request.get_json() or {}

    try:
        id_ativo = data.get("id") or _gerar_id_ativo()

        # Cria a entidade Ativo respeitando o contrato atual do domínio.
        ativo = Ativo(
            id_ativo=id_ativo,
            tipo=data["tipo"],
            marca=data["marca"],
            modelo=data["modelo"],
            usuario_responsavel=data["usuario_responsavel"],
            departamento=data["departamento"],
            status=data["status"],
            data_entrada=data["data_entrada"],
            data_saida=data.get("data_saida"),
            criado_por=user_id,
        )

        ativos_service.criar_ativo(ativo, user_id=user_id)
        return jsonify({"ok": True}), 201
    except KeyError as erro:
        return _erro_json(f"Campo obrigatório ausente: {erro.args[0]}", 400)
    except AtivoJaExiste as erro:
        return _erro_json(str(erro), 409)
    except AtivoErro as erro:
        return _erro_json(str(erro), 400)


@app.get("/ativos/<id_ativo>")
@login_required
def buscar_ativo(id_ativo):
    """
    Busca um ativo específico do usuário autenticado.
    """
    # Validação de autenticação centralizada pelo decorator
    user_id = usuario_logado_id()
    try:
        ativo = ativos_service.buscar_ativo(id_ativo=id_ativo, user_id=user_id)
        return jsonify({"ok": True, "ativo": _ativo_para_dict(ativo)})
    except (AtivoNaoEncontrado, PermissaoNegada) as erro:
        return _erro_json(str(erro), 404)
    except AtivoErro as erro:
        return _erro_json(str(erro), 400)


@app.put("/ativos/<id_ativo>")
@login_required
def atualizar_ativo(id_ativo):
    """
    Atualiza um ativo do usuário autenticado.
    """
    # Validação de autenticação centralizada pelo decorator
    user_id = usuario_logado_id()
    data = request.get_json() or {}

    try:
        # O payload recebido deve usar os nomes padronizados do domínio.
        ativo_atualizado = ativos_service.atualizar_ativo(
            id_ativo=id_ativo, dados=data, user_id=user_id
        )

        return jsonify({"ok": True, "ativo": _ativo_para_dict(ativo_atualizado)})
    except AtivoErro as erro:
        return _erro_json(str(erro), 400)


@app.delete("/ativos/<id_ativo>")
@login_required
def remover_ativo(id_ativo):
    """
    Remove um ativo do usuário autenticado.
    """
    # Validação de autenticação centralizada pelo decorator
    user_id = usuario_logado_id()
    try:
        ativos_service.remover_ativo(id_ativo=id_ativo, user_id=user_id)
        return jsonify({"ok": True})
    except AtivoErro as erro:
        return _erro_json(str(erro), 400)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
