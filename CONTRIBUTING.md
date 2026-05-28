# Contribuindo

## Configuração do ambiente

1. Crie um ambiente virtual local.
2. Ative o ambiente.
3. Instale as dependências com `pip install -r requirements.txt` e, se existir, `pip install -r requirements-dev.txt`.
4. Configure as variáveis de ambiente locais necessárias para a execução e os testes, sem versionar segredos reais.

## Como rodar testes

- Execute `python -m pytest -q` na raiz do repositório.
- Se necessário, rode `bandit` e `pip-audit` para validar segurança antes do envio da PR.

## Como criar branch

- Use branches curtas e descritivas.
- Prefira nomes como `docs/...`, `ci/...`, `security/...` ou `fix/...`.
- Baseie a branch na principal em uso no repositório.

## Como fazer commit

- Faça commits pequenos e focados.
- Use mensagens objetivas, como `docs: adiciona SECURITY.md` ou `ci: cria workflow de testes`.
- Não inclua arquivos sensíveis nem chaves em texto plano.

## Como abrir PR

- Preencha o template de pull request.
- Explique o objetivo, o impacto e os testes executados.
- Confirme que não houve mudança de regra de negócio, schema ou templates fora do escopo.

## Validações de segurança

- Rode `bandit` no diretório `controle_ativos`.
- Rode `pip-audit` nos arquivos de dependência aplicáveis.
- Verifique se nenhum segredo real foi incluído no diff.

## Arquivos sensíveis

- Nunca versionar `.env`.
- Use apenas exemplos com placeholders quando for necessário documentar variáveis.
