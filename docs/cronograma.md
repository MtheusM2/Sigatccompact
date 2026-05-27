# Cronograma do Projeto

Este cronograma consolida o andamento do TCC com base no estado atual do repositório e da documentação técnica.

## Resumo executivo

- O núcleo funcional do sistema está implementado (Flask + MySQL com operações centrais de ativos).
- O projeto possui autenticação, CRUD de ativos, dashboard, interface web Flask e documentação técnica reorganizada em `docs/`.
- A interface web Flask já existe com páginas de login, dashboard e áreas do sistema; ela trabalha com sessão no estado atual do projeto.
- A documentação de segurança foi atualizada para refletir a autenticação por sessão Flask como fluxo operacional vigente.
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
| 8 | Autenticação por sessão Flask | Concluído | 100% | `controle_ativos/web/app.py`, `controle_ativos/services/auth_service.py` |
| 9 | Rate limit no login | Planejado | 20% | `docs/seguranca.md`, `controle_ativos/web/app.py` |
| 10 | Política de senha forte | Parcial | 50% | `controle_ativos/utils/validators.py`, `docs/seguranca.md` |
| 11 | Mensagens genéricas para reduzir enumeração | Parcial | 40% | `controle_ativos/web/app.py`, `docs/seguranca.md` |
| 12 | Proteção parcial de rotas sensíveis | Parcial | 50% | `controle_ativos/web/app.py`, `docs/seguranca.md` |
| 13 | Separação futura entre UI e API | Planejado | 20% | `docs/arquitetura.md`, `docs/roadmap.md` |
| 14 | Logs de auditoria mais detalhados | Planejado | 20% | `docs/seguranca.md`, `docs/roadmap.md` |
| 15 | Organização do schema e migrations | Parcial | 50% | `controle_ativos/database/schema.sql`, `controle_ativos/database/init_db.py` |
| 16 | Benchmark e validação automatizada | Concluído | 80% | `controle_ativos/tests/`, `docs/testes.md` |
| 17 | Banco de dados e migrations | Parcial | 50% | `controle_ativos/database/schema.sql`, `controle_ativos/database/init_db.py`, `controle_ativos/database/migrations/` |
| 18 | Testes automatizados | Concluído | 80% | `docs/testes.md`, `controle_ativos/tests/` |
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

- Evolução e refinamento da interface web, mantendo compatibilidade temporária com a camada de sessão.
- Consolidação de evidências de segurança diretamente em código-fonte versionado.
- Implementação/estabilização da pasta `security/` com fontes efetivamente versionadas.
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

- Cobertura completa de código com relatório percentual.
- RBAC completo e formalmente separado.
- Auditoria forense completa.
- Conformidade LGPD formal certificada.
- Deploy público em produção.
- WAF e monitoramento corporativo avançado.
- Separação total frontend/backend já concluída.

Esses pontos podem evoluir depois, mas não fazem parte da entrega obrigatória atual do TCC.

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
