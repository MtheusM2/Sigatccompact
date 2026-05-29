# ADR 0006 - RBAC com perfis e permissoes basicas

## Status

Aceito

## Contexto

O backend ja possui autenticacao, cookies explicitos, CSRF, mensagens genericas, rate limit, tratamento global de erros, auditoria basica e interface web funcional. A necessidade atual e separar o acesso por perfil sem reescrever a arquitetura nem introduzir permissões customizadas por usuario.

## Decisao

Adotar um utilitario central de permissao em `controle_ativos/utils/permissions.py`, com decorators `role_required` e `permission_required`, perfis validos definidos em codigo e validacao de `perfil`/`ativo` na sessao apos o login.

A primeira migracao RBAC adiciona os campos `perfil`, `ativo`, `ultimo_login` e `bloqueado_ate` em `usuarios`, e um script seguro promove o primeiro `SUPER_ADMIN`.

## Consequencias

- O controle de acesso fica declarativo nas rotas principais.
- O login passa a gravar perfil e status ativo na sessao.
- O usuario inativo nao consegue autenticar.
- A listagem de ativos passa a ser global para usuarios autenticados e `criado_por` permanece como metadado de autoria e auditoria.
- O projeto ganha um caminho seguro para inicializar o primeiro `SUPER_ADMIN` sem hardcode.
- A gestao simples de usuarios fica restrita ao `SUPER_ADMIN`.
- A auditoria persistida e permissões customizadas continuam como evolucao futura.
