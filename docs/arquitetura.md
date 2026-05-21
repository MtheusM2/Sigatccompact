# Arquitetura do Sistema

Visão geral

O projeto segue arquitetura modular organizada por responsabilidades, com separação clara entre camada web, serviços de negócio, modelos e persistência de dados.

Principais componentes

- `web/`: camada de interface (Flask) e templates HTML.
- `services/`: lógica de negócio e operações sobre entidades (ex.: `ativos_service.py`, `auth_service.py`).
- `models/`: entidades do domínio (ex.: `ativos.py`, `usuario.py`).
- `database/`: conexão com MySQL, scripts de inicialização (`init_db.py`, `schema.sql`).
- `utils/`: funções auxiliares, criptografia e validadores.
- `tests/`: suítes de testes automatizados (pytest).

Fluxo básico

1. O cliente (navegador ou cliente HTTP) faz requisição ao Flask em `web/app.py`.
2. O endpoint valida entrada e delega a um serviço em `services/`.
3. O serviço utiliza `models/` e `database/` para persistir/consultar dados.
4. A resposta é renderizada via template ou retornada como JSON.

Observações

- O sistema está preparado para evolução para API RESTful; templates HTML e endpoints coexistem atualmente.
- Não foram inventadas camadas extras além das já presentes no código — este documento descreve o estado atual do repositório.