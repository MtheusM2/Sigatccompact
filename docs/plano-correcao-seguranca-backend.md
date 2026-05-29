# Plano de Correcao de Seguranca Backend

## Correcoes obrigatorias antes do RBAC

| Ordem | Item | Risco tratado | Prioridade | Criterio de aceite |
| ----- | ---- | ------------- | ---------- | ------------------ |
| 1 | Criar decorator central `login_required` e aplicar em rotas privadas. | Falha por esquecimento de verificacao manual. | P0 | Toda rota privada retorna 401/redirect padronizado sem sessao; testes cobrem rotas atuais. |
| 2 | Configurar cookies de sessao explicitamente. | Sessao exposta a CSRF/roubo por configuracao implicita. | P0 | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"` e `SESSION_COOKIE_SECURE` habilitavel por ambiente HTTPS. |
| 3 | Adicionar protecao CSRF em POST/PUT/DELETE. | Requisicoes forjadas de outro site. | P0 | Formularios e chamadas `fetch` enviam token; requisicoes mutaveis sem token retornam 400/403. |
| 4 | Unificar resposta publica de falha de login/recuperacao. | Enumeracao de usuarios. | P0 | Usuario inexistente e senha incorreta retornam mensagem generica e mesmo status publico. (implementado) |
| 5 | Implementar rate limit simples para login e recuperacao. | Tentativas automatizadas e forca bruta. | P0 | Apos N falhas por IP/e-mail em janela curta, endpoint retorna bloqueio temporario documentado. (implementado) |
| 6 | Limpar sessao antes de gravar login e manter `session.clear()` no logout. | Fixacao/reuso indevido de sessao. | P0 | Teste confirma sessao antiga removida no login e logout. |
| 7 | Padronizar tratamento de erros e remover detalhe tecnico do cliente. | Exposicao de internals e respostas inconsistentes. | P1 | Cliente recebe mensagens genericas; detalhes tecnicos ficam somente em log tecnico. (implementado) |
| 8 | Criar logs/auditoria basica para eventos sensiveis atuais. | Falta de rastreabilidade para login e CRUD. | P1 | Eventos de login, falha de login, logout e CRUD sao registrados sem senha/resposta/segredo. (implementado) |

Importacao, exportacao e upload nao existem no backend atual e nao fazem parte das correcoes obrigatorias antes do RBAC. O escopo imediato e backend seguro + RBAC: autenticacao, sessao, CSRF, controle de acesso, tratamento de erros e logs/auditoria basica.

A base de RBAC ja foi iniciada neste repositório com migration, script de promocao, utilitario central de permissoes, decorators e testes. A evolucao futura passa a ser gestao de usuarios, auditoria persistida e refinamento de escopos administrativos.

## Correcoes recomendadas para a Fase 1

| Item | Prioridade | Criterio de aceite |
| ---- | ---------- | ------------------ |
| Criar `.env.example` com placeholders seguros. | P1 | Arquivo existe, nao contem segredo real e reflete variaveis usadas. |
| Tornar `APP_PEPPER` obrigatorio em ambiente de producao ou validar configuracao no startup. | P1 | Aplicacao/documentacao diferencia ambiente local e producao. |
| Criar desenho da tabela/service de auditoria antes de operacoes administrativas. | P1 | Documento ou migracao planejada define campos minimos: ator, acao, recurso, resultado, IP, data. |
| Alinhar `controle_ativos/requirements.txt` com os requirements oficiais ou remover arquivo duplicado. | P1 | Uma fonte de verdade de dependencias fica documentada. |
| Padronizar handlers de erro 400, 401, 403, 404 e 500. | P1 | Erros inesperados nao exibem traceback nem detalhe tecnico ao usuario. |
| Planejar campo de usuario ativo/bloqueado. | P1 | Decisao registrada antes do RBAC e do bloqueio por falhas. |

## Correcoes para evolucao futura

