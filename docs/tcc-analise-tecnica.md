# Análise Técnica do TCC

Problema

Gestão descentralizada de inventário de TI causa perda de controle e rastreabilidade.

Proposta de solução

Desenvolver um sistema modular para cadastro, consulta e controle de ativos com autenticação de usuários e medidas básicas de segurança.

Justificativa técnica

Escolhas tecnológicas: Python + Flask (rápido para prototipagem e servidor web), MySQL (persistência relacional conhecida e compatível com requisitos acadêmicos).

Arquitetura e componentes

- Camada Web (Flask) para interface e endpoints.
- Serviços para lógica de negócio (`services/`).
- Modelos e persistência em MySQL.

Segurança e testes

Aplica-se hash de senhas, políticas de validação e autenticação por sessão Flask no estado atual; a suíte de testes automatizados fornece verificação de comportamento (ver `docs/testes.md`). A autenticação por token permanece como possibilidade futura de evolução.

Limitações

Ainda não há controle avançado de permissões, auditoria detalhada ou políticas de conformidade completas.

