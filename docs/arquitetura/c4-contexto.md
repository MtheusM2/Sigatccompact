# C4 - Contexto

## Objetivo

Mostrar o sistema de Controle de Ativos no contexto do uso acadêmico e interno.

```mermaid
flowchart LR
    usuario[Usuário do sistema]
    gestor[Administrador / operador]
    sistema[Sistema de Controle de Ativos]
    mysql[(MySQL)]
    github[GitHub Actions]

    usuario -->|consulta e cadastro| sistema
    gestor -->|administra ativos e acessos| sistema
    sistema -->|persiste dados| mysql
    github -->|valida CI e segurança| sistema
```

## Leitura do diagrama

- O sistema atende usuários autenticados e administradores operacionais.
- A persistência é feita em MySQL.
- A governança do repositório é reforçada por automação no GitHub.
