# DataAssets — Sistema de Controle de Ativos

[![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-yellowgreen)]() [![TCC](https://img.shields.io/badge/Tipo-TCC-blue)]() [![Tech](https://img.shields.io/badge/Stack-Python%20|%20Flask%20|%20MySQL-lightgrey)]()

Resumo

Projeto acadêmico (TCC) para controle de ativos de TI. Fornece cadastro, consulta, edição e remoção de ativos, com autenticação de usuários e uma base para migração progressiva para APIs com Bearer Token.

Problema que resolve

Reduz a dependência de planilhas dispersas, melhora rastreabilidade de equipamentos e organiza um inventário único para a gestão de ativos.

Objetivos

- Inventário centralizado de ativos.
- Controle de ciclo de vida dos equipamentos.
- Apoio à governança de TI e auditoria básica.

Status do projeto

- Desenvolvimento para TCC.
- Funcionalidades principais implementadas (CRUD de ativos, autenticação, dashboard).
- Segurança em evolução: migração gradual para Bearer Token; rate limit e política de senha implementados.

Principais tecnologias

- Python 3.11+
- Flask
- MySQL
- HTML/CSS/JavaScript
- Pytest

Índice de documentação

| Documento | Descrição |
|---|---|
| [Visão Geral](docs/visao-geral.md) | Propósito do projeto, público e escopo. |
| [Funcionalidades](docs/funcionalidades.md) | Lista de funcionalidades implementadas e em evolução. |
| [Arquitetura](docs/arquitetura.md) | Organização técnica e fluxo da aplicação. |
| [Banco de Dados](docs/banco-de-dados.md) | Estrutura básica e cuidados com dados. |
| [Segurança](docs/seguranca.md) | Medidas aplicadas e riscos conhecidos. |
| [Autenticação por Token](docs/autenticacao-token.md) | Fluxo de tokens e uso do decorator `@token_required`. |
| [Instalação e Configuração](docs/instalacao-configuracao.md) | Como preparar ambiente local. |
| [Testes](docs/testes.md) | Suíte de testes e comandos. |
| [Operação e Uso](docs/operacao-uso.md) | Fluxos de operação para usuários. |
| [Roadmap](docs/roadmap.md) | Melhorias planejadas. |
| [Análise Técnica (TCC)](docs/tcc-analise-tecnica.md) | Documento para apresentação acadêmica. |

Como começar (resumo rápido)

1. Criar ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente: copie `.env.example` para `.env` e preencha os valores (não versionar `.env`).

4. Inicializar banco (MySQL) e criar esquema:

```bash
python controle_ativos/database/init_db.py
```

5. Executar a aplicação localmente (desenvolvimento):

```bash
python controle_ativos/web/app.py
```

6. Executar testes:

```bash
python -m pytest -q
```

Avisos de segurança

- Nunca versionar `.env` ou arquivos com credenciais.
- Use `.env.example` com placeholders para documentação.
- Não inclua tokens ou senhas reais nos documentos.

Estrutura do repositório (resumo)

```
controle_ativos/
	├─ web/ (Flask app and templates)
	├─ services/ (business logic)
	├─ models/ (data models)
	├─ database/ (connection and schema)
	└─ utils/ (helpers, crypto, validators)

docs/ (documentação organizada para TCC)
tests/ (pytest)
```


Contribuição e contato

Este repositório é mantido pelo autor do TCC. Para contribuições, siga o fluxo de branches e Pull Requests. Para dúvidas, abra uma issue.

Equipe

| Nome | Função / Responsabilidade |
|---|---|
| Mateus Santos | Backend e Segurança |
| Felipe | Frontend |
| Giovane | Documentação: proposta de vendas |
| Laís | Documentação completa (monografia) |
| Vitória | Documentação: problemas e propostas de solução |

Licença / Observação acadêmica

Projeto desenvolvido para fins de Trabalho de Conclusão de Curso (TCC). Consulte `docs/tcc-analise-tecnica.md` para a análise técnica.
