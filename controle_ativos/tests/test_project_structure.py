import os


def test_project_structure_exists():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assert os.path.exists(os.path.join(base, 'web', 'app.py')), 'controle_ativos/web/app.py ausente'
    assert os.path.isdir(os.path.join(base, 'services')), 'controle_ativos/services/ ausente'
    assert os.path.isdir(os.path.join(base, 'utils')), 'controle_ativos/utils/ ausente'
    assert os.path.isdir(os.path.join(base, 'database')), 'controle_ativos/database/ ausente'
    # .gitignore deve existir na raiz do repositório
    repo_root = os.getcwd()
    assert os.path.exists(os.path.join(repo_root, '.gitignore')), '.gitignore ausente na raiz'
