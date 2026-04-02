# Assests

# 📋 Sigatccompact — Sistema de Controle de Ativos

> **Sistema acadêmico e técnico para gestão de ativos de TI, criado para apoiar o controle patrimonial escolar e estruturar uma base confiável para cadastro, rastreabilidade, autenticação e futura evolução web.**

[![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)]()
[![Curso](https://img.shields.io/badge/Curso-Manutenção%20e%20Suporte-blue)]()
[![Disciplina](https://img.shields.io/badge/Disciplina-Governança%20de%20TI-purple)]()
[![Framework](https://img.shields.io/badge/Framework-COBIT_2019-orange)]()

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Problema e Justificativa](#-problema-e-justificativa)
- [Objetivos](#-objetivos)
- [Framework / Metodologia Adotada](#-framework--metodologia-adotada)
- [Escopo e Delimitações](#-escopo-e-delimitações)
- [Entregáveis](#-entregáveis)
- [Cronograma](#-cronograma)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Navegar este Projeto](#-como-navegar-este-projeto)
- [Resultados e Conclusões](#-resultados-e-conclusões)
- [Referências](#-referências)
- [Glossário de Termos Técnicos](#-glossário-de-termos-técnicos)
- [Equipe](#-equipe)

---

## 🎯 Sobre o Projeto

| Campo | Detalhe |
|-------|---------|
| **Instituição** | ETEC Jaraguá |
| **Curso** | Manutenção e Suporte em Informática |
| **Disciplina** | Governança de TI |
| **Semestre** | 2026.1 |
| **Orientador(a)** | Professora Tainá Barros Batista Oliveira |
| **Tipo de Trabalho** | TCC – Trabalho de Conclusão de Curso |

**Resumo:**

O projeto Sigatccompact surgiu a partir da necessidade de modernizar o controle patrimonial e administrativo de ativos em ambiente escolar, com foco inicial na realidade da ETEC Jaraguá. A proposta parte de um problema recorrente em instituições educacionais: controles descentralizados, baixa padronização cadastral, dificuldade de localizar equipamentos por setor e pouca visibilidade sobre o estado real dos bens, como itens em uso, manutenção, reserva ou baixa.

Como resposta, foi desenvolvida uma base técnica em Python com persistência em MySQL, autenticação de usuários, validações centralizadas e arquitetura modular separada por responsabilidades. O sistema já contempla cadastro, login, recuperação de senha, CRUD de ativos, filtros por múltiplos critérios, ordenação e controle de acesso por usuário autenticado. Além da operação em terminal, o projeto já possui camada web em Flask com rotas para autenticação e manipulação de ativos, além de telas HTML/CSS em evolução. O resultado atual é uma fundação funcional e rastreável, pronta para consolidação final, integração visual, testes intensivos e documentação acadêmica. 

**Palavras-chave:** `governança de TI`, `COBIT 2019`, `gestão de ativos`, `controle patrimonial escolar`, `instituição de ensino`

---

## ❗ Problema e Justificativa

### Problema

> A gestão de ativos em ambiente escolar tende a sofrer com registros descentralizados, baixa padronização de informações e dificuldade de rastrear equipamentos por setor e por responsável. No contexto da ETEC Jaraguá, o projeto foi concebido justamente para atacar essa lacuna, estruturando uma base digital que substitua controles manuais e reduza a perda de visibilidade sobre o ciclo de vida dos ativos.

### Justificativa

- 📊 **Dados do cenário atual:**
  - Controle patrimonial tradicionalmente dependente de processos manuais e baixa rastreabilidade institucional.
  - Necessidade de padronização de cadastro, autenticação, status operacionais e filtros por setor, responsável e datas.
  - O projeto já evoluiu para arquitetura modular com autenticação, CRUD funcional, integração com MySQL e camada web iniciada.
- 💰 **Impacto no negócio:**
  - Redução de retrabalho administrativo e melhora na confiabilidade do inventário interno.
  - Criação de base para manutenção, auditoria, planejamento de reposição e controle operacional mais seguro.
- 📖 **Relevância acadêmica:**
  - Integra conteúdos de governança de TI, modelagem de dados, autenticação, organização por camadas, persistência relacional e evolução controlada de software.
  - Gera um artefato aplicável a cenário real, com valor prático para a escola e potencial de adaptação para outras instituições.

---

## 🎯 Objetivos

### Objetivo Geral

Desenvolver um sistema de controle de ativos com autenticação de usuários e persistência em banco MySQL, estruturado de forma modular e alinhado à disciplina de Governança de TI, para apoiar o controle patrimonial escolar e preparar a solução para evolução web, documentação acadêmica e uso operacional mais seguro.

### Objetivos Específicos

1. [x] Desenvolver a estrutura modular do sistema separando modelos, serviços, banco de dados, utilitários e interface.
2. [x] Implementar autenticação com cadastro, login e recuperação de senha por pergunta de segurança.
3. [x] Implementar CRUD de ativos com regras de negócio, validações, filtros e ordenação.
4. [🔨] Consolidar a camada web em Flask com integração progressiva entre rotas, sessão e interface HTML/CSS.
5. [🔨] Organizar a documentação técnica e acadêmica do projeto para entrega final do TCC.

---

## 📐 Framework / Metodologia Adotada

### Framework de Governança

| Framework | Versão | Processos/Domínios Utilizados | Papel no Projeto |
|-----------|--------|-------------------------------|------------------|
| COBIT | 2019 | APO01, BAI03, DSS01, MEA01 | Principal |
| ITIL | v4 | Gestão de serviços, controle operacional, suporte e melhoria contínua | Complementar |
| ISO/IEC | 27001 / 27002 | Princípios de proteção de credenciais e dados sensíveis | Complementar |
| PMBOK | 7ª ed. | Planejamento, cronograma, riscos e acompanhamento de entregas | Complementar |

### Detalhamento das Práticas Aplicadas

| Prática / Processo | O que diz o framework | Como foi aplicado no seu projeto |
|--------------------|----------------------|----------------------------------|
| **Gestão de ativos de TI** | Organiza identificação, controle e rastreabilidade dos recursos | Estruturação de cadastro, status, responsável, departamento, datas e filtros operacionais para cada ativo |
| **Controle de acesso** | Garante uso autorizado de recursos e segregação mínima | Implementação de autenticação, sessão, vínculo entre usuário autenticado e ativos criados |
| **Qualidade e controle operacional** | Exige regras claras, validações e previsibilidade de processo | Centralização de validadores, padronização de exceções e tratamento das regras de status e datas |
| **Melhoria contínua** | Promove evolução incremental baseada em lacunas e riscos | Projeto evoluiu de CRUD simples para arquitetura modular com MySQL, segurança reforçada e base web em refinamento |

### Metodologia de Pesquisa

- **Tipo:** Pesquisa aplicada com estudo de caso
- **Abordagem:** Qualitativa, com apoio técnico-documental
- **Coleta de dados:** análise do cenário escolar, levantamento funcional do problema, definição de requisitos, registro evolutivo do desenvolvimento e documentação técnica do projeto
- **Amostra/participantes:** equipe do TCC e contexto institucional da ETEC Jaraguá
- **Ferramentas:** Python, Flask, MySQL, SQL, HTML, CSS, JavaScript, GitHub, documentação técnica e relatórios acadêmicos
- **Período de coleta:** fevereiro de 2026 a maio de 2026

---

## 🔲 Escopo e Delimitações

### ✅ Dentro do Escopo

- Cadastro de usuários com e-mail, senha e pergunta de recuperação.
- Login, logout e recuperação de senha com resposta de segurança.
- CRUD de ativos com identificação, tipo, marca, modelo, responsável, departamento, status e datas.
- Listagem, busca por ID, filtros por responsável, departamento, status e datas, além de ordenação.
- Integração com banco MySQL e estrutura SQL própria.
- Estruturação de camada web com Flask e telas iniciais de autenticação.
- Versionamento e rastreabilidade do desenvolvimento via GitHub.

### ❌ Fora do Escopo

- Implantação produtiva completa dentro da instituição — depende de homologação e consolidação final.
- Dashboard analítico completo e relatórios gerenciais avançados — etapa futura após estabilização da base.
- Gestão completa de estoque e movimentação de outros domínios além dos ativos atuais — ampliação planejada para evolução posterior.

### ⚠️ Premissas e Restrições

| Tipo | Descrição |
|------|-----------|
| Premissa | O projeto será desenvolvido com base em ferramentas acessíveis ao contexto acadêmico. |
| Premissa | O sistema deve servir como artefato técnico e acadêmico do TCC. |
| Restrição | Prazo limitado ao calendário letivo e à data de entrega final. |
| Restrição | Camada web ainda em consolidação, o que limita a maturidade visual atual. |
| Restrição | Dados pessoais devem ser tratados com cuidado, em linha com preocupações de LGPD. |

---

## 📦 Entregáveis

| # | Entregável | Formato | Localização no Repo | Status |
|---|-----------|---------|---------------------|--------|
| 1 | README técnico e acadêmico do projeto | MD | `README.md` | ✅ Concluído |
| 2 | Estrutura de banco de dados | SQL | `database/schema.sql` | ✅ Concluído |
| 3 | Script de inicialização do banco | PY | `database/init_db.py` | ✅ Concluído |
| 4 | Módulo de autenticação | PY | `services/auth_service.py` | ✅ Concluído |
| 5 | Módulo de ativos com regras de negócio | PY | `services/ativos_service.py` | ✅ Concluído |
| 6 | Interface terminal do sistema | PY | `main.py` e `services/sistema_ativos.py` | ✅ Concluído |
| 7 | Base da camada web Flask | PY | `web/app.py` | 🔨 Em andamento |
| 8 | Telas iniciais de autenticação | HTML/CSS | `templates/` e `static/` | ✅ Concluído |
| 9 | Relatório técnico / monografia TCC | DOCX / PDF | `docs/` | 🔨 Em andamento |
| 10 | Slides da defesa | PPTX | `apresentacao/slides-defesa.pptx` | 🔲 Pendente |

**Legenda:** 🔲 Pendente · 🔨 Em andamento · ✅ Concluído

---

## 📅 Cronograma

| Fase | Atividade | Início | Fim | Entregável Associado | Status |
|------|-----------|--------|-----|---------------------|--------|
| 1 | Definição do tema, narrativa do problema e escopo inicial | 11/02/2026 | 02/03/2026 | Estrutura inicial do projeto | ✅ |
| 2 | Modelagem inicial e organização modular | 02/03/2026 | 15/03/2026 | Arquitetura por camadas | ✅ |
| 3 | Implementação de autenticação e persistência | 16/03/2026 | 24/03/2026 | Módulo de usuários + banco MySQL | ✅ |
| 4 | Consolidação do CRUD de ativos e refinamento de regras | 24/03/2026 | 27/03/2026 | CRUD funcional em terminal | ✅ |
| 5 | Estabilização técnica do backend | 27/03/2026 | 10/04/2026 | Backend consolidado e alinhado | 🔨 |
| 6 | Evolução visual e refinamento da interface | 11/04/2026 | 20/04/2026 | Login refinado e estrutura principal | 🔲 |
| 7 | Integração entre telas e backend | 21/04/2026 | 27/04/2026 | Fluxos web validados | 🔨 |
| 8 | Testes, documentação e evidências | 28/04/2026 | 30/04/2026 | Relatórios, prints e revisão final | 🔲 |
| 9 | Preparação da apresentação | 01/05/2026 | 03/05/2026 | Slides e roteiro | 🔲 |
| 10 | **Entrega / apresentação final** | 04/05/2026 | 04/05/2026 | Projeto final | 🔲 |

---

## 📁 Estrutura do Repositório

```text
sigatccompact/
│
├── README.md
│
├── database/
│   ├── connection.py
│   ├── init_db.py
│   └── schema.sql
│
├── models/
│   ├── ativos.py
│   └── usuario.py
│
├── services/
│   ├── ativos_service.py
│   ├── auth_service.py
│   └── sistema_ativos.py
│
├── utils/
│   ├── crypto.py
│   └── validators.py
│
├── web/
│   └── app.py
│
├── templates/
│   ├── index.html
│   ├── register.html
│   └── recovery.html
│
├── static/
│   └── index.css
│
├── docs/
│   ├── relatorio-tecnico.docx
│   ├── mini-relatorio-crud.docx
│   └── monografia-tcc.pdf
│
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

---

## 🧭 Como Navegar este Projeto

| Eu quero... | Vá para... |
|-------------|-----------|
| Entender o objetivo do sistema | [Sobre o Projeto](#-sobre-o-projeto) |
| Ver o problema e justificativa | [Problema e Justificativa](#-problema-e-justificativa) |
| Entender o recorte acadêmico | [Framework / Metodologia Adotada](#-framework--metodologia-adotada) |
| Ver a estrutura técnica do backend | `database/`, `models/`, `services/`, `utils/` |
| Rodar a versão terminal | `main.py` |
| Evoluir a versão web | `web/app.py`, `templates/`, `static/` |
| Entender as regras de negócio dos ativos | `services/ativos_service.py` e `utils/validators.py` |
| Revisar a base de autenticação e segurança | `services/auth_service.py` e `utils/crypto.py` |

---

## 📊 Resultados e Conclusões

### Principais Resultados

| Métrica / Indicador | AS-IS (antes) | TO-BE (depois/projetado) | Variação |
|---------------------|---------------|--------------------------|----------|
| Controle patrimonial | Manual / disperso | Digital / padronizado | Melhoria estrutural |
| Rastreabilidade dos ativos | Baixa | Média a alta (projetada) | Ganho funcional |
| Cadastro e autenticação | Inexistente no sistema | Implementado | +100% |
| CRUD de ativos | Inexistente no sistema | Funcional em terminal | +100% |
| Camada web | Não existente | Base criada e em evolução | Em progresso |

### Conclusões

1. O projeto já ultrapassou a fase de protótipo conceitual e possui base técnica funcional para autenticação, persistência e gestão de ativos.
2. A arquitetura modular adotada favorece manutenção, evolução e alinhamento entre banco, regras de negócio e interfaces.
3. O sistema já demonstra aderência prática ao problema proposto, atacando a falta de padronização e rastreabilidade de ativos.
4. A principal limitação atual não está no núcleo do backend, mas na consolidação da interface web, na bateria de testes finais e na documentação definitiva.

### Trabalhos Futuros

- Concluir a integração web ponta a ponta com autenticação e gestão de ativos em interface gráfica.
- Implementar testes automatizados e documentação complementar de API e fluxos.
- Evoluir o sistema para dashboard, relatórios gerenciais e possíveis módulos adicionais, como estoque e movimentação.
- Revisar controles de segurança, LGPD, perfis de acesso e trilhas de auditoria.

---

## 📚 Referências

1. ISACA. **COBIT 2019 Framework: Introduction and Methodology**. Schaumburg: ISACA, 2018.
2. AXELOS. **ITIL Foundation: ITIL 4 Edition**. London: TSO, 2019.
3. ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **ABNT NBR ISO/IEC 27001** — Segurança da informação, cibersegurança e proteção da privacidade. Rio de Janeiro: ABNT.
4. PRESSMAN, Roger S.; MAXIM, Bruce R. **Engenharia de Software**. 8. ed. Porto Alegre: AMGH.
5. SOMMERVILLE, Ian. **Engenharia de Software**. 10. ed. São Paulo: Pearson.
6. SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. **Sistema de Banco de Dados**. Porto Alegre: Bookman.
7. MACHADO, Felipe Nery Rodrigues. **Banco de Dados: Projeto e Implementação**. São Paulo: Érica.
8. Documentação técnica interna do projeto Sigatccompact.

> 📝 Lista bibliográfica final pode ser consolidada em `docs/referencias.bib`

---

## 📖 Glossário de Termos Técnicos

<details open>
<summary><strong>🎯 Termos Específicos deste Projeto</strong></summary>

| Termo | Definição no contexto deste projeto |
|-------|-------------------------------------|
| **Ativo** | Equipamento ou recurso de TI cadastrado no sistema, com identificação, responsável, departamento, status e datas de controle. |
| **Usuário responsável** | Pessoa vinculada ao uso operacional ou guarda do ativo no cadastro. |
| **Status do ativo** | Estado operacional padronizado do item: Disponível, Em Uso, Em Manutenção, Reservado ou Baixado. |
| **Pergunta de recuperação** | Campo usado como segunda camada de validação para redefinição de senha. |
| **CRUD** | Conjunto de operações de criação, leitura, atualização e remoção aplicadas aos ativos. |
| **Camada de serviço** | Parte do sistema onde ficam as regras de negócio e o controle das operações principais. |
| **Camada web** | Estrutura em Flask responsável pela futura interface visual e exposição dos fluxos do sistema. |

</details>

<details open>
<summary><strong>🏛️ Governança e Gestão de TI</strong></summary>

| Termo | Definição |
|-------|-----------|
| **Governança de TI** | Estruturas, processos e mecanismos que garantem que a TI sustente e estenda a estratégia da organização. |
| **Gestão de TI** | Execução operacional dos recursos, serviços e controles definidos para a área de tecnologia. |
| **Alinhamento Estratégico** | Relação entre as necessidades institucionais e as soluções tecnológicas adotadas. |
| **Compliance** | Conformidade com normas, políticas e exigências legais aplicáveis. |
| **Maturidade** | Nível de evolução de um processo ou solução ao longo do tempo. |
| **Stakeholder** | Parte interessada afetada pelo projeto, como equipe, escola, orientador e usuários. |

</details>

<details>
<summary><strong>📗 COBIT 2019</strong></summary>

| Termo | Definição |
|-------|-----------|
| **COBIT** | Framework de governança e gestão de TI voltado a controle, valor, risco e alinhamento. |
| **APO** | Domínio de alinhar, planejar e organizar. |
| **BAI** | Domínio de construir, adquirir e implementar. |
| **DSS** | Domínio de entregar, servir e suportar. |
| **MEA** | Domínio de monitorar, avaliar e analisar. |
| **RACI** | Matriz de responsabilidades: Responsible, Accountable, Consulted, Informed. |

</details>

<details>
<summary><strong>📘 ITIL v4</strong></summary>

| Termo | Definição |
|-------|-----------|
| **ITIL** | Conjunto de boas práticas para gerenciamento de serviços de TI. |
| **Serviço** | Meio de entregar valor ao usuário sem transferir a ele todos os riscos e custos. |
| **Incidente** | Interrupção não planejada ou redução da qualidade de um serviço. |
| **Melhoria Contínua** | Prática de revisar e aperfeiçoar processos, rotinas e resultados de forma recorrente. |
| **Service Desk** | Ponto central de contato entre usuário e suporte. |
| **Catálogo de Serviços** | Lista estruturada de serviços oferecidos pela TI. |

</details>

<details>
<summary><strong>🔒 Segurança da Informação</strong></summary>

| Termo | Definição |
|-------|-----------|
| **Hash** | Representação criptográfica usada para armazenar senhas e respostas sem manter o texto puro. |
| **Pepper** | Segredo adicional aplicado ao processo de hash para reforço de segurança. |
| **PBKDF2** | Algoritmo de derivação de chave usado para proteger credenciais com múltiplas iterações. |
| **LGPD** | Lei Geral de Proteção de Dados, aplicável ao tratamento de dados pessoais. |
| **Sessão** | Mecanismo para manter o usuário autenticado entre requisições na camada web. |
| **Variável de ambiente** | Configuração sensível separada do código-fonte, usada para credenciais e segredos. |

</details>

<details>
<summary><strong>⚙️ Desenvolvimento e Arquitetura</strong></summary>

| Termo | Definição |
|-------|-----------|
| **Arquitetura modular** | Organização do projeto em partes independentes por responsabilidade. |
| **Model** | Camada que representa as entidades principais do sistema, como usuário e ativo. |
| **Service** | Camada de lógica de negócio, validações operacionais e integração com persistência. |
| **Schema SQL** | Definição estrutural do banco de dados. |
| **Context manager** | Recurso usado para gerenciar abertura e fechamento seguro de conexões e cursores. |
| **Validação centralizada** | Estratégia de manter regras de consistência em utilitários únicos para reduzir duplicidade. |

</details>

---

## 👥 Equipe

| Nome | RA/Matrícula | Função no Projeto | Contato |
|------|-------------|-------------------|---------|
| Matheus Santos do Nascimento | 09862 | Back-end / Arquitetura / Integração técnica | matheus.nascimento237@etec.sp.gov.br |
| Felipe dos Santos Nascimento | 10624 | Front-end / Interface visual | felipe.nascimento227@etec.sp.gov.br |
| Lays Yuri Matukawa | 10413 | Documentação acadêmica | lays.matukawa@etec.sp.gov.br |
| Vitória Lopes Siqueira | 10568 | Revisão e documentação | vitoria.siqueira24@etec.sp.gov.br |
| Geovanny Iago Damasceno Mendes | 10522 | Organização e apoio documental | geovanny.mendes@etec.sp.gov.br |

**Orientador(a):** A definir / não informado no repositório

---

## 📄 Licença

Este trabalho é de natureza acadêmica e foi desenvolvido como requisito parcial para conclusão do curso de **Manutenção e Suporte em Informática** na disciplina de **Governança de TI**.

© 2026 ETEC Jaraguá — Todos os direitos reservados.

---

<details>
<summary>📝 <strong>Checklist de Entrega do TCC</strong></summary>

### Documentação
- [x] README.md preenchido e atualizado
- [ ] Monografia/relatório revisado e formatado (ABNT)
- [ ] Referências bibliográficas completas e verificadas
- [x] Glossário contém os principais termos técnicos do trabalho

### Artefatos Técnicos
- [ ] Diagrama AS-IS do processo analisado
- [ ] Diagrama TO-BE com a proposta de melhoria
- [x] Artefato principal do projeto estruturado em código funcional
- [ ] Matriz RACI preenchida
- [ ] Plano de implementação com cronograma e responsáveis

### Dados e Evidências
- [ ] Dados de pesquisa/coleta organizados e anonimizados
- [ ] Métricas de baseline documentadas com fonte
- [ ] Resultados/projeções tabulados com justificativa
- [ ] Instrumentos de coleta disponíveis

### Apresentação
- [ ] Slides da defesa preparados
- [ ] Ensaio da apresentação realizado
- [ ] Material de apoio para perguntas da banca

### Repositório
- [ ] Todos os arquivos no local correto conforme estrutura de pastas
- [ ] `.gitignore` configurado adequadamente
- [ ] Sem arquivos desnecessários ou temporários
- [ ] Nomes de arquivos em padrão consistente

### Verificação Final
- [x] O README foi convertido do modelo para conteúdo real
- [ ] Links internos do README revisados no repositório final
- [ ] Todos os arquivos referenciados no README existem na estrutura final do GitHub
- [ ] Revisão final de conformidade com LGPD

</details>
