# Validacao de rotas e testes

Data da revisao: 2026-05-27

## Objetivo

Registrar a analise da camada Flask, dos servicos e dos testes automatizados relacionados a validacao de entrada.

## Diagnostico

O defeito que impedia a aplicacao de subir a partir de `controle_ativos/web` era de bootstrap/importacao, nao de regra de negocio. O arquivo `controle_ativos/web/app.py` importava o pacote `controle_ativos.*`, mas adicionava a pasta `controle_ativos` ao `sys.path`. Para esse import absoluto funcionar, o Python precisa enxergar a raiz do repositorio.

## Correcao aplicada

- `controle_ativos/web/app.py` agora adiciona a raiz do repositorio ao `sys.path`.
- A logica das rotas, servicos, modelos e validadores nao foi alterada.
- Foi criado teste automatizado para importar o app diretamente a partir da pasta `controle_ativos/web`, reproduzindo o cenario que antes causava `ModuleNotFoundError`.

## Cobertura de validacao adicionada

Foram adicionados testes para:

- Importacao local do Flask app a partir da pasta `web`.
- Campos obrigatorios ausentes em `/register`, `/login` e `/forgot-password`.
- Exigencia de usuario autenticado nas rotas `/ativos`.
- Campo obrigatorio ausente na criacao de ativo via rota Flask.
- Traducao de erros da camada de servico para respostas HTTP em busca, atualizacao e remocao de ativos.
- Caminhos de sucesso das rotas de autenticacao e ativos com servicos mockados.
- `AuthService` com cursor fake para email invalido, senha invalida, duplicidade, login invalido, pergunta de recuperacao e redefinicao de senha.
- `AtivosService` com cursor fake para listagem, busca, permissao negada, filtros, atualizacao e remocao.

## Estado atual das rotas

Rotas de paginas:

- `/`, `/register`, `/recovery`: renderizam templates publicos.
- `/dashboard` e subrotas em `/dashboard/*`: exigem sessao e redirecionam/renderizam login quando nao ha usuario autenticado.

Rotas de autenticacao:

- `POST /register`: valida campos obrigatorios na rota e delega formato/regras ao `AuthService`.
- `POST /login`: valida campos obrigatorios na rota e delega autenticacao ao `AuthService`.
- `POST /logout`: limpa a sessao.
- `POST /forgot-password`: valida campos obrigatorios na rota e delega a redefinicao ao `AuthService`.

Rotas de ativos:

- `GET /ativos`, `POST /ativos`, `GET /ativos/<id>`, `PUT /ativos/<id>`, `DELETE /ativos/<id>`: exigem sessao.
- Criacao valida campos obrigatorios na rota e delega regras completas ao `AtivosService`.
- Busca, atualizacao e remocao delegam validacao de ID, permissao e regras ao `AtivosService`.

## Cobertura consolidada

- `AuthService`: cadastro, normalizacao de email, duplicidade, autenticacao, pergunta de recuperacao e redefinicao de senha.
- `AtivosService`: criacao duplicada, listagem, busca, filtros, atualizacao, remocao, permissao negada e validacoes de ID/status/data.
- `web/app.py`: importacao segura, segredo de sessao, dashboard protegido, campos obrigatorios, rotas autenticadas e serializacao JSON.

## Lacunas remanescentes recomendadas

Prioridade media:

- Testar templates HTML com maior profundidade quando a interface visual estabilizar.
- Adicionar testes de integracao opcionais contra MySQL local em ambiente controlado, separados da suite rapida.

Prioridade baixa:

- Medir cobertura percentual com `pytest-cov` e registrar meta minima de cobertura.
- Criar testes end-to-end quando a camada frontend estiver pronta para automacao.

## Estado verificado

- Data: 2026-05-27
- Comando: `python -m pytest -q`
- Resultado: 59 testes aprovados

## Decisao tecnica

A melhor solucao neste momento e manter a validacao de negocio centralizada nos servicos e deixar a rota Flask responsavel por:

1. Ler payload e sessao.
2. Verificar campos obrigatorios imediatos.
3. Delegar regras ao servico correto.
4. Traduzir excecoes de dominio para respostas HTTP consistentes.

Essa abordagem evita duplicacao de regra entre Flask e servicos, preserva a arquitetura atual e permite que os testes de rota sejam rapidos, sem acoplamento ao banco de dados.
