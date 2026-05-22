# Funcionalidades

Funcionalidades implementadas

- Autenticação de usuários (login/logout).
- Cadastro de usuários e recuperação de conta (fluxos básicos).
- CRUD de ativos: cadastro, listagem/consulta, edição e exclusão.
- Dashboard com visão resumida de ativos.
- Validações de entrada centralizadas (validators).
- Importação/exportação (quando disponível no repositório).
- Suíte de testes automatizados (pytest).

Funcionalidades em evolução

- Migração gradual para autenticação por Bearer Token (APIs protegidas já aceitam tokens). 
- Melhorias de segurança (rate limit, política de senha).

Funcionalidades planejadas

- API REST totalmente separada da interface HTML.
- Controle granular de permissões (roles/admin).
- Logs e auditoria mais detalhados.

Observação

Esta lista reflete o estado atual do código no repositório; não documente funcionalidades que não existam no código. Consulte `controle_ativos/README.md` para descrições originais e exemplos de uso.