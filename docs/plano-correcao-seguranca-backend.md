# Plano de Correcao de Seguranca Backend

## Base de seguranca ja entregue

| Item | Status | Observacao |
| ---- | ------ | ---------- |
| `login_required` em rotas privadas | Entregue | O backend ja aplica o controle central de acesso nas rotas privadas. |
| Cookies de sessao explicitos | Entregue | `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` e `SESSION_COOKIE_SECURE` estao documentados e aplicados conforme ambiente. |
| CSRF em rotas mutaveis | Entregue | Formularios e chamadas `fetch` enviam token CSRF. |
| Mensagens genericas de login/recuperacao | Entregue | Evita enumeracao de usuarios. |
| Rate limit em login/recuperacao | Entregue | Bloqueio temporario simples reduz tentativas automatizadas. |
| Limpeza de sessao | Entregue | `session.clear()` e limpeza antes de novo login. |
| Tratamento global de erros | Entregue | Respostas genericas e sem traceback para o usuario final. |
| Logs e auditoria basica | Entregue | Eventos sensiveis sao registrados e a interface mostra eventos recentes em memoria. |

## RBAC entregue

| Item | Status | Observacao |
| ---- | ------ | ---------- |
| Matriz de perfis | Entregue | `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR` estao documentados e implementados. |
| Gestao simples de usuarios | Entregue | Restrita ao `SUPER_ADMIN`. |
| Listagem global de ativos | Entregue | `criado_por` e apenas metadado de autoria. |

## Evolucoes futuras

| Item | Prioridade | Observacao |
| ---- | ---------- | ---------- |
| Auditoria persistida em banco | P2 | Criar tabela/service se a necessidade historica ficar real. |
| Permissoes customizadas por usuario | P2 | Manter como evolucao futura, sem complicar o caso de uso atual. |
| Reautenticacao para acoes criticas | P2 | Pode ser confirmacao de senha atual em telas destrutivas. |
| Exportacao controlada de logs/auditoria | P3 | Considerar apenas depois da auditoria persistida. |
| Headers basicos de seguranca | P2 | `X-Content-Type-Options`, `Referrer-Policy` e CSP simples. |
| Ajuste de `APP_PEPPER` para producao | P2 | Validar obrigatoriedade se o projeto sair do contexto academico. |
| Interface administrativa mais rica | P3 | Evolucao natural, mas nao necessaria para o TCC atual. |

## Ordem de referencia para a documentacao

1. Base segura e controles de entrada.
2. RBAC por perfil.
3. Auditoria simples em memoria.
4. Evolucoes futuras apenas se houver demanda real.

## Testes que continuam relevantes

| Area | Testes recomendados |
| ---- | ------------------- |
| Autenticacao | Falha de login com usuario inexistente e senha errada retorna resposta generica; limite de tentativas bloqueia temporariamente. |
| Sessao | Login limpa dados antigos antes de gravar nova sessao; logout limpa sessao; rotas privadas sem sessao retornam padrao unico. |
| Cookies | Configuracoes `HttpOnly`, `SameSite` e `Secure` conforme ambiente. |
| CSRF | POST/PUT/DELETE sem token falham; com token valido passam. |
| Controle de acesso | Usuario A nao busca, edita ou remove ativo do usuario B. |
| Erros | Erro interno simulado retorna 500 generico sem traceback. |
| Logs | Eventos de login/CRUD sao registrados sem senha, resposta de recuperacao ou segredo. |
| Dependencias | `pip-audit` e `bandit` executam em CI ou roteiro documentado. |

## Riscos documentados

| Risco | Decisao temporaria | Mitigacao |
| ----- | ------------------ | --------- |
| Auditoria nao persistida | Aceito no TCC | Persistir apenas se houver necessidade historica real. |
| Permissoes customizadas ausentes | Aceito no TCC | Manter matriz por perfil e evoluir depois, se necessario. |
| Reautenticacao ausente | Aceito no TCC | Adicionar em fase futura, se o contexto mudar. |
| Importacao/exportacao/upload fora do escopo | Aceito no TCC | Nao criar superficie extra de ataque agora. |
