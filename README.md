# Sigatccompact — Sistema de Controle de Ativos

Sistema acadêmico e técnico para gestão de ativos de TI, com backend Flask/MySQL, autenticação por sessão, CSRF, rate limit em login/recuperação, RBAC por perfil e interface web server-rendered. O objetivo do projeto é apoiar o controle patrimonial escolar com rastreabilidade, segurança básica e documentação de TCC consistente com o estado real do código.

## Visão geral

O projeto já está funcional no backend e na interface web. Hoje ele cobre cadastro de usuários, login, recuperação de senha, CRUD de ativos, listagem global para usuários autenticados, filtragem de ativos, auditoria básica e gestão simples de usuários para `SUPER_ADMIN`.

O comportamento atual é o seguinte:

- Backend Flask e MySQL funcionando.
- Autenticação por sessão.
- CSRF ativo nas rotas mutáveis.
- Rate limit em login e recuperação.
- Tratamento global de erros.
- Auditoria básica com logs e página de eventos recentes.
- RBAC com `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR`.
- Listagem global de ativos para usuários autenticados.
- Busca de ativos com filtros parciais e combinados.
- Campo `email_responsavel` disponível nos ativos.

## Tecnologias usadas

- Python 3.11+
- Flask
- MySQL
- Jinja2
- HTML, CSS e JavaScript
- `pytest`
- `bandit`
- `pip-audit`

## Funcionalidades implementadas

- Cadastro, login, logout e recuperação de senha.
- CRUD de ativos com validações centralizadas.
- Filtros por campos operacionais, inclusive `email_responsavel`.
- Ordenação e listagem global de ativos.
- Gestão simples de usuários para `SUPER_ADMIN`.
- Tela simples de auditoria para eventos recentes.
- Tratamento padronizado de erros HTTP.
- Inicialização do banco com schema + migrations.

## Segurança implementada

- Senhas com PBKDF2-SHA256.
- Salt por senha e comparação segura.
- CSRF por sessão.
- Cookies de sessão configurados explicitamente.
- Rate limit simples para login e recuperação.
- `login_required` e controle central de acesso.
- `role_required` e `permission_required`.
- Logs técnicos de autenticação e operações sensíveis.
- Tratamento global de erros sem expor detalhes técnicos ao usuário.

## Perfis RBAC

| Perfil | Acesso real atual |
| --- | --- |
| `SUPER_ADMIN` | Visualiza tudo, cria, edita e exclui ativos, cria usuários, gerencia usuários e acessa a auditoria simples. |
| `ADMIN` | Visualiza tudo, cria, edita e exclui ativos, e acessa a auditoria simples. |
| `USUARIO` | Visualiza tudo, cria e edita qualquer ativo, mas não exclui nem gerencia usuários. |
| `LEITOR` | Visualiza dashboard, quantidades e tabela global, sem criar, editar, excluir ou gerenciar usuários. |

O campo `criado_por` passou a ser metadado de autoria e auditoria. Ele não limita mais a visibilidade da listagem global de ativos.

## Interface atual

- `base.html` compartilha o layout principal.
- O dashboard exibe e-mail, perfil e contexto do usuário logado.
- A tabela de ativos é global para usuários autenticados.
- As ações de editar e excluir saem da linha selecionada, quando o perfil permite.
- A busca de ativos foi corrigida: selects começam vazios, campos vazios não filtram, `Todos` não é enviado como filtro real e filtros parciais/combinados funcionam.
- `SUPER_ADMIN` possui uma tela simples de gestão de usuários.
- Existe uma tela simples de auditoria com eventos recentes em memória.

## Banco de dados e migrations

O banco recomendado para o TCC é `tcc`.

Não misture essa base com o banco legado `controle_ativos`, que aparece em materiais antigos do projeto e pode carregar suposições já superadas.

### Tabelas e campos relevantes

