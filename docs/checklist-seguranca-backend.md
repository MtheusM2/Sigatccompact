# Checklist de Seguranca Backend

Legenda: `[x] Atendido`, `[ ] Pendente`, `[~] Parcial`, `[-] Nao aplicavel`.

## Autenticacao

- [x] Cadastro de usuario valida e-mail e senha minima.
- [x] Login valida senha por hash, nao por texto puro.
- [x] Logout limpa a sessao com `session.clear()`.
- [x] Mensagens de login e recuperacao sao genericas; usuario inexistente nao e enumerado.
- [x] Rate limit ou bloqueio temporario apos falhas.
- [ ] Controle de usuario inativo/bloqueado.
- [ ] Reautenticacao para acoes criticas futuras.

## Sessao

- [x] `FLASK_SECRET_KEY` e obrigatorio no startup.
- [x] Rotas privadas verificam `user_id` com decorator central `login_required`.
- [x] Decorator central `login_required` implementado e aplicado nas rotas privadas.
- [x] Limpeza explicita da sessao antes de gravar novo login.
- [x] Testes automatizados adicionados para limpeza de sessao e protecao de rotas.

## Cookies

- [x] `SESSION_COOKIE_HTTPONLY` configurado explicitamente.
- [x] `SESSION_COOKIE_SAMESITE` configurado explicitamente.
- [x] `SESSION_COOKIE_SECURE` habilitado para producao/HTTPS.
- [x] Uso de sessao Flask com politica explicita de cookies.

## CSRF

- [x] Tokens CSRF gerados por sessao e expostos aos templates.
- [x] CSRF em POST `/register`.
- [x] CSRF em POST `/login`.
- [x] CSRF em POST `/forgot-password`.
- [x] CSRF em POST `/ativos`.
- [x] CSRF em PUT/DELETE `/ativos/<id>`.

## Controle de acesso

- [x] Rotas de ativos exigem usuario autenticado.
- [x] Ativos sao filtrados por `criado_por`.
- [x] Update/delete usam `id` e `criado_por`.
- [~] Dashboard exige sessao, mas renderiza login com status 200.
- [ ] Politica deny-by-default.
- [ ] Separacao entre visualizar, criar, editar e excluir.
- [-] Importar/exportar arquivos nao aplicavel no backend atual. Observacao: Funcionalidade nao implementada no backend atual.
- [ ] Decorators `role_required` ou `permission_required`.
- [ ] Matriz futura para `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR`.

## Criptografia

- [x] Senhas armazenadas com PBKDF2-SHA256.
- [x] Salt aleatorio por segredo.
- [x] Comparacao com `hmac.compare_digest`.
- [x] Resposta de recuperacao armazenada como hash.
- [~] Pepper existe via `APP_PEPPER`, mas nao e obrigatorio.
- [ ] Politica de rotacao/gestao de segredos documentada.

## Banco de dados

- [x] Queries principais usam parametros.
- [x] Conexao usa commit/rollback via context manager.
- [x] FK de `ativos.criado_por` para `usuarios.id`.
- [~] Schema tem timestamps, mas nao historico/auditoria completa.
- [ ] Campo de usuario ativo/bloqueado.
- [ ] Tabela/service de auditoria.

## Upload/importacao

- [-] Upload nao aplicavel no backend atual. Observacao: Funcionalidade nao implementada no backend atual.
- [-] Importacao em massa nao aplicavel no backend atual. Observacao: Funcionalidade nao implementada no backend atual.
- [-] Exportacao de arquivos nao aplicavel no backend atual. Observacao: Funcionalidade nao implementada no backend atual.
- [-] Evolucao futura: validacao de extensao, tamanho e conteudo se upload/importacao forem criados.
- [-] Evolucao futura: confirmacao antes de importacao em massa se a funcionalidade for criada.
- [-] Evolucao futura: rollback/transacao especifica para importacao se a funcionalidade for criada.

## Logs/auditoria

- [~] Log estruturado de login.
- [x] Log tecnico de falha de login e recuperacao sem senha/resposta/segredo.
- [ ] Log de logout.
- [ ] Log de criacao, edicao e exclusao de ativos.
- [-] Evolucao futura: Exportacao de logs de auditoria quando a auditoria persistida for implementada.
- [ ] Log de alteracao de usuario/perfil quando RBAC existir.
- [ ] Alertas basicos para falhas repetidas.

## Tratamento de erros

- [x] Erros de dominio sao convertidos para respostas JSON em varias rotas.
- [x] Transacoes fazem rollback em excecao.
- [~] Status 400/401/404 aparecem nas rotas principais.
- [ ] Handlers globais para 400, 401, 403, 404 e 500.
- [ ] Remover detalhe tecnico de erro MySQL retornado ao cliente.
- [ ] Garantir ausencia de traceback para usuario final.

## Dependencias

- [x] `requirements.txt` raiz com versoes fixadas.
- [x] `requirements-dev.txt` inclui `bandit` e `pip-audit`.
- [x] `pip-audit` executado sem vulnerabilidades conhecidas nas dependencias informadas.
- [~] Existe `controle_ativos/requirements.txt` com ranges e bibliotecas nao usadas.
- [ ] Processo periodico documentado para atualizar dependencias.

## Configuracao de ambiente

- [x] `.env` ignorado no `.gitignore`.
- [x] `.env` nao aparece em `git ls-files`.
- [~] Documentacao orienta usar `.env.example`.
- [ ] Criar `.env.example` real com placeholders.
- [x] `FLASK_DEBUG` fica falso por padrao.
- [ ] Validacao de configuracao minima para producao.

## Testes

- [x] Suite atual: 75 testes aprovados.
- [x] Testes cobrem rotas de ativos sem autenticacao.
- [x] Testes cobrem segredo de sessao obrigatorio.
- [x] Testes cobrem hash de senha.
- [x] Testes de CSRF.
- [x] Testes de cookies.
- [x] Testes de rate limit.
- [ ] Testes de acesso cruzado usuario A vs usuario B.
- [ ] Testes de logs/auditoria.
