# Auditoria de Seguranca OWASP 2025 - Backend Flask/Python

## Resumo executivo

Esta auditoria analisou o backend Flask/Python do sistema de Controle de Ativos com foco em autenticacao, sessao, controle de acesso, validacao, banco MySQL, dependencias e documentacao tecnica. O estado atual tem fundamentos importantes: senhas e respostas de recuperacao sao armazenadas com PBKDF2, salt e suporte a pepper; as principais queries usam parametros; as rotas de ativos exigem sessao; e os servicos filtram ativos por `criado_por`, reduzindo risco de IDOR no CRUD atual.

Os principais riscos antes da evolucao para RBAC sao: ausencia de CSRF em formularios e endpoints mutaveis, configuracoes de cookies de sessao nao explicitadas, falta de decorators centralizados de autenticacao/permissao, ausencia de rate limit/bloqueio temporario no login, mensagens que podem permitir enumeracao de usuario, falta de logs/auditoria de eventos sensiveis e ausencia de reautenticacao para acoes criticas. Nao foi identificada vulnerabilidade critica evidente no codigo analisado, mas ha riscos altos que devem ser tratados antes do RBAC.

## Escopo da auditoria

- Aplicacao Flask: `controle_ativos/web/app.py`.
- Services: `controle_ativos/services/auth_service.py`, `controle_ativos/services/ativos_service.py`.
- Utilitarios: `controle_ativos/utils/crypto.py`, `controle_ativos/utils/validators.py`.
- Banco: `controle_ativos/database/connection.py`, `controle_ativos/database/schema.sql`, `controle_ativos/database/init_db.py`.
- Templates web em `controle_ativos/web/templates/`.
- Dependencias: `requirements.txt`, `requirements-dev.txt`, `controle_ativos/requirements.txt`.
- Testes em `controle_ativos/tests/`.
- Documentacao existente em `docs/`, `README.md` e `.gitignore`.

## Limitacoes da auditoria

- Auditoria estatica e funcional local; nao houve teste exploratorio em navegador real, pentest ativo contra banco real ou ambiente publicado.
- Nao foram alterados backend, arquitetura, banco ou RBAC nesta etapa.
- Arquivo `.env` existe localmente, mas esta ignorado pelo Git; nao foram expostos valores sensiveis neste documento.
- Importacao/exportacao e upload nao foram identificados como rotas/servicos implementados no backend atual. Portanto, itens de fluxo de arquivos sao "Nao aplicavel no backend atual" e nao fazem parte das pendencias obrigatorias P0/P1 nem bloqueiam RBAC.
- O escopo imediato e backend seguro + RBAC: autenticacao, sessao, CSRF, controle de acesso, logs/auditoria basica e, depois, matriz de permissoes.
- A classificacao usa risco pratico para aplicacao Flask interna/controlada, nao para ambiente publico de alta exposicao.

## Mapa OWASP Top 10:2025 aplicado ao projeto

| Categoria | Status geral | Risco geral | Prioridade geral | Sintese |
| --------- | ------------ | ----------- | ---------------- | ------- |
| A01: Broken Access Control | Parcial | Alto | P0 | Rotas de ativos exigem sessao e filtram por usuario, mas nao ha decorators centralizados nem papeis/permissoes para separar funcoes sensiveis. |
| A02: Security Misconfiguration | Parcial | Alto | P0 | `FLASK_SECRET_KEY` e debug default seguro existem, mas cookies de sessao, headers e `.env.example` precisam ser formalizados. |
| A03: Supply Chain Failures | Parcial | Medio | P1 | Dependencias raiz estao fixadas e `pip-audit` passou; ha arquivo alternativo com ranges e bibliotecas nao usadas. |
| A04: Cryptographic Failures | Parcial | Medio | P1 | PBKDF2, salt e pepper existem; `APP_PEPPER` nao e obrigatorio e mensagens/logs devem evitar dados sensiveis. |
| A05: Injection | Parcial | Medio | P1 | Queries usam parametros; ordenacao usa allowlist. Validacao e resposta de erro precisam ser endurecidas. |
| A06: Insecure Design | Parcial | Alto | P0 | Falta modelo formal de permissoes, auditoria e reautenticacao para acoes criticas. |
| A07: Authentication Failures | Parcial | Alto | P0 | Login/logout existem, mas sem rate limit, bloqueio temporario, regeneracao explicita de sessao ou controle de usuario inativo. |
| A08: Software and Data Integrity Failures | Parcial | Medio | P1 | Validacoes de ativo existem; falta auditoria e confirmacao para operacoes destrutivas futuras. |
| A09: Logging and Alerting Failures | Nao Atendido | Alto | P1 | Nao foi identificado service/tabela de auditoria nem logs estruturados de login, CRUD ou erros internos. |
| A10: Mishandling of Exceptional Conditions | Parcial | Medio | P1 | Ha tratamento de erros de dominio e rollback; erro de MySQL em registro retorna detalhe tecnico ao cliente. |