- `usuarios`: usuários com perfil, status e dados de autenticação.
- `ativos`: ativos com identificação, status, responsável, departamento, datas e `email_responsavel`.

### Migrations relevantes

- `012_rbac_usuarios.sql`: adiciona a base de RBAC em usuários.
- `013_email_responsavel_ativos.sql`: adiciona `email_responsavel` aos ativos.

O executor de migrations foi corrigido para evitar o erro `Unread result found` ao inicializar o banco.

## Como rodar o projeto

### 1. Criar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar `.env`

Use a raiz do repositório e ajuste os valores para o ambiente local:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tcc
DB_USER=<USUARIO_DO_BANCO>
DB_PASSWORD=<SENHA_DO_BANCO>
FLASK_SECRET_KEY=<CHAVE_SECRETA>
APP_PEPPER=<PEPPER_LOCAL>
```

### 4. Inicializar o banco

```bash
python controle_ativos/database/init_db.py
```

Esse comando cria o schema, aplica migrations e compatibiliza bancos locais antigos quando necessário.

### 5. Promover o primeiro `SUPER_ADMIN`

```bash
python controle_ativos/scripts/promover_super_admin.py
```

### 6. Subir a aplicação

```bash
python controle_ativos/web/app.py
```

### 7. Executar os testes

```bash
python -m pytest -q
```

## Como aplicar migrations e inicializar o banco

- O fluxo atual usa `controle_ativos/database/init_db.py` como ponto de entrada.
- O script aplica o schema base e as migrations disponíveis.
- A migration 013 já faz parte do estado atual do banco e deve ser mantida no repositório.
- Se o banco local tiver estruturas legadas, o inicializador ajusta apenas o necessário para não quebrar o fluxo atual.

## Como criar o primeiro `SUPER_ADMIN`

1. Inicialize o banco.
2. Configure um usuário válido no banco, se ainda não existir.
3. Execute `python controle_ativos/scripts/promover_super_admin.py`.
4. Confirme o perfil `SUPER_ADMIN` na tela simples de gestão de usuários.

## Testes

O projeto possui suíte automatizada com `pytest`. Os testes cobrem:

- autenticação e recuperação de senha;
- CSRF e cookies de sessão;
- rate limit de login/recuperação;
- RBAC e permissões por perfil;
- busca e filtro de ativos;
- inicialização do banco e migrations;
- tratamento de erros e rotas principais.

O estado atual foi validado com `python -m pytest -q`.

## Status atual do projeto

- Backend funcional e consistente com a interface web atual.
- RBAC implementado por perfil.
- Listagem global de ativos consolidada.
- Busca de ativos corrigida.
- Migrations 012 e 013 presentes.
- Inicialização do banco corrigida contra `Unread result found`.
- Testes aprovados no estado atual.

## Limitações conhecidas e evoluções futuras

- A auditoria da interface ainda mostra eventos recentes em memória; persistência histórica em banco continua como evolução futura.
- Permissões customizadas por usuário ainda não existem; o sistema usa perfis padrão.
- Reautenticação para ações críticas ainda pode ser adicionada depois.
- Exportação controlada de logs também fica para uma etapa posterior.
- Headers de segurança mais avançados podem ser incorporados em evolução futura.
- Uma interface administrativa mais rica para usuários e auditoria pode ser construída depois do TCC.

## Documentação relacionada

- [RBAC - Perfis e Permissões](docs/rbac-perfis-permissoes.md)
- [Plano de Interface e RBAC](docs/plano-interface-rbac.md)
- [Auditoria da Interface e Templates](docs/auditoria-interface-templates.md)
- [Banco de Dados](docs/banco-de-dados.md)
- [Segurança](docs/seguranca.md)
- [Checklist de Segurança Backend](docs/checklist-seguranca-backend.md)
- [Riscos Conhecidos de Segurança](docs/riscos-conhecidos-seguranca.md)
- [Plano de Correção de Segurança Backend](docs/plano-correcao-seguranca-backend.md)

