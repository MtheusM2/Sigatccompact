# Visão Geral

Problema

Organizações de pequeno e médio porte frequentemente mantêm inventários de ativos em planilhas dispersas, o que causa perda de rastreabilidade, inconsistência de dados e dificuldade para auditoria.

Justificativa do projeto

O DataAssets busca centralizar o cadastro e o controle de ativos de TI (hardware e itens relacionados), reduzindo dependência de planilhas e facilitando rastreabilidade e auditoria.

Público-alvo

- Equipes de TI e gestores que precisam manter inventário de equipamentos.
- Departamentos que requerem rastreabilidade de ativos e histórico de movimentações.

Objetivo geral

Construir um sistema modular que permita cadastrar, consultar, editar e remover ativos, com controle básico de usuários e segurança apropriada ao escopo do TCC.

Objetivos específicos

- Fornecer CRUD de ativos com validações.
- Oferecer autenticação de usuários e mecanismos de recuperação de conta.
- Criar base para migração progressiva para API com Bearer Token.
- Documentar arquitetura e base para apresentação acadêmica.

Escopo atual

Funcionalidades centrais implementadas: cadastro de ativos, edição, exclusão, listagem/consulta, autenticação, dashboard básico e importação/exportação quando aplicável.

Limites do projeto (TCC)

O projeto foca no backend e em uma interface web básica; não se apresenta como solução certificada para ambientes críticos e não implementa, por enquanto, controles avançados de permissão e auditoria completos.