## Tabela detalhada por categoria

| Categoria | Item verificado | Evidencia encontrada no codigo | Arquivos analisados | Status | Risco | Prioridade | Recomendacao |
| --------- | --------------- | ------------------------------- | ------------------- | ------ | ----- | ---------- | ------------ |
| A01 | Rotas internas exigem login | `/dashboard` e subrotas chamam `_render_pagina_sistema`, que valida `user_id` na sessao; rotas `/ativos` retornam 401 sem usuario. | `controle_ativos/web/app.py:64`, `controle_ativos/web/app.py:70`, `controle_ativos/web/app.py:230` | Parcial | Medio | P1 | Centralizar em decorator `login_required` para reduzir esquecimento em novas rotas. |
| A01 | Controle contra IDOR em ativos | `listar_ativos` usa `WHERE criado_por = %s`; busca compara `row["criado_por"]` com `user_id`; update/delete usam `WHERE id=%s AND criado_por=%s`. | `controle_ativos/services/ativos_service.py:108`, `controle_ativos/services/ativos_service.py:144`, `controle_ativos/services/ativos_service.py:266`, `controle_ativos/services/ativos_service.py:294` | Atendido | Baixo | P2 | Manter testes de acesso cruzado entre usuarios para buscar/editar/excluir. |
| A01 | Separacao entre visualizar/criar/editar/excluir | A permissao atual e apenas estar autenticado; nao ha roles, `role_required` ou `permission_required`. | `controle_ativos/web/app.py:230`, `controle_ativos/web/app.py:247`, `controle_ativos/web/app.py:306`, `controle_ativos/web/app.py:333` | Nao Atendido | Alto | P0 | Antes do RBAC, criar camada central de autenticacao; depois mapear permissoes por acao. |
| A01 | Politica deny-by-default | Nao identificado mecanismo global de bloqueio por padrao; cada rota verifica manualmente ou renderiza login. | `controle_ativos/web/app.py` | Parcial | Alto | P0 | Definir padrao: rotas privadas exigem decorator; rotas publicas ficam explicitamente marcadas. |
| A02 | DEBUG desativado por padrao | `app.run` usa `FLASK_DEBUG` e default `"false"`. Teste verifica que `FLASK_DEBUG` nao esta ativo por padrao. | `controle_ativos/web/app.py:350`, `controle_ativos/tests/test_app_security_config.py` | Atendido | Baixo | P2 | Documentar que producao nao deve usar `FLASK_DEBUG=true`. |
| A02 | `FLASK_SECRET_KEY` obrigatorio | Aplicacao levanta `RuntimeError` quando variavel nao existe. | `controle_ativos/web/app.py:45`, `controle_ativos/web/app.py:47` | Atendido | Baixo | P2 | Manter teste e usar segredo forte fora do Git. |
| A02 | Cookies de sessao | Nao identificado `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` ou `SESSION_COOKIE_SECURE` configurados explicitamente. | `controle_ativos/web/app.py` | Parcial | Alto | P0 | Definir `HttpOnly=True`, `SameSite=Lax` inicialmente e `Secure=True` em HTTPS/producao. |
| A02 | `.env` fora do versionamento e exemplo seguro | `.gitignore` ignora `.env`; `git ls-files` nao lista `.env`; nao foi encontrado `.env.example`. | `.gitignore:13`, `.gitignore:15`, `git ls-files`, `rg --files -g ".env.example"` | Parcial | Medio | P1 | Criar `.env.example` com placeholders, sem valores reais. |
| A02 | Exposicao de erro tecnico | Registro captura `mysql.connector.Error`, imprime erro e retorna `str(erro)` ao cliente. | `controle_ativos/web/app.py:168`, `controle_ativos/web/app.py:170` | Parcial | Medio | P1 | Retornar mensagem generica ao usuario e registrar detalhe apenas em log tecnico. |
| A02 | Headers basicos de seguranca | Nao identificado `after_request` para headers como `X-Content-Type-Options`, `Referrer-Policy` ou CSP basica. | `controle_ativos/web/app.py` | Nao Atendido | Baixo | P2 | Adicionar headers simples compativeis com Flask interno. |
| A03 | Dependencias fixadas | `requirements.txt` raiz fixa Flask, mysql-connector e python-dotenv; `requirements-dev.txt` fixa pytest, bandit e pip-audit. | `requirements.txt`, `requirements-dev.txt` | Atendido | Baixo | P2 | Usar os arquivos raiz como fonte principal para CI e ambiente. |
| A03 | Dependencias com ranges e bibliotecas extras | `controle_ativos/requirements.txt` usa ranges e inclui `openpyxl`, `reportlab`, `waitress`, `PyJWT`, nao identificados como imports reais na aplicacao atual. | `controle_ativos/requirements.txt`, `docs/RELATORIO_REQUIREMENTS_OFICIAIS.md` | Parcial | Medio | P1 | Remover/arquivar arquivo alternativo ou alinhar com dependencias realmente usadas. |
| A03 | Auditoria de dependencias | `python -m pip_audit -r requirements.txt -r requirements-dev.txt` retornou "No known vulnerabilities found". | Execucao local em 2026-05-28 | Atendido | Baixo | P2 | Documentar execucao periodica no fluxo de testes. |
| A03 | Analise estatica | `python -m bandit -r controle_ativos ... -lll` nao reportou issues no perfil executado. | Execucao local em 2026-05-28 | Parcial | Baixo | P2 | Rodar Bandit no CI e revisar tambem severidade media quando aplicavel. |
| A04 | Hash de senha | `gerar_hash` usa PBKDF2-SHA256 com 600000 iteracoes, salt aleatorio e formato versionado. | `controle_ativos/utils/crypto.py:6`, `controle_ativos/utils/crypto.py:7`, `controle_ativos/utils/crypto.py:20`, `controle_ativos/utils/crypto.py:33` | Atendido | Baixo | P2 | Manter PBKDF2 e revisar iteracoes periodicamente. |
| A04 | Uso de salt e comparacao segura | Salt vem de `os.urandom`; verificacao usa `hmac.compare_digest`. | `controle_ativos/utils/crypto.py:20`, `controle_ativos/utils/crypto.py:61` | Atendido | Baixo | P2 | Manter testes de hash e verificacao. |
| A04 | Pepper | `_pepper()` le `APP_PEPPER`, mas retorna string vazia se ausente. | `controle_ativos/utils/crypto.py:12` | Parcial | Medio | P1 | Tornar `APP_PEPPER` obrigatorio em ambiente produtivo ou documentar exigencia minima. |
| A04 | Senhas em texto puro | Nao identificado armazenamento de senha pura; cadastro grava `senha_hash` e recuperacao grava hash da resposta. | `controle_ativos/services/auth_service.py:57`, `controle_ativos/services/auth_service.py:70` | Atendido | Baixo | P2 | Evitar logar payloads de autenticacao. |
| A04 | Segredos versionados | `.env` local existe, mas `.gitignore` ignora e `git ls-files` nao lista `.env`. | `.gitignore:13`, `git ls-files` | Parcial | Medio | P1 | Criar `.env.example` e revisar historico Git antes de publicar. |
| A05 | SQL Injection | Queries usam parametros `%s`; filtros constroem SQL com allowlist para ordenacao. | `controle_ativos/services/auth_service.py:62`, `controle_ativos/services/ativos_service.py:226`, `controle_ativos/services/ativos_service.py:219` | Parcial | Baixo | P2 | Manter parametros e testes para filtros; evitar interpolar entrada direta em SQL. |
| A05 | Concatenacao em SQL | `filtrar_ativos` concatena `WHERE` e `ORDER BY`, mas `ORDER BY` vem de dicionario controlado e valores ficam em parametros. | `controle_ativos/services/ativos_service.py:149`, `controle_ativos/services/ativos_service.py:221` | Parcial | Baixo | P2 | Preservar allowlist e rejeitar campos nao mapeados. |
| A05 | Command Injection | Nao identificado uso de `os.system` ou subprocess na aplicacao; subprocess aparece em testes. | `rg` no codigo, `controle_ativos/tests/test_app_security_config.py` | Atendido | Baixo | P3 | Manter proibicao de shell com entrada de usuario. |
| A05 | Upload/path traversal | Nao identificado endpoint de upload/importacao no backend atual. | `controle_ativos/web/app.py`, `controle_ativos/services/` | Nao Aplicavel no backend atual | Baixo | P3 | Nao e correcao obrigatoria imediata. Se a funcionalidade for criada futuramente, validar extensao, tamanho, nome e conteudo. |
| A06 | Modelo formal de permissoes | Nao ha colunas de perfil, decorators de role ou matriz de permissoes implementada. | `controle_ativos/database/schema.sql`, `controle_ativos/web/app.py` | Nao Atendido | Alto | P0 | Documentar matriz antes do RBAC e implementar depois de corrigir base de sessao/CSRF. |
| A06 | Validacao no service | `AtivosService` chama `validar_ativo`; `AuthService` valida email, senha e textos. | `controle_ativos/services/ativos_service.py:76`, `controle_ativos/services/auth_service.py:45` | Atendido | Baixo | P2 | Manter regras no service, nao apenas na rota. |
| A06 | Usuario inativo/bloqueado | Schema de `usuarios` nao possui campo de ativo/bloqueado; login nao verifica estado. | `controle_ativos/database/schema.sql:7`, `controle_ativos/services/auth_service.py:78` | Nao Atendido | Medio | P1 | Planejar campos `ativo`/`bloqueado_ate` antes de politica de bloqueio. |
| A06 | Auditoria de acoes sensiveis | Nao identificado service/tabela de auditoria para CRUD, login ou alteracao de usuario. | `controle_ativos/database/schema.sql`, `controle_ativos/services/` | Nao Atendido | Alto | P1 | Criar trilha minima antes de expor operacoes administrativas. |
| A07 | Login/logout | Login autentica via service e grava `user_id`/`email`; logout executa `session.clear()`. | `controle_ativos/web/app.py:173`, `controle_ativos/web/app.py:186`, `controle_ativos/web/app.py:199`, `controle_ativos/web/app.py:204` | Parcial | Medio | P1 | Limpar sessao antes de login e avaliar regeneracao de sessao. |
| A07 | Politica de senha | `validar_senha` exige 8 a 128 caracteres; nao exige complexidade. | `controle_ativos/utils/validators.py:22` | Parcial | Medio | P1 | Para TCC interno, manter simples mas exigir tamanho adequado e documentar; opcionalmente adicionar criterio leve. |
| A07 | Rate limit/bloqueio | Nao identificado rate limit, contador de falhas ou bloqueio temporario. | `controle_ativos/web/app.py`, `controle_ativos/services/auth_service.py` | Nao Atendido | Alto | P0 | Implementar limite simples por IP/e-mail antes de RBAC. |
| A07 | Enumeracao de usuario | Usuario inexistente gera "Usuario nao encontrado"; senha errada gera mensagem generica. | `controle_ativos/services/auth_service.py:93`, `controle_ativos/services/auth_service.py:96` | Parcial | Medio | P1 | Unificar resposta publica de falha de login e recuperacao. |
| A07 | Recuperacao de senha | Redefinicao usa resposta de recuperacao hasheada e valida nova senha; nao exige sessao nem fator adicional. | `controle_ativos/services/auth_service.py:121`, `controle_ativos/services/auth_service.py:138`, `controle_ativos/web/app.py:208` | Parcial | Medio | P1 | Limitar tentativas e evitar revelar existencia de e-mail. |
| A08 | Integridade de dados de ativos | Validadores cobrem campos obrigatorios, status permitido e datas coerentes. | `controle_ativos/utils/validators.py`, `controle_ativos/services/ativos_service.py:76` | Parcial | Baixo | P2 | Ampliar testes de regras de negocio e limites. |
| A08 | Importacao em massa | Nao identificado endpoint/servico de importacao no backend atual. | `controle_ativos/web/app.py`, `controle_ativos/services/` | Nao Aplicavel no backend atual | Baixo | P3 | Nao e correcao obrigatoria imediata. Quando existir, exigir pre-validacao, resumo e confirmacao antes de gravar. |
| A08 | Controle de alteracoes criticas | Schema tem `criado_em`/`atualizado_em`, mas nao registra quem alterou ou historico. | `controle_ativos/database/schema.sql:13`, `controle_ativos/database/schema.sql:30` | Parcial | Medio | P1 | Criar auditoria de alteracao para ativos e usuarios. |
| A09 | Logs de login/falha | Nao identificado `logging` estruturado ou tabela de eventos para login/falha. | `controle_ativos/web/app.py`, `controle_ativos/services/auth_service.py` | Nao Atendido | Alto | P1 | Registrar evento, usuario/e-mail normalizado, resultado, IP e timestamp sem senha. |
| A09 | Logs de CRUD e auditoria | Nao identificado log de criacao, edicao ou exclusao. | `controle_ativos/services/ativos_service.py` | Nao Atendido | Alto | P1 | Criar service de auditoria e chamadas nas operacoes sensiveis atuais. |
| A09 | Exportacao de logs/auditoria | Nao existe tabela/service de auditoria persistida nem endpoint de exportacao no backend atual. | `controle_ativos/database/schema.sql`, `controle_ativos/services/`, `controle_ativos/web/app.py` | Evolucao futura | Baixo | P3 | Considerar somente apos a auditoria persistida existir, com acesso controlado por `SUPER_ADMIN` ou `ADMIN`. |
| A09 | Alertas basicos | Nao identificado alerta para falhas repetidas, erros internos ou acoes destrutivas. | Codigo analisado | Nao Atendido | Medio | P2 | Planejar alerta simples por log/contador para ambiente interno. |
| A10 | Tratamento 400/401/404 | Rotas traduzem `KeyError`, erros de auth e erros de ativos para status HTTP coerentes em varios pontos. | `controle_ativos/web/app.py:158`, `controle_ativos/web/app.py:193`, `controle_ativos/web/app.py:300` | Parcial | Baixo | P2 | Padronizar handlers globais para 400/401/403/404/500. |
| A10 | Rollback/transacao | Context manager desativa autocommit, faz commit no sucesso e rollback em excecao. | `controle_ativos/database/connection.py:103`, `controle_ativos/database/connection.py:105`, `controle_ativos/database/connection.py:109` | Atendido | Baixo | P2 | Manter operacoes criticas dentro do context manager. |
| A10 | Exposicao de erro interno | Registro retorna detalhe de erro MySQL ao usuario. | `controle_ativos/web/app.py:170` | Parcial | Medio | P1 | Retornar erro generico e logar detalhe no servidor. |
| CSRF | Formularios POST e endpoints mutaveis | Templates usam `fetch` para `/login`, `/register`, `/forgot-password` e `/ativos`; nao foi identificado token CSRF. | `controle_ativos/web/templates/auth/login.html:56`, `controle_ativos/web/templates/auth/register.html:62`, `controle_ativos/web/templates/auth/recovery.html:57`, `controle_ativos/web/templates/dashboard.html:67` | Nao Atendido | Alto | P0 | Adicionar protecao CSRF para POST/PUT/DELETE antes de ampliar perfis. |
| SameSite | SameSite nos cookies | Nao identificado `SESSION_COOKIE_SAMESITE` configurado explicitamente. | `controle_ativos/web/app.py` | Parcial | Alto | P0 | Usar `Lax` no curto prazo; avaliar `Strict` para telas administrativas internas. |
| Acoes criticas | Reautenticacao/confirmacao | Exclusao exige sessao, mas nao reautenticacao; alteracao de senha por recuperacao nao exige senha atual. | `controle_ativos/web/app.py:333`, `controle_ativos/web/app.py:208` | Parcial | Alto | P0 | Exigir confirmacao explicita e, para futuras acoes administrativas, reautenticacao. |

## Evidencias de verificacao executadas

| Verificacao | Resultado |
| ----------- | --------- |
| `python -m pytest` | 59 testes aprovados, 1 ignorado. |
| `python -m bandit -r controle_ativos -x "controle_ativos/tests,tests,controle_ativos/.venv,.venv,venv" -lll` | Sem issues reportadas no perfil executado. |
| `python -m pip_audit -r requirements.txt -r requirements-dev.txt` | Nenhuma vulnerabilidade conhecida encontrada. |
