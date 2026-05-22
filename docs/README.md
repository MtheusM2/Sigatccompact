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
8. [Cronograma](cronograma.md) (progresso, pendências e marcos)
9. [Roadmap](roadmap.md) (evoluções planejadas)
10. [Análise Técnica do TCC](tcc-analise-tecnica.md) (documento para apresentação)

Divisão: documentos técnicos e documentos acadêmicos

- Técnicos: Visão Geral, Funcionalidades, Arquitetura, Banco de Dados, Segurança, Testes, Operação e Instalação, Cronograma, Roadmap.
- Acadêmicos: Análise Técnica do TCC, materiais de apresentação (em `apresentacao/`).

Observação sobre autenticação

O projeto está em migração gradual de sessão Flask para Bearer Token (opaco). Algumas rotas e páginas ainda mantêm compatibilidade temporária com sessão para não quebrar a navegação existente. Para detalhes do fluxo de tokens, veja [Autenticação por Token](autenticacao-token.md).
