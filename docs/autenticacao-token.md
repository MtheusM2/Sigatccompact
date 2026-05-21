# Autenticação por Token

Visão geral

O projeto usa tokens opacos para proteger APIs. O token é gerado no login e enviado ao cliente; apenas o hash do token é armazenado no banco de dados.

Fluxo (conceitual)

1. Usuário realiza login com credenciais.
2. O servidor valida as credenciais e gera um token opaco (valor aleatório).
3. O servidor armazena apenas o hash do token no banco (ex.: `auth_tokens`).
4. O cliente armazena o token em `sessionStorage` (frontend) e o envia em requisições protegidas:

```
Authorization: Bearer <token>
```

5. O decorator `@token_required` valida o header `Authorization`, compara o hash e popula `g.usuario_id` para uso nos handlers.
6. No logout, o token é revogado/invalidado no banco; tokens revogados deixam de funcionar.

Vantagens

- Tokens opacos evitam expor informações internas quando comparados a JWTs sem assinatura adequada.
- Armazenar apenas hash reduz risco em caso de vazamento do banco.

Observações operacionais

- Não coloque exemplos de tokens reais na documentação.
- A migração para Bearer Token está em andamento; algumas rotas ainda aceitam sessões por compatibilidade.