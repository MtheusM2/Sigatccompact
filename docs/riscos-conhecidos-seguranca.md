# Riscos Conhecidos de Seguranca

## Contexto

O sistema esta em fase de TCC e deve ser tratado como aplicacao interna/controlada, nao exposta publicamente. O objetivo imediato e consolidar a base Flask/MySQL com autenticacao e CRUD de ativos antes de implementar RBAC com os perfis `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR`.

Esta lista registra riscos conhecidos para evitar falsa sensacao de seguranca e orientar a ordem de evolucao.

Importacao, exportacao e upload de arquivos estao fora do escopo atual porque nao existem como rotas/servicos no backend analisado. Adicionar exportacao agora criaria superficie de ataque desnecessaria para o objetivo imediato, que e backend seguro + RBAC.

## Riscos que existem hoje

| Risco | Impacto | Severidade | Situacao atual | Mitigacao futura |
| ----- | ------- | ---------- | -------------- | ---------------- |
| Ausencia de CSRF em formularios e endpoints mutaveis. | Um site externo poderia tentar acionar POST/PUT/DELETE usando a sessao do navegador. | Alto | Nao ha token identificado nos templates ou rotas. | Implementar CSRF antes do RBAC. |
| Cookies de sessao nao configurados explicitamente. | Dependencia de defaults e falta de politica clara para HTTPS/producao. | Alto | Nao ha `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` ou `SESSION_COOKIE_SECURE` no app. | Definir configuracao por ambiente. |
| Falta de decorator central de autenticacao. | Novas rotas podem esquecer validacao de sessao. | Alto | Rotas atuais verificam manualmente ou via helper de renderizacao. | Criar `login_required` e padrao deny-by-default. |
| Sem RBAC/perfis. | Usuario autenticado tem o mesmo nivel funcional nas rotas de ativos. | Alto | Nao ha perfil no schema nem decorators de permissao. | Implementar RBAC apos base P0. |
| Sem rate limit/bloqueio temporario. | Login e recuperacao ficam mais expostos a tentativa automatizada. | Alto | Nao ha contador de falhas. | Limite simples por IP/e-mail. |
| Possivel enumeracao de usuario. | Mensagens diferentes podem indicar se e-mail existe. | Medio | Usuario inexistente gera mensagem especifica no service. | Unificar mensagens publicas. |
| Sem logs/auditoria estruturados. | Dificulta investigar alteracoes e falhas. | Alto | Nao ha tabela/service de auditoria identificado. | Criar logs basicos e depois tabela de auditoria. |
| `APP_PEPPER` opcional. | Hash continua forte com salt/PBKDF2, mas perde camada extra quando pepper nao existe. | Medio | `_pepper()` retorna vazio se variavel ausente. | Exigir em producao ou validar configuracao. |
| Erro MySQL pode ser retornado ao cliente no registro. | Pode expor detalhe tecnico de banco. | Medio | Rota `/register` retorna `str(erro)` em erro de conector. | Mensagem generica ao cliente e detalhe em log. |
| `.env.example` ausente. | Novos ambientes podem copiar configuracoes inseguras ou incompletas. | Medio | `.env` e ignorado, mas exemplo nao existe. | Criar exemplo com placeholders. |

## Riscos aceitos temporariamente no TCC

| Risco aceito | Justificativa tecnica | Condicao de aceite |
| ------------ | --------------------- | ------------------ |
| Ausencia de RBAC no momento. | O pedido atual e auditar e documentar antes de criar perfis; o CRUD atual limita ativos por `criado_por`. | Nao expor publicamente e corrigir P0 antes de implementar RBAC. |
| Sem auditoria completa em banco. | Criar tabela e fluxo de auditoria altera modelo de dados, o que foi excluido desta etapa. | Registrar risco e planejar para Fase 1. |
| Importacao/exportacao/upload de arquivos fora do escopo atual. | Codigo atual nao mostra endpoints de importacao, exportacao ou upload; implementar exportacao agora criaria superficie de ataque desnecessaria. | Manter fora do escopo. Evolucao futura apenas para exportacao controlada de logs/auditoria para `SUPER_ADMIN` ou `ADMIN`, depois da auditoria persistida. |
| Politica de senha simples. | Para ambiente interno/TCC, comprimento minimo ja reduz senhas muito fracas sem criar alta friccao. | Reavaliar antes de uso real por terceiros. |
| Headers de seguranca ainda ausentes. | Sao endurecimento importante, mas menos urgente que CSRF, sessao e controle de acesso. | Implementar apos P0. |

## Justificativa para nao implementar tudo agora

- A etapa atual exige somente auditoria e documentacao, sem mudancas funcionais no backend.
- Alteracoes como RBAC, auditoria persistida, usuario inativo/bloqueado e reautenticacao podem exigir mudancas de schema e fluxo de negocio.
- Corrigir controles de base primeiro evita construir RBAC sobre sessoes, CSRF e logs ainda incompletos.
- Para TCC, e melhor ter risco bem documentado, criterio de aceite claro e evolucao incremental do que introduzir arquitetura complexa sem testes suficientes.

## Plano de mitigacao futuro

| Fase | Mitigacao |
| ---- | --------- |
| Antes do RBAC | `login_required`, cookies explicitos, CSRF, mensagens genericas, rate limit e limpeza de sessao no login. |
| Fase 1 de seguranca | `.env.example`, logs basicos, tratamento global de erros, pepper obrigatorio em producao e alinhamento de dependencias. |
| Apos base segura | RBAC com matriz de permissoes, `role_required`/`permission_required`, usuario ativo/bloqueado e reautenticacao para acoes criticas. |
| Evolucao futura | Auditoria persistida, exportacao controlada de logs/auditoria para `SUPER_ADMIN` ou `ADMIN`, alertas basicos e headers de seguranca mais completos. |

## Observacao operacional

Enquanto esses riscos estiverem pendentes, o sistema deve permanecer em ambiente interno/controlado, com acesso restrito, sem exposicao publica direta e sem dados sensiveis reais de terceiros. Qualquer uso fora desse contexto deve ser precedido pela correcao dos itens P0 e pela revisao dos itens P1.
