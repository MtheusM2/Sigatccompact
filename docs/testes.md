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

Estado atual

- Suíte executada em 2026-05-27: 59 testes aprovados com `python -m pytest -q`.
- Os benchmarks de performance continuam desativados por padrão e só executam com `RUN_PERF_TESTS=1`.
- A camada Flask possui testes de importação, segredo de sessão, campos obrigatórios, proteção das rotas de ativos e caminhos de sucesso com serviços mockados.
- `AuthService` e `AtivosService` possuem testes unitários com cursores fake para validar erros, permissões, filtros e atualizações sem depender do MySQL real.
- O mapa de cobertura de validação está documentado em [Validação de Rotas e Testes](validacao-rotas-e-testes.md).

Observação

Se os testes forem alterados, atualize este documento com o novo estado e instruções específicas.
