# Cronograma do Projeto

Este cronograma consolida o andamento do TCC com base no estado atual do repositório e da documentação técnica.

## Resumo executivo

- O núcleo funcional do sistema está implementado (Flask + MySQL com operações centrais de ativos).
- O projeto possui autenticação, CRUD de ativos, dashboard e documentação técnica organizada em `docs/`.
- A interface web Flask já existe com páginas de login, dashboard e áreas do sistema; ela continua em evolução junto da migração de autenticação.
- Há evolução de segurança documentada (Bearer Token, rate limit, política de senha e mensagens genéricas), porém a migração para Bearer permanece **gradual** e não deve ser tratada como 100% finalizada.
- A documentação foi reorganizada e o `README.md` principal foi mantido como página inicial enxuta.
- A suíte de testes automatizados possui último estado conhecido registrado em `docs/testes.md`.
- Permanecem pendências acadêmicas e de maturidade (revisão final da monografia, apresentação e evolução profissional do sistema).

## Fases e progresso

| Fase | Entrega / Atividade | Status | Progresso | Evidência / Artefato |
|---|---|---|---|---|
| 1 | Definição do problema e escopo do TCC | Concluído | 100% | `docs/visao-geral.md` |
| 2 | Levantamento do processo atual / AS-IS | Concluído | 100% | `docs/arquitetura.md` |
| 3 | Proposta de processo alvo / TO-BE | Concluído | 100% | `docs/arquitetura.md`, `docs/roadmap.md` |
| 4 | Modelagem da arquitetura do sistema | Concluído | 100% | `docs/arquitetura.md` |
| 5 | Implementação do núcleo funcional | Concluído | 100% | `controle_ativos/web/app.py`, `controle_ativos/services/` |
| 6 | Cadastro, consulta, edição e exclusão de ativos | Concluído | 100% | `controle_ativos/web/app.py`, `controle_ativos/services/ativos_service.py` |
| 7 | Autenticação inicial de usuários | Concluído | 100% | `controle_ativos/services/auth_service.py`, `controle_ativos/web/app.py` |
| 8 | Migração gradual para Bearer Token | Em andamento | 70% | `docs/seguranca.md`, `docs/autenticacao-token.md` |
| 9 | Serviço de tokens opacos | Parcial | 70% | `docs/autenticacao-token.md`, `controle_ativos/security/__pycache__/token_service*.pyc` |
| 10 | Guard/decorator `@token_required` | Parcial | 70% | `docs/autenticacao-token.md`, `controle_ativos/security/__pycache__/auth_guard*.pyc` |
| 11 | Login com emissão de token | Parcial | 70% | `docs/autenticacao-token.md`, `controle_ativos/tests/__pycache__/test_login_token*.pyc` |
| 12 | Logout com revogação de token | Parcial | 70% | `docs/autenticacao-token.md`, `controle_ativos/tests/__pycache__/test_logout_token*.pyc` |
| 13 | Proteção parcial de rotas sensíveis | Parcial | 65% | `docs/seguranca.md`, `docs/autenticacao-token.md` |
| 14 | Rate limit no login | Parcial | 65% | `docs/seguranca.md`, `controle_ativos/tests/__pycache__/test_login_rate_limit*.pyc` |
| 15 | Política de senha forte | Em andamento | 80% | `controle_ativos/utils/validators.py`, `docs/seguranca.md` |
| 16 | Mensagens genéricas para reduzir enumeração | Parcial | 70% | `docs/seguranca.md`, `docs/autenticacao-token.md` |
| 17 | Banco de dados e migrations | Parcial | 75% | `controle_ativos/database/schema.sql`, `controle_ativos/database/init_db.py` (pasta `migrations/` não encontrada) |
| 18 | Testes automatizados | Parcial | 80% | `docs/testes.md`, `controle_ativos/tests/__pycache__/` |
| 19 | Organização da documentação em `docs/` | Concluído | 100% | `docs/README.md` |
| 20 | README principal como índice do projeto | Concluído | 100% | `README.md` |
| 21 | Documentação de governança de TI | Concluído | 100% | `docs/governanca.md` |
| 22 | Documentação de instalação e operação | Concluído | 100% | `docs/instalacao-configuracao.md`, `docs/operacao-uso.md` |
| 23 | Roadmap e limitações | Concluído | 100% | `docs/roadmap.md`, `docs/tcc-analise-tecnica.md` |
| 24 | Revisão final acadêmica / monografia | Em andamento | 70% | `docs/tcc-analise-tecnica.md` |
| 25 | Preparação para apresentação | Em andamento | 65% | `docs/apresentacao/` |
| 26 | Interface web Flask (login, dashboard e páginas do sistema) | Concluído (em evolução) | 85% | `controle_ativos/web/app.py`, `controle_ativos/web/templates/`, `controle_ativos/web/static/` |

