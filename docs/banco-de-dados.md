# Banco de Dados

Banco: MySQL

Visão geral das tabelas (resumo)

- `usuarios`: tabela de usuários com identificador, email e hash de senha.
- `ativos`: tabela de ativos com campos de identificação, status, responsável, departamento e datas.

Estado atual do schema

- O esquema do repositório está centrado em `usuarios` e `ativos`, com FK de `criado_por` para usuário autenticado.
- A autenticação operacional atual usa sessão Flask; não há tabela de tokens no schema atual.
- O fluxo atual de cadastro de usuários não depende de `empresa_id` nem de `nome`.
- Bancos locais legados que ainda possuam `usuarios.empresa_id`, `usuarios.nome` ou `ativos.empresa_id` são compatibilizados pelo `init_db.py` para permitir `NULL`, sem apagar colunas nem dados existentes.

Migrações e inicialização

O esquema inicial está em `controle_ativos/database/schema.sql` e o script de criação em `controle_ativos/database/init_db.py`.

O script de inicialização é idempotente para o estado atual do projeto: pode ser executado novamente para criar tabelas ausentes e relaxar campos legados obrigatórios que não fazem parte do fluxo operacional atual.

Cuidados com credenciais

- Use variáveis de ambiente para conexão (não versionar `.env`).
- Faça backups regulares do banco antes de alterações estruturais.

Observação

Não inclua credenciais no repositório. Use `.env.example` com placeholders para documentar as variáveis necessárias.
