# Testes Automatizados

Ferramenta: `pytest`

Objetivo

Garantir comportamento esperado de validações, autenticação, rotas e serviços.

Tipos de testes presentes

- Testes de validação (senha, e-mail, campos).
- Testes de autenticação e token.
- Testes de logout e revogação de token.
- Testes de rate limit (login).
- Testes de rotas e serviços de negócio.

Executar suíte

```bash
python -m pytest -q
```

Último estado conhecido

- Suíte completa: 172 testes aprovados (último estado registrado durante o desenvolvimento). Se desejar validar o número atual, execute o comando acima.

Observação

Se os testes forem alterados, atualize este documento com o novo estado e instruções específicas.