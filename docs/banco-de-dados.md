# Banco de Dados

Documento de referência para o estado validado do banco do Sigatccompact.

## Visão geral

- Banco utilizado no projeto: `tcc`.
- Tabelas principais: `usuarios` e `ativos`.
- O esquema inclui RBAC, status de usuário, `email_responsavel` e `criado_por`.

## Migrations e inicialização

- `controle_ativos/database/migrations/012_rbac_usuarios.sql` consolida a base de RBAC em `usuarios`.
- `controle_ativos/database/migrations/013_email_responsavel_ativos.sql` adiciona `email_responsavel` em `ativos`.
- `controle_ativos/database/init_db.py` cria o schema, aplica migrations e foi corrigido para drenar resultados pendentes, evitando `Unread result found`.

## Relação com o projeto

- `criado_por` é metadado de autoria e rastreabilidade.
- A listagem de ativos é global para usuários autenticados, respeitando RBAC.
- As regras de negócio complementares estão em [regras de negócio](requisitos/regras_negocio.md).

## Cuidados com credenciais

- Use variáveis de ambiente para conexão e não versionar `.env`.
- Faça backups regulares antes de alterações estruturais.
