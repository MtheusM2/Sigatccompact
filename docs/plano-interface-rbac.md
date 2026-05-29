# Plano de Interface e RBAC

## O que existe hoje

- O layout principal é compartilhado por `base.html`.
- O dashboard mostra usuário, e-mail, perfil e contexto operacional.
- A listagem de ativos é global para usuários autenticados.
- As ações por linha de ativo aparecem conforme o perfil do usuário.
- A busca de ativos foi corrigida e agora trabalha com filtros opcionais reais.
- `SUPER_ADMIN` possui uma tela simples de gestão de usuários.
- Existe uma tela simples de auditoria com eventos recentes em memória.

## Interface principal

### `base.html`

- Centraliza o esqueleto visual das páginas autenticadas e públicas.
- Mantém navegação e mensagens consistentes.
- Evita duplicação de estrutura entre telas.

### Dashboard

- Mostra o contexto do usuário autenticado.
- Carrega fragmentos da área de sistema sem trocar toda a página.
- Exibe cards, tabela global e ações por perfil.
- Mantém a experiência simples e adequada ao TCC.

### Tabela global

- Mostra todos os ativos aos usuários autenticados.
- Usa ações de editar e excluir a partir da linha selecionada, quando permitido.
- Não limita a visibilidade por autoria.

### Busca e filtros

- Os selects começam vazios.
- Campos vazios não filtram.
- `Todos` não é enviado como filtro real.
- Filtros parciais e combinados funcionam.
- A busca deixa de ser apenas visual e passa a refletir o comportamento real do backend.

### Usuários

- `SUPER_ADMIN` é o único perfil com gestão simples de usuários.
- A criação de usuários foi mantida propositalmente direta, sem console administrativo complexo.

### Auditoria

- A tela de auditoria é simples.
- Mostra eventos recentes em memória.
- Não substitui uma trilha histórica persistida em banco.

## Limitações atuais

- Não há SPA nem frontend framework.
- Não há console administrativo avançado.
- A auditoria ainda não é persistida.
- A interface é intencionalmente simples para manter o escopo do TCC controlado.

## Próximos passos futuros

- Persistir auditoria em banco quando a necessidade histórica justificar.
- Evoluir a busca apenas se aparecer uma nova demanda funcional.
- Refinar a área administrativa de usuários apenas se o escopo crescer.