# Auditoria da Interface e Templates

## Resumo executivo

A interface atual já representa o estado real do backend: o layout base é compartilhado, o dashboard mostra o contexto do usuário logado, a listagem de ativos é global, a busca foi corrigida para filtros opcionais reais, a edição e exclusão saem da tabela quando aplicável, `SUPER_ADMIN` possui gestão simples de usuários e a tela de auditoria mostra eventos recentes em memória.

As limitações são intencionais para o TCC: não há SPA, não há frontend framework, não há auditoria persistida e não há console administrativo complexo.

## Templates analisados

| Arquivo | Tela | Usa CSRF | Usa sessao | Status | Observacao |
| ------- | ---- | -------- | ---------- | ------ | ---------- |
| `controle_ativos/web/templates/base.html` | Layout base | Sim | Indiretamente | Funcional | Centraliza estrutura, navegação e mensagens comuns. |
| `controle_ativos/web/templates/auth/login.html` | Login | Sim | Nao diretamente | Funcional | Formulario assincrono com `fetch` e header `X-CSRF-Token`. |
| `controle_ativos/web/templates/auth/register.html` | Cadastro de usuario | Sim | Nao diretamente | Funcional | Mantem o mesmo padrao visual do login. |
| `controle_ativos/web/templates/auth/recovery.html` | Recuperacao de senha | Sim | Nao diretamente | Funcional | Mantem o mesmo padrao visual do login. |
| `controle_ativos/web/templates/dashboard.html` | Shell principal do dashboard | Sim | Indiretamente | Funcional | Carrega fragmentos via `fetch`, mostra perfil/e-mail e aciona a busca filtrada. |
| `controle_ativos/web/templates/sistema/status_ativos.html` | Cards e tabela global | Nao no fragmento | Nao | Funcional | Exibe a listagem global e as acoes por perfil. |
| `controle_ativos/web/templates/sistema/cadastrar_ativos.html` | Cadastro de ativos | Nao no fragmento | Nao diretamente | Funcional | Mantem o fluxo simples com selects e `email_responsavel`. |
| `controle_ativos/web/templates/sistema/buscar_ativos.html` | Busca de ativos | Nao | Nao | Funcional | Comeca com selects vazios e reflete filtros opcionais reais. |
| `controle_ativos/web/templates/sistema/editar_ativos.html` | Edicao de ativos | Nao | Nao | Funcional | Carrega o ativo selecionado pela tabela e usa selects consistentes. |
| `controle_ativos/web/templates/sistema/excluir_ativos.html` | Exclusao de ativos | Nao | Nao | Funcional | Carrega o ativo selecionado pela tabela e evita digitacao manual do ID. |
| `controle_ativos/web/templates/sistema/usuarios.html` | Gestao de usuarios | Sim | Sim | Funcional | Restrita ao `SUPER_ADMIN`. |
| `controle_ativos/web/templates/sistema/auditoria.html` | Auditoria recente | Nao | Sim | Funcional | Mostra eventos recentes em memoria para `ADMIN` e `SUPER_ADMIN`. |
| `controle_ativos/web/templates/errors/generic.html` | Erro generico | Nao | Nao | Funcional | Mantem o padrao visual do restante do app. |

## Principais achados

- A tabela global não depende mais de autoria para aparecer.
- Editar e excluir não exigem digitação manual do ID quando a linha já foi selecionada.
- Os formulários de ativos compartilham os mesmos campos operacionais, inclusive `email_responsavel`.
- A busca foi corrigida para aceitar filtros parciais e combinados.
- A tela de usuários é propositalmente simples e restrita ao `SUPER_ADMIN`.
- A tela de auditoria é propositalmente simples e usa eventos recentes em memória.

## Riscos e notas

- A auditoria ainda não é persistida.
- O dashboard ainda depende de carregamento de fragmentos via `fetch`.
- O backend segue como fonte de verdade para RBAC e CSRF.

## Atualização de estado

- Depois da reorganização da interface, o projeto passou a usar `base.html`, lista global de ativos, ações por linha, gestão simples de usuários, auditoria simples e busca filtrada funcional.
