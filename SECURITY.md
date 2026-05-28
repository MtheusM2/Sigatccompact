# Security Policy

## Escopo do projeto

Este repositório contém o backend acadêmico do projeto de Controle de Ativos em Python, Flask e MySQL. O foco atual é manter o código, a documentação e a automação do repositório sob controle, sem exposição pública de dados sensíveis ou de ambientes produtivos.

## Ambiente interno e controlado

O sistema deve ser tratado como aplicação interna/controlada enquanto os riscos P0 e P1 listados na documentação permanecerem em aberto. Não é recomendado expor este backend diretamente à internet sem revisão de CSRF, sessão, RBAC, logs de auditoria e hardening complementar.

## Como reportar falhas

Relatos de segurança devem ser enviados ao mantenedor do projeto ou ao canal interno do TCC, com descrição objetiva do problema, impacto, evidência mínima e passos para reproduzir. Se o problema envolver credenciais, não compartilhe segredos em texto aberto; descreva apenas o padrão do erro e o contexto.

## Referências de auditoria

Consulte os documentos abaixo para o contexto de risco e priorização:

- [docs/auditoria-seguranca-owasp-2025.md](docs/auditoria-seguranca-owasp-2025.md)
- [docs/plano-correcao-seguranca-backend.md](docs/plano-correcao-seguranca-backend.md)
- [docs/riscos-conhecidos-seguranca.md](docs/riscos-conhecidos-seguranca.md)
- [docs/seguranca.md](docs/seguranca.md)

## Riscos conhecidos

Os riscos conhecidos estão documentados em detalhe nos arquivos de segurança do diretório `docs/`. Entre os pontos já assumidos para a fase atual estão a ausência de RBAC, a necessidade de CSRF, o endurecimento de cookies de sessão e a futura consolidação de auditoria persistida.

## Política de exposição pública

Enquanto houver riscos P0 ou P1 pendentes, o projeto não deve ser exposto publicamente nem tratado como ambiente de produção. A publicação externa só deve ser considerada após revisão dos controles mínimos, validação de segurança e aprovação do mantenedor do TCC.
