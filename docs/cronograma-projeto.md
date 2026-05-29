# Cronograma Atualizado do Projeto Sigatccompact

Este documento registra o cronograma real e atualizado do projeto Sigatccompact com base no estado atual do repositório, da documentação técnica e da suíte de testes.

## Resumo executivo

O núcleo funcional do sistema já está consolidado: backend Flask/MySQL, autenticação por sessão, CRUD de ativos, RBAC por perfis, CSRF, rate limit, tratamento global de erros, auditoria básica e migrations aplicadas.

A interface web está disponível em ambiente local e passou por refinamentos, mas ainda segue em validação manual para garantir o comportamento esperado com todos os perfis.

Os testes locais já passam com `python -m pytest -q`, e o CI com verificações de segurança existe no GitHub Actions, ainda com validação final de merge dependendo do estado do pipeline.

## Status geral do projeto

- Estado geral: concluído para a entrega acadêmica, com validação final encerrada.
- Situação atual: backend, segurança, banco, RBAC, interface, documentação e CI concluídos; apresentação final pendente.
- Risco principal: manter coerência entre código, documentação e comportamento observado na interface até a defesa.

## Linha do tempo por fases

### Fase 1: definição e planejamento

Definição do problema, escopo acadêmico, objetivo do sistema e organização inicial do TCC.

### Fase 2: base técnica

Estrutura Flask/MySQL, conexão com banco, schema inicial e organização modular do backend.

### Fase 3: funcionalidades centrais

CRUD de ativos, autenticação por sessão, login, logout, recuperação de senha e listagem global.

### Fase 4: segurança base

CSRF, rate limit, tratamento global de erros e ajustes de cookies/sessão.

### Fase 5: RBAC e governança de acesso

Perfis SUPER_ADMIN, ADMIN, USUARIO e LEITOR, além da gestão de usuários.

### Fase 6: interface web e validação de uso

Dashboard, navegação do sistema, filtros, fluxo de edição e uso da interface com perfis reais.

### Fase 7: auditoria e rastreabilidade

Eventos recentes, logs básicos e metadados como `email_responsavel` e `criado_por`.

### Fase 8: documentação técnica

README acadêmico/técnico, documentação em `docs/` e consolidação do material de apoio.

### Fase 9: CI e segurança automatizada

Workflows de GitHub Actions, testes e verificações de segurança.

### Fase 10: fechamento acadêmico

Slides, roteiro, revisão final e preparação para defesa.

## Tabela principal do cronograma

| Fase | Período/Ordem | Status | Entregas | Observações |
| --- | --- | --- | --- | --- |
| Planejamento e escopo | Fase 1 | ✅ Concluído | Definição do sistema e objetivo do TCC | Base conceitual definida |
| Estrutura inicial Flask/MySQL | Fase 2 | ✅ Concluído | Backend, conexão e schema inicial | Ambiente local funcional |
| CRUD de ativos | Fase 3 | ✅ Concluído | Cadastro, listagem, edição e exclusão | Regras ajustadas para tabela global |
| Segurança base | Fase 4 | ✅ Concluído | CSRF, cookies, rate limit, tratamento de erros | Base de segurança aplicada |
| RBAC | Fase 5 | ✅ Concluído | SUPER_ADMIN, ADMIN, USUARIO, LEITOR | Permissões por perfil |
| Interface web | Fase 6 | ✅ Concluído | Dashboard, tabela global, filtros e gestão de usuários | Fluxos validados |
| Auditoria básica | Fase 7 | ✅ Concluído no escopo atual | Eventos recentes/logs | Persistência futura |
| Documentação | Fase 8 | ✅ Concluído | README e docs técnicos | Cronograma incorporado |
| CI/GitHub | Fase 9 | ✅ Concluído | Workflows de CI/security | Checks validados |
| Validação final | Fase 10 | ✅ Concluído | Suíte completa, smoke tests e revisão documental | Versão candidata de entrega |
| Apresentação final | Fase 11 | ⏳ Pendente | Slides, roteiro e defesa | Próxima etapa acadêmica |

## O que já foi concluído

- Backend Flask.
- Banco MySQL.
- CRUD de ativos.
- Login, logout e recuperação de senha.
- CSRF ativo.
- Rate limit em login e recuperação.
- Tratamento global de erros.
- RBAC com SUPER_ADMIN, ADMIN, USUARIO e LEITOR.
- Gestão de usuários para SUPER_ADMIN.
- Campo `email_responsavel` nos ativos.
- Busca e filtros de ativos corrigidos.
- Migrations 012 e 013 aplicadas.
- Executor de migrations corrigido contra `Unread result found`.
- Testes locais passando.
- README acadêmico/técnico refinado.

## O que foi concluído

- Interface no navegador com todos os perfis.
- CI no GitHub.
- Fluxo de cadastro, edição e exclusão.
- Auditoria básica.
- Merge para `main`.
- Validação final com suíte completa e revisão documental.

## O que ainda falta

- Finalizar slides e apresentação.
- Preparar roteiro de defesa.

## O que fica como evolução futura

- Auditoria persistida em banco.
- Exportação de logs.
- Permissões customizadas por usuário.
- Dashboard analítico.
- API REST.
- Frontend SPA.
- SSO.
- LGPD mais detalhada.

## Riscos e cuidados antes do merge/finalização

- Garantir que o CI permaneça verde antes do merge.
- Verificar se a interface web está coerente com os perfis e com o texto do README.
- Revisar se o status das migrations e do executor do banco continua consistente.
- Evitar introduzir divergências entre documentação e comportamento real da aplicação.
- Conferir se não há arquivos temporários, credenciais ou artefatos locais versionados.

## Próximos passos recomendados

1. Confirmar o último ciclo de testes locais.
2. Validar a interface manualmente com os quatro perfis.
3. Acompanhar o CI até a aprovação final.
4. Finalizar merge para `main` quando o pipeline estiver estável.
5. Fechar slides, roteiro e apresentação da banca.
6. Revisar a documentação final antes da entrega acadêmica.

## Observações finais

- Este cronograma prioriza o estado real do projeto, não uma linha do tempo idealizada.
- Os status indicam maturidade atual, validação ou pendência de entrega.
- A documentação deve ser atualizada sempre que o projeto avançar de fase.
