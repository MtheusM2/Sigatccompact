# Fase 1 — Instruções mínimas para testes e higiene do repositório

Este arquivo descreve os comandos mínimos para executar os testes e limpar artefatos rastreados pelo Git.

Requisitos mínimos:
- Python 3.x instalado
- Dependências do projeto já instaladas no ambiente (se houver)

Executar testes (PowerShell):

```powershell
python -m pytest -q
```

Verificação rápida de artefatos rastreados (PowerShell):

```powershell
# listar arquivos rastreados que correspondam a padrões indesejados
git ls-files | Select-String '__pycache__|\.pyc$|^\.env$|\.log$' | ForEach-Object { Write-Host $_.Line }
```

Remover artefatos rastreados do índice Git (não faz commit):

```powershell
# remove arquivos correspondentes do índice sem apagar do disco
git ls-files | Where-Object { $_ -match '__pycache__|\\.pyc$' } | ForEach-Object { git rm --cached --ignore-unmatch $_ }
```

Adicionar/atualizar `.gitignore` (exemplo mínimo já presente no repositório):

```text
# python
__pycache__/
*.py[cod]
.venv/
.env
*.log

```

Notas importantes:
- Não commitamos mudanças de segurança nesta fase (CSRF, PBKDF2, salt/pepper, regras de negócio).
- As instruções acima apenas removem arquivos do índice; se quiser persistir as mudanças, faça `git add .` seguido de `git commit` localmente.
- Se encontrar `index.lock`, verifique processos Git em execução ou remova `.git/index.lock` com cuidado.

Contato: mantenha backup antes de remover arquivos massivamente do índice.
