# Autenticação por Token

Visão geral

Este documento descreve uma proposta futura de autenticação por token opaco. No estado atual do projeto, a autenticação operacional usa sessão Flask.

Fluxo (conceitual)

1. Usuário realiza login com credenciais.
2. O servidor valida as credenciais e gera um token opaco (valor aleatório).
3. O servidor poderia armazenar apenas o hash do token no banco em uma evolução futura (ex.: tabela `auth_tokens`).
4. O cliente poderia armazenar o token em `sessionStorage` (frontend) e o enviar em requisições protegidas:

```
Authorization: Bearer <token>
```

5. Um decorator `@token_required` poderia validar o header `Authorization`, comparar o hash e popular `g.usuario_id` para uso nos handlers.
6. No logout, o token seria revogado/invalidado no banco; tokens revogados deixariam de funcionar.

Vantagens

- Tokens opacos evitam expor informações internas quando comparados a JWTs sem assinatura adequada.
- Armazenar apenas hash reduz risco em caso de vazamento do banco.

Observações operacionais

- Não coloque exemplos de tokens reais na documentação.
- A migração para Bearer Token permanece como possibilidade futura; algumas rotas ainda aceitam sessões por compatibilidade no estado atual.