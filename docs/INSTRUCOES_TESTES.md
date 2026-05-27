# Requirements oficiais e testes

Esta página resume como instalar o ambiente, executar os testes e rodar a auditoria de dependências do projeto DataAssets.

O projeto usa dois arquivos de dependências:
- `requirements.txt` para execução do sistema em produção/local.
- `requirements-dev.txt` para desenvolvimento, testes e CI.

Instalação do ambiente (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Rodar testes:

```powershell
python -m pytest -q
```

Estado verificado em 2026-05-27:

```text
59 passed
```

Observacao: os testes de performance ficam desativados por padrao. Para executar benchmarks locais, defina `RUN_PERF_TESTS=1` e garanta que o MySQL esteja disponivel com schema compativel.

Auditoria:

```powershell
bandit -r controle_ativos -x "controle_ativos/tests,tests,controle_ativos/.venv,.venv,venv" -lll
pip-audit -r requirements.txt --strict
```

Notas importantes:
- `requirements.txt` deve conter apenas dependências necessárias para executar o sistema.
- `requirements-dev.txt` deve conter o arquivo principal mais as ferramentas de teste e segurança.
- `.venv` não deve ser versionado.
- Toda dependência nova deve entrar no arquivo correto, nunca via instalação manual no workflow.
- Se precisar limpar bytecode rastreado, use `git rm --cached` para remover apenas do índice.
