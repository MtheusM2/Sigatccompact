# C4 - Container

## Objetivo

Detalhar os principais containers lógicos do projeto.

```mermaid
flowchart TB
    navegador[Navegador / interface web]
    flask[Aplicação Flask]
    servicos[Services de domínio]
    utils[Utils de validação e crypto]
    banco[(MySQL)]
    ci[GitHub Actions]

    navegador --> flask
    flask --> servicos
    flask --> utils
    servicos --> banco
    ci --> flask
```

## Leitura do diagrama

- A interface web conversa com a aplicação Flask.
- A lógica de negócio fica concentrada nos services.
- Validações e funções auxiliares permanecem em utils.
- O banco relacional sustenta a persistência.
