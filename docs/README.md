# Documentação - Sistema de Controle de Ativos

Pasta com documentação técnica e acadêmica do projeto.

Ordem de leitura sugerida (para banca / avaliadores):

1. [Visão Geral](visao-geral.md) (contexto e escopo)
2. [Funcionalidades](funcionalidades.md) (o que o sistema faz hoje)
3. [Arquitetura](arquitetura.md) (organização técnica)
4. [Banco de Dados](banco-de-dados.md) (tabelas e observações)
5. [Segurança](seguranca.md) (medidas e riscos)
6. [Governança](governanca.md) (valor para TI)
7. [Testes](testes.md) (suíte automatizada)
8. [Validação de Rotas e Testes](validacao-rotas-e-testes.md) (mapa de cobertura e lacunas)
9. [Cronograma](cronograma.md) (progresso, pendências e marcos)
10. [Roadmap](roadmap.md) (evoluções planejadas)
11. [Análise Técnica do TCC](tcc-analise-tecnica.md) (documento para apresentação)

Divisão: documentos técnicos e documentos acadêmicos

- Técnicos: Visão Geral, Funcionalidades, Arquitetura, Banco de Dados, Segurança, Testes, Operação e Instalação, Cronograma, Roadmap.
- Acadêmicos: Análise Técnica do TCC, materiais de apresentação (em `apresentacao/`).

Observação sobre autenticação

O projeto opera atualmente com sessão Flask para autenticação e navegação. A ideia de Bearer Token pode ser retomada futuramente, mas não faz parte do fluxo ativo do estado atual.
