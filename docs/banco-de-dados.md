# Banco de Dados

Banco recomendado para o TCC: MySQL com schema nomeado como `tcc`.

Não misture essa base com o banco legado `controle_ativos` do projeto antigo. O nome aparece em materiais históricos, mas o fluxo atual deve usar a base do TCC de forma isolada.

## Visão geral das tabelas

- `usuarios`: usuários com e-mail, hash de senha, perfil, status e metadados de autenticação.
- `ativos`: ativos com identificação, status, responsável, departamento, datas e `email_responsavel`.

## Estado atual do schema

- O fluxo atual usa sessão Flask, não tabela de tokens.
- `criado_por` em `ativos` funciona como metadado de autoria e auditoria.
- A listagem de ativos não é mais limitada por autoria.
- O schema atual cobre a base de RBAC com perfis e status de usuário.
- Bancos locais legados ainda podem passar pelo inicializador para compatibilidade, mas isso não altera o comportamento atual esperado.

## Migrations e inicialização

- `controle_ativos/database/schema.sql` define a base atual do banco.
- `controle_ativos/database/migrations/012_rbac_usuarios.sql` adiciona a base de RBAC em `usuarios`.
- `controle_ativos/database/migrations/013_email_responsavel_ativos.sql` adiciona `email_responsavel` em `ativos`.
- `controle_ativos/database/init_db.py` cria o schema, aplica migrations e foi corrigido para drenar resultados pendentes, evitando `Unread result found`.

O inicializador é idempotente no estado atual: pode ser executado novamente sem quebrar o fluxo real do projeto.

## Cuidados com credenciais

- Use variáveis de ambiente para conexão e não versionar `.env`.
- Faça backups regulares antes de alterações estruturais.

## Observação

- O banco recomendado para o TCC é `tcc`.
- Não reutilize a base legada `controle_ativos` como se fosse o ambiente atual do projeto.
