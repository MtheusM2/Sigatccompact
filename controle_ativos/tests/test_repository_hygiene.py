import subprocess
import re


def test_no_tracked_bytecode_or_secrets():
    """
    Protege o repositório contra artefatos locais versionados.
    Falha se encontrar arquivos `.pyc`, `__pycache__`, `.env` ou `.log` rastreados pelo Git.
    """
    proc = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    assert proc.returncode == 0, 'Falha ao executar git ls-files'
    out = proc.stdout
    # Busca por padrões proibidos
    m = re.search(r'(^|\n).*(__pycache__|\.pyc$|^\.env$|\.log$)', out, re.M)
    assert m is None, f'Arquivos indesejados versionados detectados: {m.group(0) if m else "(nenhum)"}'
