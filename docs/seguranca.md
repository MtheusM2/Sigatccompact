# Segurança

Visão geral

O projeto adota medidas de segurança com foco em autenticação por sessão, proteção de formulários, RBAC por perfil, registro básico de eventos e redução de exposição de detalhes técnicos.

Medidas aplicadas

- Hash de senhas com PBKDF2-SHA256.
- Salt por senha e comparação segura.
- Política mínima de senha validada no código.
- CSRF ativo em rotas mutáveis.
- Cookies de sessão configurados explicitamente.
- Rate limit em login e recuperação.
- RBAC por perfil com `SUPER_ADMIN`, `ADMIN`, `USUARIO` e `LEITOR`.
- Gestão de usuários restrita ao `SUPER_ADMIN`.
- Log técnico e tela simples de auditoria com eventos recentes.
- `FLASK_SECRET_KEY`, `APP_PEPPER` e credenciais de banco são lidos por variáveis de ambiente via `.env` local não versionado.

Estado atual

- O sistema usa autenticação por sessão no estado atual do projeto.
- A listagem de ativos é global para usuários autenticados.
- `criado_por` é metadado de autoria e auditoria, não regra de visibilidade.
- A busca de ativos trabalha com filtros parciais e combinados.

Riscos conhecidos

- Auditoria persistida ainda não existe; a tela atual mostra eventos recentes em memória.
- `APP_PEPPER` ainda pode ser opcional em alguns ambientes e merece validação mais rígida se o projeto for levado além do TCC.
- Headers de segurança mais avançados ainda podem ser adicionados em evolução futura.
- Permissões customizadas por usuário ainda não existem.

Próximos passos de segurança

- Persistir auditoria em banco se a necessidade histórica existir após o TCC.
- Adicionar permissões customizadas por usuário apenas se houver demanda real.
- Adicionar reautenticação para ações críticas em fase futura.
- Incorporar headers de segurança mais avançados em outra etapa.
- Revisar `APP_PEPPER` e rotação de secrets se o projeto sair do contexto acadêmico.

Não exponha segredos

Nunca inclua senhas reais, chaves ou tokens em documentos versionados. Use `.env.example` com placeholders.
