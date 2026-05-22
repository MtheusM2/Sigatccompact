# Segurança

Visão geral

O projeto adota medidas de segurança, com foco em armazenamento seguro de credenciais e controle básico de acesso.

Medidas aplicadas

- Hash de senhas no armazenamento (não armazenar senhas em texto claro).
- Política mínima de senha forte (validadores no código).
- Rate limit simples aplicado ao endpoint de login para reduzir tentativas automatizadas.
- Tokens opacos para autenticação de API: tokens são gerados e armazenados no banco apenas como hash.
- Logout realiza revogação do token (remoção/invalidade no banco).

Compatibilidade e migração

O sistema está em migração gradual de sessão Flask para Bearer Token. Algumas páginas HTML mantêm compatibilidade temporária com sessão para não quebrar a navegação existente.

Riscos conhecidos

- Implementação não substitui controles formais de produção (ex.: WAF, rotinas de rotação de secrets, monitoramento centralizado).
- Algumas áreas (permissões finas, logs de auditoria) precisam de evolução antes de uso em ambientes regulados.

Próximos passos de segurança

- Concluir migração completa para Bearer Token em APIs e avaliar separação entre UI e API.
- Implementar rotação de chaves/pepper e armazenamento seguro para secrets.
- Adicionar logs de auditoria e controle de acesso por função.

Não exponha segredos

Nunca inclua senhas reais, chaves ou tokens em documentos versionados. Use `.env.example` com placeholders.