| Item | Prioridade | Observacao |
| ---- | ---------- | ---------- |
| Evoluir RBAC com gestao de usuarios e refinamento de escopos administrativos. | P2 | Base de perfis e decorators ja implementada; evoluir telas/rotas administrativas e restricoes adicionais. |
| Consolidar matriz por acao e ampliar cobertura administrativa. | P2 | Separar visualizar, criar, editar, excluir e administrar usuarios. Importacao/exportacao de arquivos ficam fora do backend atual. |
| Exigir reautenticacao para excluir/desativar usuario, alterar perfil e operacoes destrutivas. | P2 | Pode ser simples: confirmar senha atual em tela critica. |
| Criar fluxo seguro de importacao/upload se a funcionalidade for criada. | P3 | Evolucao futura, nao aplicavel no backend atual; validar extensao, tamanho, conteudo, preview, confirmacao e rollback. |
| Exportacao controlada de logs/auditoria. | P3 | Exportacao de relatorios de logs sera considerada apenas apos criacao da tabela/service de auditoria. |
| Adicionar headers basicos de seguranca. | P2 | `X-Content-Type-Options`, `Referrer-Policy` e CSP simples compativel com templates atuais. |
| Alertas para falhas repetidas e acoes destrutivas. | P3 | Para ambiente interno pode iniciar como log destacado. |

## Ordem sugerida de implementacao

1. Decorator `login_required` e padronizacao de erro nao autenticado. (implementado)
2. Configuracao explicita de cookies e segredo/pepper por ambiente. (implementado)
3. CSRF em formularios e endpoints mutaveis. (implementado)
4. Mensagens genericas de login/recuperacao. (implementado)
5. Rate limit em login/recuperacao. (implementado)
6. Limpeza de sessao antes do login e no logout. (implementado)
7. Tratamento global de erros.
8. Logs/auditoria basica de eventos sensiveis atuais.
9. Documentar matriz RBAC.
10. Implementar RBAC.

## Testes que devem ser criados

| Area | Testes recomendados |
| ---- | ------------------- |
| Autenticacao | Falha de login com usuario inexistente e senha errada retorna resposta generica; limite de tentativas bloqueia temporariamente. |
| Sessao | Login limpa dados antigos antes de gravar nova sessao; logout limpa sessao; rotas privadas sem sessao retornam padrao unico. |
| Cookies | Configuracoes `HttpOnly`, `SameSite` e `Secure` conforme ambiente. |
| CSRF | POST/PUT/DELETE sem token falham; com token valido passam. |
| Controle de acesso | Usuario A nao busca, edita ou remove ativo do usuario B. |
| Erros | Erro interno simulado retorna 500 generico sem traceback. |
| Logs | Eventos de login/CRUD sao registrados sem senha, resposta de recuperacao ou segredo. Exportacao de logs nao e exigida nesta etapa. |
| Dependencias | `pip-audit` e `bandit` executam em CI ou roteiro documentado. |

## Riscos conhecidos que ficarao documentados

| Risco | Decisao temporaria | Mitigacao |
| ----- | ------------------ | --------- |
| Sem RBAC no estado atual. | Aceito ate concluir base de sessao/CSRF. | CRUD fica limitado por `criado_por`; RBAC entra depois. |
| Sem CSRF hoje. | Nao aceito para evolucao; corrigir antes do RBAC. | Implementar token em formularios e endpoints mutaveis. |
| Sem rate limit. | Corrigido na Fase 1.3. | Bloqueio simples por IP/e-mail em memoria para login e recuperacao. |
| Sem auditoria detalhada. | Aceito temporariamente no TCC interno. | Criar logs basicos antes de perfis administrativos. |
| Importacao/exportacao/upload nao implementados no backend atual. | Fora do escopo imediato e nao bloqueia RBAC. | Nao criar fluxo de arquivos agora; projetar validacao e confirmacao apenas se a funcionalidade for adicionada futuramente. |
| Exportacao de relatorios de logs. | Evolucao futura dependente de auditoria persistida. | Considerar somente apos criacao da tabela/service de auditoria, com acesso controlado por `SUPER_ADMIN` ou `ADMIN`. |
