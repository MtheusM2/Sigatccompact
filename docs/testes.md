# Testes Automatizados

Ferramenta: `pytest`

Objetivo

Garantir comportamento esperado de validações, autenticação, rotas e serviços.

Tipos de testes presentes

- Testes de validação (senha, e-mail, campos).
- Testes de autenticação por sessão e serviços.
- Testes de logout e limpeza de sessão.
- Testes de configuração de segurança do Flask.
- Testes de rate limit e CSRF.
- Testes de RBAC e permissões por perfil.
- Testes de busca e filtro de ativos.
- Testes de inicialização do banco e migrations.

Executar suíte

```bash
python -m pytest -q
```

Estado atual

- Suíte validada no estado atual com `python -m pytest -q`.
- Os benchmarks de performance continuam desativados por padrão e só executam com `RUN_PERF_TESTS=1`.
- A camada Flask possui testes de importação, segredo de sessão, campos obrigatórios, proteção das rotas de ativos e caminhos de sucesso com serviços mockados.
- `AuthService` e `AtivosService` possuem testes unitários com cursores fake para validar erros, permissões, filtros, RBAC e atualizações sem depender do MySQL real.
- Há cobertura para a correção do fluxo de busca/filtro, para a inicialização do banco e para o executor de migrations sem `Unread result found`.
- O mapa de cobertura de validação está documentado em [Validação de Rotas e Testes](validacao-rotas-e-testes.md).

Observação

Se os testes forem alterados, atualize este documento com o novo estado e instruções específicas.
