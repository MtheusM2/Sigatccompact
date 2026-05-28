# C4 - Componentes

## Objetivo

Mostrar os componentes internos mais relevantes do backend.

```mermaid
flowchart LR
    app[web/app.py]
    auth[AuthService]
    ativos[AtivosService]
    crypto[utils/crypto.py]
    validadores[utils/validadores.py]
    conn[database/connection.py]
    models[models/*]

    app --> auth
    app --> ativos
    auth --> crypto
    ativos --> validadores
    auth --> conn
    ativos --> conn
    auth --> models
    ativos --> models
```

## Leitura do diagrama

- `web/app.py` atua como ponto de entrada da camada Flask.
- `AuthService` concentra autenticação e recuperação.
- `AtivosService` concentra as operações do domínio de ativos.
- `crypto` e `validadores` sustentam regras de apoio reutilizáveis.
- `connection.py` mantém a integração com o banco isolada do restante do código.
