# Segurança

Visão geral

O projeto adota medidas de segurança, com foco em armazenamento seguro de credenciais e controle básico de acesso.

Medidas aplicadas

- Hash de senhas no armazenamento (não armazenar senhas em texto claro).
- Política mínima de senha forte (validadores no código).
- Sessão Flask para navegação e autenticação operacional nas rotas do sistema.
- Logout limpa a sessão do usuário autenticado.
- `FLASK_SECRET_KEY`, `APP_PEPPER` e credenciais de banco são lidos por variáveis de ambiente via `.env` local não versionado.

Compatibilidade e migração

O sistema usa sessão Flask no estado atual do projeto. A migração para Bearer Token pode ser retomada no futuro, mas não faz parte do fluxo ativo hoje.

Riscos conhecidos

- Implementação não substitui controles formais de produção (ex.: WAF, rotinas de rotação de secrets, monitoramento centralizado).
- Algumas áreas (permissões finas, logs de auditoria) precisam de evolução antes de uso em ambientes regulados.

Próximos passos de segurança

- Implementar rate limit no endpoint de login para reduzir tentativas automatizadas.
- Avaliar futuramente se a migração para Bearer Token ainda faz sentido para o escopo final do TCC.
- Implementar rotação de chaves/pepper e armazenamento seguro para secrets.
- Adicionar logs de auditoria e controle de acesso por função.

Não exponha segredos

Nunca inclua senhas reais, chaves ou tokens em documentos versionados. Use `.env.example` com placeholders.
