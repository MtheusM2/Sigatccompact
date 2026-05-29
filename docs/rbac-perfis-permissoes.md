# RBAC - Perfis e Permissoes

## Objetivo

Introduzir controle de acesso por perfil no backend Flask sem refatorar a arquitetura inteira e sem quebrar o CRUD atual de ativos.

## Perfis

### SUPER_ADMIN

- Acesso total nas rotas cobertas nesta fase.
- Pode visualizar, criar, editar e excluir ativos.
- Pode futuramente gerenciar usuarios e alterar perfis.
- Pode acessar auditoria administrativa.
- Nao pode ser rebaixado por ADMIN.

### ADMIN

- Pode visualizar, criar, editar e excluir ativos.
- Pode acessar logs/auditoria basica, se a rota existir.
- Nao pode alterar perfis nesta fase.
- Nao pode gerenciar SUPER_ADMIN.

### USUARIO

- Pode visualizar ativos.
- Pode criar ativos.
- Pode editar ativos permitidos pelo fluxo atual.
- Nao pode excluir ativos.
- Nao pode acessar gestao de usuarios.
- Nao pode acessar auditoria administrativa.

### LEITOR

- Pode apenas visualizar dashboard, listagem e detalhes.
- Nao pode criar, editar ou excluir ativos.
- Nao pode acessar auditoria administrativa.
- Nao pode gerenciar usuarios.

## Matriz de permissoes

| Permissao | SUPER_ADMIN | ADMIN | USUARIO | LEITOR |
| --- | --- | --- | --- | --- |
| `dashboard.acessar` | x | x | x | x |
| `ativos.ver` | x | x | x | x |
| `ativos.criar` | x | x | x | - |
| `ativos.editar` | x | x | x | - |
| `ativos.excluir` | x | x | - | - |
| `auditoria.ver` | x | x | - | - |
| `usuarios.gerenciar` | x | - | - | - |
| `usuarios.alterar_perfil` | x | - | - | - |

## Decisoes de seguranca

- As verificacoes de acesso sao centralizadas em `controle_ativos/utils/permissions.py`.
- O login grava `perfil` e `ativo` na sessao, e o logout limpa a sessao inteira.
- Usuario inativo nao autentica.
- O primeiro SUPER_ADMIN e promovido por script seguro, sem hardcode de e-mail ou senha.
- A fase atual nao cria tela complexa de gestao de usuarios.
- A fase atual nao cria exportacao de logs, importacao, upload ou schema de auditoria persistida.
- O controle por `criado_por` continua valido nos servicos de ativos nesta fase para reduzir risco de regressao.

## Limitacoes desta fase

- Nao existe ainda interface administrativa para usuarios.
- Nao existe troca de perfil por rota publica.
- Nao existe persistencia de auditoria em tabela dedicada.
- O escopo de ativos continua limitado pelo fluxo atual de propriedade.
- A gestao de bloqueio temporal por usuario ainda e apenas estrutural.

## Proximos passos

- Criar rotas administrativas seguras para gestao de usuarios.
- Evoluir auditoria para tabela persistida quando houver demanda de consulta historica.
- Reavaliar o escopo de `criado_por` para SUPER_ADMIN/ADMIN em uma proxima fase.
- Se necessario, transformar `bloqueado_ate` em bloqueio temporal efetivo por usuario.
- Adicionar exportacao controlada de auditoria apenas quando a persistencia existir.

## Referencias

- Migration: `controle_ativos/database/migrations/012_rbac_usuarios.sql`
- Script de promocao: `controle_ativos/scripts/promover_super_admin.py`
- Utilitario central: `controle_ativos/utils/permissions.py`
