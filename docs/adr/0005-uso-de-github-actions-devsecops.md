# ADR 0005 - Uso de GitHub Actions e DevSecOps

## Status

Aceito

## Contexto

O repositório precisa de validação contínua, verificação de segurança e rastreabilidade de mudanças sem depender de processos manuais. O uso de GitHub Actions permite automatizar testes, varreduras e checagens de governança.

## Decisão

Adotar GitHub Actions para CI, verificação de segurança e suporte a uma rotina DevSecOps leve no repositório.

## Consequências

- Os testes passam a rodar automaticamente em pull request e push.
- As checagens de segurança podem ser repetidas sem esforço manual.
- O projeto ganha sinalização de risco cedo, antes do merge.
- As permissões do token do workflow permanecem mínimas.
