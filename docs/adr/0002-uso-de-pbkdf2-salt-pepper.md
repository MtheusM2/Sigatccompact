# ADR 0002 - Uso de PBKDF2, salt e pepper

## Status

Aceito

## Contexto

O sistema manipula credenciais de usuários e precisa evitar o armazenamento de senhas em texto puro. O projeto também deve suportar configuração por ambiente, mantendo o segredo fora do código-fonte.

## Decisão

Manter o hashing de senha com PBKDF2 e salt único por credencial, somando pepper configurado por variável de ambiente quando disponível.

## Consequências

- O repositório não armazena senhas em claro.
- Um vazamento isolado do banco não expõe imediatamente as credenciais.
- O pepper amplia a proteção operacional quando configurado corretamente.
- A rotação de segredos passa a ser uma preocupação de ambiente e governança.