## Atividades concluídas

- Definição do escopo do TCC e objetivos do projeto.
- Implementação da aplicação Flask com persistência MySQL.
- Estrutura modular do backend (`web/`, `services/`, `models/`, `database/`, `utils/`).
- Implementação do CRUD de ativos e dashboard básico.
- Interface web inicial em Flask com templates para login, dashboard e páginas do sistema.
- Autenticação inicial de usuários (registro, login, recuperação e logout por sessão).
- Documentação técnica reorganizada em `docs/`.
- Índice principal no `README.md` mantido como entrada limpa do projeto.
- Documentação de segurança, autenticação por token, banco de dados, governança, operação, instalação e roadmap.
- Equipe e responsabilidades registradas no `README.md`.
- Suíte de testes automatizados com último estado conhecido registrado em `docs/testes.md`.

## Atividades em andamento

- Migração completa de sessão Flask para Bearer Token.
- Evolução e refinamento da interface web, mantendo compatibilidade temporária com a camada de sessão.
- Consolidação de evidências de segurança diretamente em código-fonte versionado (além de documentação e artefatos compilados).
- Separação progressiva entre páginas HTML e APIs.
- Validação final da documentação acadêmica.
- Revisão da monografia.
- Preparação da apresentação e acabamento final.

## Atividades pendentes

- Finalizar apresentação para banca (slides, roteiro e ensaio).
- Revisar texto acadêmico final (padronização e consistência).
- Conferir links finais da documentação.
- Validar repositório limpo sem `.env` versionado.
- Resolver pendências de merge/PR, quando existirem.
- Evoluir permissões por perfil (admin/usuário).
- Evoluir logs e auditoria detalhada.
- Revisar melhorias de importação/exportação, se aplicável.
- Planejar deploy interno controlado, se fizer parte da entrega final.

## Itens fora do escopo atual

- Cobertura completa de código com relatório percentual de coverage.
- Controle avançado RBAC completo.
- Auditoria forense completa.
- Conformidade LGPD formal certificada.
- Deploy público em produção.
- Separação completa frontend/backend já concluída.
- WAF, monitoramento centralizado e infraestrutura corporativa avançada.

Os itens acima podem ser tratados como evolução futura, mas não são obrigatórios para a entrega atual do TCC.

## Próximos marcos sugeridos

1. Revisar documentação acadêmica e monografia.
2. Conferir consistência entre `README.md`, `docs/` e o código.
3. Rodar `python -m pytest -q` para atualizar o estado conhecido dos testes.
4. Realizar smoke test manual dos fluxos principais.
5. Conferir `.gitignore` e ausência de `.env` versionado.
6. Finalizar Pull Request para a branch principal.
7. Preparar slides e roteiro de apresentação.

## Observações

- Este cronograma foca estado real de execução, não calendário rígido de datas.
- Percentuais são estimativas de acompanhamento.
- O status de testes deve ser atualizado sempre que a suíte for executada novamente.
