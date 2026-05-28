# ADR 0001 - Uso de Flask e MySQL

## Status

Aceito

## Contexto

O projeto TCC precisa de uma base web simples, modular e compatível com a stack já adotada no repositório. O objetivo é manter o backend leve, com persistência relacional e baixa complexidade operacional, sem criar dependências desnecessárias.

## Decisão

Adotar Flask para a camada web e MySQL como banco relacional do projeto.

## Consequências

- A aplicação permanece fácil de executar e documentar no contexto acadêmico.
- A estrutura modular pode evoluir sem impor um framework pesado.
- A persistência relacional continua adequada ao cadastro e ao controle de ativos.
- Controles de segurança e configuração devem ser tratados explicitamente no repositório e nos ambientes.
