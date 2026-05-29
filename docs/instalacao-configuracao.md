# Instalação e Configuração

Pré-requisitos

- Python 3.11+
- MySQL Server
- Git

Criar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instalar dependências

```bash
pip install -r requirements.txt
```

Variáveis de ambiente (`.env`)

Crie um arquivo `.env` na raiz com este exemplo (use placeholders):

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tcc
DB_USER=<USUARIO_DO_BANCO>
DB_PASSWORD=<SENHA_DO_BANCO>
FLASK_SECRET_KEY=<CHAVE_SECRETA>
APP_PEPPER=<PEPPER_LOCAL>
```

O arquivo `.env` deve ficar na raiz do repositório. A aplicação carrega esse caminho automaticamente em `controle_ativos/database/connection.py`, então não é necessário carregar o `.env` manualmente antes de iniciar o Flask.

Inicializar banco

Assegure que o MySQL está em execução e execute:

```bash
python controle_ativos/database/init_db.py
```

Esse comando também aplica as migrations atuais, incluindo `012_rbac_usuarios.sql` e `013_email_responsavel_ativos.sql`, além de compatibilizar bancos locais antigos sem alterar o comportamento real do TCC.

Executar aplicação

```bash
python controle_ativos/web/app.py
```

Executar testes

```bash
python -m pytest -q
```

Promover o primeiro SUPER_ADMIN

```bash
python controle_ativos/scripts/promover_super_admin.py
```

Notas

- Nunca commite o arquivo `.env`.
- Use `.env.example` com placeholders para facilitar contribuições.
- O banco recomendado para o TCC é `tcc`, não `controle_ativos`.
