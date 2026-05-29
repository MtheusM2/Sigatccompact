# ADR 0006 - RBAC com perfis e permissoes basicas

## Status

Aceito

## Contexto

O backend ja possui autenticacao, cookies explicitos, CSRF, mensagens genericas, rate limit, tratamento global de erros e auditoria basica. A proxima etapa de seguranca e separar o acesso por perfil sem reescrever a arquitetura nem introduzir gestao completa de usuarios.

## Decisao

Adotar um utilitario central de permissao em `controle_ativos/utils/permissions.py`, com decorators `role_required` e `permission_required`, perfis validos definidos em codigo e validacao de `perfil`/`ativo` na sessao apos o login.

A primeira migracao RBAC adiciona os campos `perfil`, `ativo`, `ultimo_login` e `bloqueado_ate` em `usuarios`, e um script seguro promove o primeiro `SUPER_ADMIN`.

## Consequencias

- O controle de acesso fica declarativo nas rotas principais.
- O login passa a gravar perfil e status ativo na sessao.
- O usuario inativo nao consegue autenticar.
- O CRUD atual continua funcionando com o filtro de propriedade por `criado_por` nesta fase.
- O projeto ganha um caminho seguro para inicializar o primeiro `SUPER_ADMIN` sem hardcode.
- A gestao de usuarios e a auditoria persistida continuam para fases posteriores.
