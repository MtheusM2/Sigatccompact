import os
from pathlib import Path


def test_project_structure_exists():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    assert os.path.exists(os.path.join(base, 'web', 'app.py')), 'controle_ativos/web/app.py ausente'
    assert os.path.isdir(os.path.join(base, 'services')), 'controle_ativos/services/ ausente'
    assert os.path.isdir(os.path.join(base, 'utils')), 'controle_ativos/utils/ ausente'
    assert os.path.isdir(os.path.join(base, 'database')), 'controle_ativos/database/ ausente'
    # .gitignore deve existir na raiz do repositório
    repo_root = os.getcwd()
    assert os.path.exists(os.path.join(repo_root, '.gitignore')), '.gitignore ausente na raiz'


def test_schema_e_migration_de_email_responsavel():
    repo_root = Path(__file__).resolve().parents[1]
    schema = (repo_root / 'database' / 'schema.sql').read_text(encoding='utf-8')
    migration = (repo_root / 'database' / 'migrations' / '013_email_responsavel_ativos.sql').read_text(encoding='utf-8')

    assert 'email_responsavel VARCHAR(255) NULL' in schema
    assert 'email_responsavel' in schema
    assert 'INFORMATION_SCHEMA.COLUMNS' in migration
    assert 'email_responsavel VARCHAR(255) NULL' in migration
