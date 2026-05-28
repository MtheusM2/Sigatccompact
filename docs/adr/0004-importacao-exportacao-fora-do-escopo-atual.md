# ADR 0004 - Importação e exportação fora do escopo atual

## Status

Aceito

## Contexto

O backend atual concentra autenticação, CRUD de ativos e documentação técnica. Recursos de importação, exportação e upload aumentariam a superfície de ataque sem resolver o objetivo principal da fase atual.

## Decisão

Manter importação, exportação e upload fora do escopo deste momento do projeto.

## Consequências

- A superfície de ataque fica menor.
- O projeto continua focado no núcleo funcional já validado.
- Futuras evoluções dessa área devem ser reavaliadas com controles de autorização e auditoria.
- O repositório evita introduzir complexidade que não faz parte do TCC atual.
