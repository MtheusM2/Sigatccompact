# RBAC - Perfis e Permissoes

## Objetivo

Documentar a matriz real de acesso atualmente implementada no backend Flask, sem limitar a listagem global de ativos por autoria e sem prometer permissões customizadas que ainda não existem.

## Perfis

### SUPER_ADMIN

- Visualiza todos os ativos.
- Cria, edita e exclui ativos.
- Cria usuários.
- Gerencia usuários.
- Acessa a auditoria simples.

### ADMIN

- Visualiza todos os ativos.
- Cria, edita e exclui ativos.
- Não gerencia usuários.
- Acessa a auditoria simples.

### USUARIO

- Visualiza todos os ativos.
- Cria ativos.
- Edita qualquer ativo.
- Não exclui ativos.
- Não gerencia usuários.
- Não acessa a gestão de usuários.

### LEITOR

- Visualiza dashboard, quantidades e tabela global.
- Não cria, edita ou exclui ativos.
- Não gerencia usuários.
- Não acessa a auditoria administrativa.

## Matriz de permissoes

| Permissao | SUPER_ADMIN | ADMIN | USUARIO | LEITOR |
| --- | --- | --- | --- | --- |
| `dashboard.acessar` | x | x | x | x |
| `ativos.visualizar` | x | x | x | x |
| `ativos.criar` | x | x | x | - |
| `ativos.editar` | x | x | x | - |
| `ativos.excluir` | x | x | - | - |
| `auditoria.ver` | x | x | - | - |
| `usuarios.criar` | x | - | - | - |
| `usuarios.gerenciar` | x | - | - | - |

## Decisoes de modelagem e auditoria

- As verificacoes de acesso continuam centralizadas em `controle_ativos/utils/permissions.py`.
- O login grava `perfil` e `ativo` na sessao, e o logout limpa a sessao inteira.
- Usuario inativo nao autentica.
- A listagem de ativos e global para usuarios autenticados; `criado_por` agora e somente metadado de autoria e auditoria.
- As operacoes de criar, editar e excluir sao registradas em logs tecnicos e refletem na trilha simples de auditoria da interface.
- O primeiro `SUPER_ADMIN` continua sendo promovido por script, sem hardcode de credenciais.
- A gestao de usuarios desta fase e simples e restrita ao `SUPER_ADMIN`.

## Limitacoes atuais

- Nao existe permissao customizada por usuario.
- Nao existe tabela persistida de auditoria historica.
- A tela de auditoria mostra apenas eventos recentes em memoria.
- Nao existe reautenticacao para acoes criticas.

## Proximos passos

- Evoluir permissões customizadas apenas se houver necessidade real depois do TCC.
- Persistir auditoria em banco quando houver demanda de consulta historica.
- Adicionar reautenticacao para operações criticas em fase posterior.

## Referencias

- Migrations: [012_rbac_usuarios.sql](../controle_ativos/database/migrations/012_rbac_usuarios.sql) e [013_email_responsavel_ativos.sql](../controle_ativos/database/migrations/013_email_responsavel_ativos.sql)
- Script de promocao: [promover_super_admin.py](../controle_ativos/scripts/promover_super_admin.py)
- Utilitario central: [permissions.py](../controle_ativos/utils/permissions.py)
