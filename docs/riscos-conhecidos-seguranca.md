# Riscos Conhecidos de Seguranca

## Contexto

O sistema esta em fase de TCC e deve ser tratado como aplicacao interna/controlada, nao exposta publicamente. O objetivo imediato e consolidar a base Flask/MySQL com autenticacao, CRUD de ativos e RBAC com os perfis `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR`.

Esta lista registra os riscos que ainda existem de verdade no estado atual, sem repetir itens que ja foram mitigados.

Importacao, exportacao e upload de arquivos continuam fora do escopo atual porque nao existem como rotas/servicos no backend analisado. Adicionar exportacao agora criaria superficie de ataque desnecessaria para o objetivo imediato, que e backend seguro + RBAC.

## Riscos que existem hoje

| Risco | Impacto | Severidade | Situacao atual | Mitigacao futura |
| ----- | ------- | ---------- | -------------- | ---------------- |
| Auditoria persistida ausente. | Nao existe trilha historica de longo prazo para consulta posterior. | Medio | A interface mostra eventos recentes em memoria, mas nao grava em tabela dedicada. | Persistir auditoria em banco se a necessidade historica ficar real. |
| `APP_PEPPER` ainda nao e obrigatorio. | O hash segue forte com PBKDF2 e salt, mas perde uma camada extra de defesa se o pepper nao existir. | Medio | A aplicacao aceita `APP_PEPPER` vazio em alguns ambientes. | Tornar obrigatorio em producao ou validar no startup. |
| Headers de seguranca avançados ausentes. | A aplicacao ainda pode receber melhorias como CSP e `Referrer-Policy`. | Baixo | Nao implementados nesta fase do TCC. | Adicionar em evolucao futura. |
| Permissoes customizadas por usuario inexistentes. | O sistema opera por perfis fixos; isso pode ser pouco flexivel em cenarios maiores. | Medio | O RBAC atual usa perfis padrão e matriz fixa. | Adicionar permissões por usuario apenas se houver demanda real. |
| Reautenticacao para acoes criticas inexistente. | Operacoes destrutivas ainda dependem apenas da sessao atual. | Medio | Ainda nao ha fluxo de confirmacao adicional. | Exigir senha atual ou confirmacao extra em fase futura. |

## Riscos aceitos temporariamente no TCC

| Risco aceito | Justificativa tecnica | Condicao de aceite |
| ------------ | --------------------- | ------------------ |
| Auditoria em memoria. | Para o TCC, a tela recente em memoria cumpre o objetivo de demonstracao sem exigir schema extra. | Aceitar no curto prazo e migrar para persistencia apenas se houver demanda posterior. |
| RBAC por perfil fixo. | A estrategia atual resolve o caso de uso sem introduzir complexidade excessiva. | Manter perfis fixos e deixar permissões customizadas como evolucao futura. |
| Reautenticacao nao implementada. | O fluxo atual atende o objetivo do TCC sem aumentar atrito desnecessario. | Reavaliar apenas se o projeto sair do contexto academico. |
| Importacao/exportacao/upload fora do escopo. | Nao existe funcionalidade real nessa area no backend atual. | Manter fora do escopo e nao criar superficie de ataque desnecessaria. |

## Justificativa para nao implementar tudo agora

- A etapa atual precisa de documentação coerente com o comportamento real, nao de novas funcionalidades.
- Auditoria persistida, permissões customizadas e reautenticacao exigiriam mudancas adicionais de schema e fluxo.
- Para TCC, e melhor manter o escopo controlado e bem documentado do que ampliar a superficie do sistema sem necessidade real.

## Plano de mitigacao futuro

| Fase | Mitigacao |
| ---- | --------- |
| Base segura ja entregue | `login_required`, cookies explicitos, CSRF, mensagens genericas, rate limit, limpeza de sessao, logs basicos e tratamento global de erros. |
| Pos-TCC imediato | Auditoria persistida, permissões customizadas e reautenticacao para acoes criticas. |
| Evolucao futura | Exportacao controlada de logs/auditoria, headers de seguranca mais completos e possivel ajuste de `APP_PEPPER` para producao. |

## Observacao operacional

Enquanto esses riscos permanecerem aceitos, o sistema deve continuar em ambiente interno/controlado, com acesso restrito, sem exposicao publica direta e sem dados sensiveis reais de terceiros. Qualquer uso fora desse contexto deve ser precedido pela revisao dos itens aceitos e pela evolucao das partes ainda futuras.
