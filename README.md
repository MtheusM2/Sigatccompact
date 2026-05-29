# 🖥️ Sigatccompact — Sistema de Gestão de Ativos

> Sistema acadêmico/técnico (TCC) para gestão de ativos de TI — backend em Flask, interface server-rendered (Jinja2) e banco MySQL. Foco em segurança aplicada, RBAC e rastreabilidade.

<!-- Badges -->
[![Status](https://img.shields.io/badge/status-Funcional%20(local)-brightgreen)](#)
[![Curso](https://img.shields.io/badge/curso-Manuten%C3%A7%C3%A3o%20e%20Suporte-blue)](#)
[![Disciplina](https://img.shields.io/badge/Disciplina-Governan%C3%A7a%20de%20TI-lightgrey)](#)
[![Semestre](https://img.shields.io/badge/Semestre-2026.1-orange)](#)
[![Backend](https://img.shields.io/badge/backend-Flask-000000?logo=flask&logoColor=white)](#)
[![Database](https://img.shields.io/badge/database-MySQL-00758F?logo=mysql&logoColor=white)](#)
[![Seguran%C3%A7a](https://img.shields.io/badge/seguran%C3%A7a-CSRF%20%2B%20RBAC-blue)](#)
[![Testes](https://img.shields.io/badge/testes-pytest-4B8BBE)](#)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)](#)
[![TCC](https://img.shields.io/badge/TCC-ETEC%20Jaragu%C3%A1-lightgrey)](#)

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Resumo e Palavras-chave](#resumo-e-palavras-chave)
- [Problema e Justificativa](#problema-e-justificativa)
- [Objetivos](#objetivos)
- [Metodologia / Estratégia Técnica](#metodologia-tecnica)
- [Escopo e Delimitações](#escopo-e-delimitacoes)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Matriz de Perfis e Permissões (RBAC)](#matriz-rbac)
- [Segurança Aplicada](#seguranca-aplicada)
- [Banco de Dados e Migrations](#banco-de-dados-e-migrations)
- [Arquitetura e Tecnologias](#arquitetura-e-tecnologias)
- [Estrutura do Repositório](#estrutura-do-repositorio)
- [Como Navegar no Projeto](#como-navegar)
- [Configuração e Execução](#configuracao-e-execucao)
- [Criar / Promover SUPER_ADMIN](#super-admin)
- [Testes e Qualidade](#testes-e-qualidade)
- [Resultados Técnicos Atuais](#resultados-tecnicos)
- [Limitações Conhecidas](#limitacoes-conhecidas)
- [Evoluções Futuras](#evolucoes-futuras)
- [Glossário](#glossario)
- [Equipe / Autoria](#equipe-e-autoria)
- [Licença / Uso Acadêmico](#licenca-uso-academico)
- [Checklist de Entrega](#checklist-de-entrega)

---

<a id="sobre-o-projeto"></a>
## Sobre o Projeto

| Campo            | Detalhe                                          |
| ---------------- | ------------------------------------------------ |
| Instituição      | ETEC Jaraguá — Centro Paula Souza                |
| Curso            | Manutenção e Suporte em Informática              |
| Disciplina       | Governança de TI                                 |
| Semestre         | 2026.1                                           |
| Orientadora      | Professora Tainá Barros Batista Oliveira         |
| Tipo de Trabalho | TCC — Trabalho de Conclusão de Curso             |
| Projeto          | Sigatccompact — Sistema de Gestão de Ativos      |
| Stack principal  | Python, Flask, MySQL, Jinja2, Pytest             |
| Status atual     | Backend e interface web funcionais em ambiente local |

---

<a id="resumo-e-palavras-chave"></a>
## Resumo e Palavras-chave

O Sigatccompact substitui controles manuais de inventário por um sistema web que oferece cadastro, autenticação, controle por perfil e rastreabilidade mínima dos ativos. O projeto prioriza segurança aplicada e reprodutibilidade do ambiente para fins de avaliação acadêmica.

Palavras-chave: `gestão de ativos`, `TCC`, `Flask`, `MySQL`, `RBAC`, `segurança`, `controle patrimonial`, `rastreabilidade`

---

<a id="problema-e-justificativa"></a>
## Problema e Justificativa

### Problema

Controles de ativos mantidos em planilhas ou registros manuais dificultam rastreio, atualização, consulta padronizada e responsabilização técnica.

### Justificativa

- Necessidade de controle centralizado de ativos em ambientes institucionais;
- Rastreamento de responsável (`email_responsavel`) e autoria (`criado_por`) para auditoria mínima;
- Aplicação de controle de acesso para operações sensíveis (RBAC);
- Reprodutibilidade técnica e validação por testes automatizados para TCC.

---

<a id="objetivos"></a>
## Objetivos

### Objetivo geral

Desenvolver um sistema web para gestão de ativos de TI com segurança básica, autenticação, controle de permissões e rastreabilidade, adequado ao escopo de TCC.

### Objetivos específicos

- Implementar backend em Flask e modelagem em MySQL;
- Criar CRUD de ativos com validações centralizadas;
- Implementar autenticação por sessão e recuperação de senha com rate limit;
- Aplicar RBAC por perfis e controles de autorização;
- Habilitar CSRF em rotas mutáveis;
- Documentar banco, migrations e decisões técnicas (ADRs);
- Estruturar suíte de testes automatizados com `pytest`;
- Disponibilizar interface server-rendered funcional para operações básicas.

---

<a id="metodologia-tecnica"></a>
## Metodologia / Estratégia Técnica

- Desenvolvimento incremental e modular;
- Arquitetura em camadas: `models`, `services`, `web`, `database`;
- Validações centralizadas e padrões de segurança inspirados em OWASP;
- Testes automatizados com `pytest` e checagens de segurança no CI;
- Versionamento em Git/GitHub e integração contínua via GitHub Actions.

---

<a id="escopo-e-delimitacoes"></a>
## Escopo e Delimitações

### Dentro do escopo

- CRUD de ativos;
- Cadastro/login/logout/recuperação de senha;
- RBAC por perfis (`SUPER_ADMIN`, `ADMIN`, `USUARIO`, `LEITOR`);
- Gestão simples de usuários (restrita a `SUPER_ADMIN`);
- Busca e filtros na listagem de ativos (campos vazios não filtram; "Todos" não é filtro real);
- Auditoria básica (eventos recentes exibidos na interface);
- Migrations e inicializador (`init_db.py`);
- Testes automatizados e documentação técnica.

### Fora do escopo atual

- Frontend SPA (React/Vue) ou mobile app;
- Permissões customizadas por usuário (além de perfis);
- Auditoria persistida em banco com histórico completo;
- Exportação avançada de logs/relatórios;
- Integrações SSO e API pública.

---

<a id="funcionalidades-implementadas"></a>
## Funcionalidades Implementadas

| Funcionalidade | Status | Observação |
|---|---:|---|
| Autenticação por sessão | Implementado | Login / logout / recuperação |
| Recuperação de senha | Implementado | Com rate limit |
| CRUD de ativos | Implementado | Interface web server-rendered |
| Listagem global | Implementado | Todos usuários autenticados visualizam |
| Busca / filtros | Implementado | Campos vazios não filtram; filtros combinados funcionam |
| RBAC | Implementado | 4 perfis (SUPER_ADMIN, ADMIN, USUARIO, LEITOR) |
| Gestão de usuários | Implementado | Restrito a `SUPER_ADMIN` |
| Auditoria básica | Parcial | Eventos recentes em memória |
| CI | Implementado | GitHub Actions (testes + security) |
| Segurança automatizada | Implementado | Bandit / pip-audit em workflow |

---

<a id="matriz-rbac"></a>
## Matriz de Perfis e Permissões (RBAC)

| Perfil | Visualizar ativos | Criar ativo | Editar ativo | Excluir ativo | Gerenciar usuários | Auditoria |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| SUPER_ADMIN | Sim | Sim | Sim | Sim | Sim | Sim |
| ADMIN | Sim | Sim | Sim | Sim | Não | Sim/Parcial |
| USUARIO | Sim | Sim | Sim | Sim | Não | Não |
| LEITOR | Sim | Não | Não | Não | Não | Não |

---

<a id="seguranca-aplicada"></a>
## Segurança Aplicada

- Hash de senhas com PBKDF2 (salt; aplicação de pepper opcional);
- CSRF habilitado para rotas mutáveis;
- Cookies de sessão configurados com flags apropriadas;
- Rate limit em endpoints sensíveis (login / recuperação de senha);
- Tratamento global de erros para evitar exposição de dados internos;
- Controle central de acesso via decoradores (`login_required`, `role_required`, `permission_required`);
- Logs técnicos para operações sensíveis;
- CI com checagens de segurança automatizadas.

---

<a id="banco-de-dados-e-migrations"></a>
## Banco de Dados e Migrations

- Banco recomendado para o TCC: `tcc`;
- Tabelas principais: `usuarios`, `ativos` (inclui `email_responsavel`, `criado_por`, status, datas);
- Migrations relevantes:
  - `012_rbac_usuarios.sql` — base de RBAC em `usuarios`;
  - `013_email_responsavel_ativos.sql` — adiciona `email_responsavel` aos ativos;
- Inicializador: `controle_ativos/database/init_db.py` aplica schema + migrations; executor ajustado para evitar `Unread result found`.

---

<a id="arquitetura-e-tecnologias"></a>
## Arquitetura e Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.11+ + Flask |
| Templates | Jinja2 |
| Banco | MySQL |
| Testes | pytest |
| Segurança | CSRF, PBKDF2, Bandit, pip-audit |
| CI/CD | GitHub Actions |
| Versionamento | Git / GitHub |

Breve mapa de responsabilidades:
- `controle_ativos/models` — modelos de entidade;
- `controle_ativos/services` — lógica de negócio;
- `controle_ativos/database` — conexão, init_db.py e migrations;
- `controle_ativos/web` — app Flask, templates e static;
- `controle_ativos/scripts` — utilitários, como `promover_super_admin.py`;

---

<a id="estrutura-do-repositorio"></a>
## Estrutura do Repositório (resumo)

```text
controle_ativos/
├── database/
├── models/
├── services/
├── scripts/
├── web/
├── tests/
├── utils/
└── README.md

docs/
.github/workflows/
requirements.txt
requirements-dev.txt
pytest.ini
```

---

<a id="como-navegar"></a>
## Como Navegar no Projeto

| Eu quero... | Vá para... |
|---|---|
| Entender permissões | [docs/rbac-perfis-permissoes.md](docs/rbac-perfis-permissoes.md) |
| Ver banco / migrations | [docs/banco-de-dados.md](docs/banco-de-dados.md) |
| Ver segurança | [docs/seguranca.md](docs/seguranca.md) |
| Rodar testes | [docs/testes.md](docs/testes.md) |
| Ver ADRs | [docs/adr/](docs/adr/) |
| Ver plano de interface e RBAC | [docs/plano-interface-rbac.md](docs/plano-interface-rbac.md) |

---

<a id="configuracao-e-execucao"></a>
## Configuração e Execução

1. Criar e ativar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instalar dependências

```bash
pip install -r requirements.txt
```

3. Configurar `.env` (exemplo mínimo, **NÃO** commitar credenciais)

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tcc
DB_USER=<usuario>
DB_PASSWORD=<senha>
FLASK_SECRET_KEY=<chave_secreta>
APP_PEPPER=<pepper>
```

4. Inicializar banco e aplicar migrations

```bash
python controle_ativos/database/init_db.py
```

5. (Opcional) Promover o primeiro `SUPER_ADMIN`

```bash
python controle_ativos/scripts/promover_super_admin.py
```

6. Iniciar a aplicação web (principal)

```bash
python -m controle_ativos.web.app
```

  Alternativa:

  ```bash
  python controle_ativos/web/app.py
  ```

7. Executar testes

```bash
python -m pytest -q
```

---

<a id="super-admin"></a>
## Criar / Promover o primeiro `SUPER_ADMIN`

1. Inicialize o banco (`init_db.py`).
2. Crie um usuário via interface ou insira registro em `usuarios` se necessário.
3. Execute `python controle_ativos/scripts/promover_super_admin.py`.
4. Valide o perfil `SUPER_ADMIN` na interface de gestão de usuários.

---

<a id="testes-e-qualidade"></a>
## Testes e Qualidade

- Executar localmente: `python -m pytest -q`;
- Verificar `git diff --check` antes de commitar para detectar normalizações de fim de linha;
- CI: GitHub Actions roda testes e verificações de segurança.

---

<a id="resultados-tecnicos"></a>
## Resultados Técnicos Atuais

| Área | Resultado |
|---|---|
| Backend | Funcional com Flask |
| Interface | Server-rendered funcional |
| Segurança | CSRF, rate limit, PBKDF2 e RBAC |
| Banco | Migrations aplicadas (012 e 013) |
| Testes | Suíte Pytest disponível |
| CI | Testes e checagens de segurança em GitHub Actions |
| Documentação | `README.md` e `docs/` |

---

<a id="limitacoes-conhecidas"></a>
## Limitações Conhecidas

- Auditoria simples em memória, sem persistência histórica;
- Permissões por usuário individual ainda não existem;
- Sem frontend SPA, exportação avançada de logs ou integrações SSO;
- Hardening HTTP avançado permanece para evolução futura.

---

<a id="evolucoes-futuras"></a>
## Evoluções Futuras

- Persistência completa de auditoria e exportação de logs;
- Permissões granulares por usuário;
- API REST para integrações;
- Frontend moderno (SPA) e dashboard analítico;
- Integração SSO e conformidade de privacidade (LGPD).

---

<a id="glossario"></a>
## Glossário

<details>
<summary>RBAC</summary>

Role-Based Access Control — controle de acesso por perfis.

</details>

<details>
<summary>CSRF</summary>

Cross-Site Request Forgery — proteção para rotas mutáveis.

</details>

<details>
<summary>CRUD</summary>

Create, Read, Update, Delete.

</details>

<details>
<summary>Migration</summary>

Script versionado que altera o esquema do banco.

</details>

<details>
<summary>Session</summary>

Autenticação baseada em sessão do servidor (cookies).

</details>

<details>
<summary>Rate limit</summary>

Limitação de tentativas em endpoints sensíveis.

</details>

<details>
<summary>SUPER_ADMIN</summary>

Perfil com acesso total ao sistema e gestão de usuários.

</details>

<details>
<summary>LEITOR</summary>

Perfil apenas de visualização de ativos e dashboard.

</details>

<details>
<summary>email_responsavel</summary>

Campo do ativo que registra o responsável vinculado.

</details>

<details>
<summary>auditoria</summary>

Registro básico de eventos recentes de operação.

</details>

<details>
<summary>criado_por</summary>

Metadado de autoria para rastreabilidade do ativo.

</details>

---

<a id="equipe-e-autoria"></a>
## Equipe / Autoria

| Nome | Responsabilidade |
|---|---|
| Lays Yuri Matukawa | Documentação, apresentação e apoio acadêmico |
| Vitória Lopes Siqueira | Documentação, apresentação e apoio acadêmico |
| Geovanny Iago Damasceno Mendes | Documentação e apoio acadêmico |
| Felipe dos Santos Nascimento | Responsável inicial pela interface / frontend |
| Matheus Santos do Nascimento |  Desenvolvimento backend, banco, segurança, RBAC, testes e documentação técnica |

**Orientadora:** Professora Tainá Barros Batista Oliveira

---

<a id="licenca-uso-academico"></a>
## Licença / Uso Acadêmico

Projeto desenvolvido para fins acadêmicos (TCC — ETEC Jaraguá). Uso e reprodução permitidos para fins educacionais, citando os autores.

---

<a id="checklist-de-entrega"></a>
## Checklist de Entrega

<details>
<summary>Itens verificados</summary>

- [x] Modelo acadêmico/técnico preservado
- [x] Índice com âncoras manuais estáveis
- [x] Links para a documentação convertidos em Markdown real
- [x] Matriz RBAC conferida
- [x] Comandos de execução padronizados

</details>
