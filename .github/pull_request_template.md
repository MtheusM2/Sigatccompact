## Resumo da alteração

<!-- Descreva de forma objetiva o que mudou e por quê. -->

## Tipo da alteração

- [ ] Documentação
- [ ] CI / DevSecOps
- [ ] Governança / Repositório
- [ ] Correção de bug
- [ ] Refatoração sem mudança funcional

## Checklist de testes

- [ ] `python -m pytest -q`
- [ ] Validação local do arquivo alterado
- [ ] Nenhum teste existente foi quebrado

## Checklist de segurança

- [ ] `bandit` executado quando aplicável
- [ ] `pip-audit` executado quando aplicável
- [ ] Nenhum segredo real foi adicionado ao commit
- [ ] Nenhum `.env` foi versionado

## Impacto em banco

- [ ] Nenhum
- [ ] Apenas documentação
- [ ] Exige revisão de schema ou migração

## Impacto em autenticação/autorização

- [ ] Nenhum
- [ ] Apenas configuração ou documentação
- [ ] Há impacto funcional e foi revisado

## Confirmação final

- [ ] Confirmo que a alteração não adiciona segredos reais nem dependências desnecessárias.
