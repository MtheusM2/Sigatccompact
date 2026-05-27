import subprocess
import sys
import os


def _run_python_import(with_secret: bool):
    """Executa um processo Python que tenta importar o módulo da aplicação.
    Retorna (exit_code, stdout+stderr).
    """
    env = os.environ.copy()
    if with_secret:
        env['FLASK_SECRET_KEY'] = 'test-secret-for-ci'
        snippet = 'import importlib; importlib.import_module("controle_ativos.web.app")'
    else:
        env.pop('FLASK_SECRET_KEY', None)
        # Simula ambiente sem FLASK_SECRET_KEY e sem .env carregado.
        # O teste continua validando que a app exige segredo explícito.
        snippet = (
            'import importlib, dotenv; '
            'dotenv.load_dotenv = lambda *args, **kwargs: False; '
            'importlib.import_module("controle_ativos.web.app")'
        )

    cmd = [sys.executable, '-c', snippet]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout + proc.stderr


def _run_web_local_import():
    """Importa `app.py` como módulo local a partir da pasta web.

    Esse cenário reproduz a execução feita dentro de `controle_ativos/web`,
    onde o app precisa ajustar o sys.path antes de importar `controle_ativos.*`.
    """
    env = os.environ.copy()
    env['FLASK_SECRET_KEY'] = 'test-secret-for-ci'

    package_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    web_dir = os.path.join(package_root, "web")
    cmd = [sys.executable, '-c', 'import importlib; importlib.import_module("app")']
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=web_dir)
    return proc.returncode, proc.stdout + proc.stderr


def test_app_requires_flask_secret_key():
    """
    Verifica que a aplicação exige `FLASK_SECRET_KEY` quando importada sem essa variável.
    Se a importação com a variável definida falhar, o teste também falha.
    """
    code_no_secret, out_no = _run_python_import(with_secret=False)
    # Esperamos que a importação sem segredo falhe (aplicação exige a variável)
    assert code_no_secret != 0, 'Importação da app sem FLASK_SECRET_KEY terminou com sucesso (esperado erro)'

    code_with_secret, out_with = _run_python_import(with_secret=True)
    assert code_with_secret == 0, f'Importação da app com FLASK_SECRET_KEY falhou: {out_with}'


def test_flask_debug_not_true_by_default():
    # Verifica var de ambiente FLASK_DEBUG não definida como true por padrão no ambiente atual
    val = os.environ.get('FLASK_DEBUG', '').lower()
    assert val != 'true', 'FLASK_DEBUG está ativo no ambiente local por padrão'


def test_app_importa_a_partir_da_pasta_web():
    """
    Garante que o app Flask sobe quando importado de dentro de `controle_ativos/web`.
    Sem a raiz do projeto no sys.path, esse fluxo falha com ModuleNotFoundError.
    """
    code, output = _run_web_local_import()
    assert code == 0, f'Importação local da app Flask falhou: {output}'
