# Requirements oficiais — DataAssets

## Arquivos criados
- `requirements.txt`
- `requirements-dev.txt`

## Dependências de produção
- `Flask==3.1.3`: framework web usado em `controle_ativos/web/app.py` para rotas, sessão e renderização de templates.
- `mysql-connector-python==9.6.0`: driver usado em `controle_ativos/database/connection.py` para conectar ao MySQL.
- `python-dotenv==1.2.2`: usado em `controle_ativos/database/connection.py` para carregar variáveis do arquivo `.env`.

Observação:
- `Werkzeug` não foi adicionado explicitamente porque não aparece como import direto no projeto; ele já vem como dependência transitiva do `Flask`.
- `openpyxl`, `reportlab`, `waitress` e `PyJWT` não foram incluídos porque não aparecem nos imports reais analisados.

## Dependências de desenvolvimento
- `-r requirements.txt`: garante que o ambiente de desenvolvimento instale também as dependências de produção.
- `pytest==9.0.3`: framework de testes usado pela suíte em `controle_ativos/tests/`.
- `pytest-cov==7.1.0`: cobertura de testes e suporte a relatórios no CI.
- `bandit==1.9.4`: análise estática de segurança do código Python.
- `pip-audit==2.10.0`: auditoria de vulnerabilidades nas dependências declaradas.

## Workflow atualizado
- O workflow do backend foi ajustado em `.github/workflows/ci-backend1.yml` para usar os arquivos oficiais de dependências.
- Agora a etapa de instalação instala `requirements-dev.txt` quando ele existe.
- Se apenas `requirements.txt` existir, o CI instala as dependências de produção e adiciona as ferramentas de teste e segurança manualmente.
- Se nenhum arquivo existir, o workflow falha com erro claro.
- A auditoria com `pip-audit` não é mais pulada; ela agora executa `pip-audit -r requirements.txt --strict`.
- O cache do `setup-python` foi reativado usando os arquivos de requirements como dependência do cache.

## Validações executadas
- `python -m pip install -r requirements-dev.txt`
- `python -m pytest -q` -> passou com sucesso.
- `bandit -r controle_ativos -x "controle_ativos/tests,tests,controle_ativos/.venv,.venv,venv" -lll` -> sem bloqueios relevantes.
- `pip-audit -r requirements.txt --strict` -> sem vulnerabilidades conhecidas.
- `git ls-files | Select-String '__pycache__|\.pyc$|^\.env$|\.log$'` -> sem saída, indicando que não há artefatos proibidos rastreados.

## Pendências
- Revisar periodicamente se novas bibliotecas realmente entram nos imports antes de adicioná-las ao `requirements.txt`.
- Se o repositório for reorganizado, considerar renomear o workflow para `ci-backend.yml` apenas para alinhar o nome ao padrão desejado.
- Quando houver novos testes ou novas ferramentas, manter a separação entre runtime e desenvolvimento.
