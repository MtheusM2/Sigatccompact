# ADR 0003 - Segurança antes do RBAC

## Status

Aceito

## Contexto

O projeto ainda está consolidando autenticação, sessão, endurecimento de cookies, CSRF e trilha mínima de riscos. Implementar RBAC completo sem essa base aumentaria a complexidade e poderia esconder vulnerabilidades elementares.

## Decisão

Priorizar controles básicos de segurança antes de introduzir RBAC formal.

## Consequências

- O projeto mantém o foco em reduzir risco estrutural primeiro.
- O trabalho de auditoria fica mais claro e mais fácil de validar.
- O escopo atual evita mudanças de schema e regras de negócio desnecessárias.
- A exposição pública deve permanecer restrita até a correção dos itens P0/P1.
