# Riscos Conhecidos de Seguranca

## Contexto

O sistema esta em fase de TCC e deve ser tratado como aplicacao interna/controlada, nao exposta publicamente. O objetivo imediato e consolidar a base Flask/MySQL com autenticacao, CRUD de ativos e RBAC com os perfis `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR`.

Esta lista registra riscos conhecidos para evitar falsa sensacao de seguranca e orientar a ordem de evolucao.

Importacao, exportacao e upload de arquivos estao fora do escopo atual porque nao existem como rotas/servicos no backend analisado. Adicionar exportacao agora criaria superficie de ataque desnecessaria para o objetivo imediato, que e backend seguro + RBAC.

## Riscos que existem hoje

| Risco | Impacto | Severidade | Situacao atual | Mitigacao futura |
| ----- | ------- | ---------- | -------------- | ---------------- |
| Ausencia de CSRF em formularios e endpoints mutaveis. | Um site externo poderia tentar acionar POST/PUT/DELETE usando a sessao do navegador. | Alto | Corrigido com token por sessao e validacao global nas rotas mutaveis. | Manter cobertura de testes ao criar novos endpoints mutaveis. |
| Cookies de sessao nao configurados explicitamente. | Dependencia de defaults e falta de politica clara para HTTPS/producao. | Alto | Corrigido com `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE` e `SESSION_COOKIE_SECURE`. | Revisar apenas se o ambiente HTTPS mudar. |
| Falta de decorator central de autenticacao. | Novas rotas podem esquecer validacao de sessao. | Alto | Corrigido com `login_required` aplicado nas rotas privadas. | Manter padrao deny-by-default em rotas novas. |
| RBAC/perfis basicos. | Usuario autenticado passa a ter niveis diferentes por rota, mas o escopo de ativos ainda e limitado por `criado_por` nesta fase. | Medio | Implementado com campos de perfil, decorators e testes; a gestao de usuarios ainda nao existe. | Evoluir usuarios, auditoria persistida e escopos administrativos em fase posterior. |
| Sem rate limit/bloqueio temporario. | Login e recuperacao ficam mais expostos a tentativa automatizada. | Alto | Corrigido com limite simples em memoria por IP/e-mail e bloqueio temporario. | Evoluir para store compartilhado se o backend escalar horizontalmente. |
| Possivel enumeracao de usuario. | Mensagens diferentes podem indicar se e-mail existe. | Medio | Corrigido com mensagens publicas genericas em login e recuperacao. | Manter log tecnico interno sem expor detalhes ao cliente. |
| Sem logs/auditoria estruturados. | Dificulta investigar alteracoes e falhas. | Alto | Corrigido com logs basicos em aplicacao (emitidos ao logger de auditoria). | Criar tabela/service de auditoria para persistencia e exportacao. |
| `APP_PEPPER` opcional. | Hash continua forte com salt/PBKDF2, mas perde camada extra quando pepper nao existe. | Medio | `_pepper()` retorna vazio se variavel ausente. | Exigir em producao ou validar configuracao. |
| Erro MySQL pode ser retornado ao cliente no registro. | Pode expor detalhe tecnico de banco. | Medio | Corrigido com mensagem generica ao cliente e detalhe apenas em log tecnico. | Manter essa regra nas rotas futuras de cadastro. |
| `.env.example` ausente. | Novos ambientes podem copiar configuracoes inseguras ou incompletas. | Medio | `.env` e ignorado, mas exemplo nao existe. | Criar exemplo com placeholders. |

## Riscos aceitos temporariamente no TCC

| Risco aceito | Justificativa tecnica | Condicao de aceite |
| ------------ | --------------------- | ------------------ |
| Escopo administrativo incompleto. | O pedido atual introduz RBAC basico, mas o CRUD continua limitado por `criado_por` e nao existe gestao completa de usuarios. | Manter o escopo atual, criar rotas administrativas apenas em fase posterior e revisar o modelo de acesso quando necessario. |
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
