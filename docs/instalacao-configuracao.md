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
DB_NAME=controle_ativos
DB_USER=<USUARIO_DO_BANCO>
DB_PASSWORD=<SENHA_DO_BANCO>
FLASK_SECRET_KEY=<CHAVE_SECRETA>
APP_PEPPER=<PEPPER_LOCAL>
```

Inicializar banco

Assegure que o MySQL está em execução e execute:

```bash
python controle_ativos/database/init_db.py
```

Executar aplicação

```bash
python controle_ativos/web/app.py
```

Executar testes

```bash
python -m pytest -q
```

Notas

- Nunca commite o arquivo `.env`.
- Use `.env.example` com placeholders para facilitar contribuições.