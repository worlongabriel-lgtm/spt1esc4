# Escopo do MVP

## Objetivo

Desenvolver uma micro-API para gestao de tarefas de uma equipe interna, permitindo registrar, consultar, atualizar e remover tarefas de forma padronizada.

O MVP deve fornecer uma base simples, testavel e extensivel para evoluir regras de priorizacao assistida por IA em releases futuras.

## Publico-alvo

Equipe interna que precisa acompanhar tarefas operacionais, tecnicas ou administrativas em um fluxo centralizado via API.

## Requisitos funcionais

### RF01 - Health check

A API deve disponibilizar um endpoint para verificacao de disponibilidade.

- Metodo: `GET`
- Rota: `/health`
- Resposta esperada: status da aplicacao e timestamp da verificacao

### RF02 - Criacao de tarefas

A API deve permitir criar uma nova tarefa.

Campos previstos:

- `title`
- `description`
- `status`
- `priority`
- `due_date`
- `created_at`
- `updated_at`

### RF03 - Listagem de tarefas

A API deve permitir listar tarefas cadastradas.

A listagem deve permitir evolucao futura para filtros por:

- status
- prioridade
- prazo
- responsavel

### RF04 - Consulta de tarefa por identificador

A API deve permitir consultar uma tarefa especifica por identificador unico.

### RF05 - Atualizacao de tarefas

A API deve permitir atualizar dados de uma tarefa existente.

Campos atualizaveis previstos:

- titulo
- descricao
- status
- prioridade
- prazo

### RF06 - Remocao de tarefas

A API deve permitir remover uma tarefa existente por identificador.

### RF07 - Priorizacao assistida

A API deve prever um fluxo para sugerir prioridade de uma tarefa com apoio de IA.

A priorizacao deve considerar, quando disponivel:

- urgencia
- impacto
- prazo
- contexto informado
- descricao da tarefa

No MVP, a implementacao pode iniciar com regra local ou contrato de endpoint, antes da integracao completa com provedor externo de IA.

### RF08 - Documentacao da API

A API deve expor documentacao interativa por meio do Swagger/OpenAPI gerado pelo FastAPI.

## Requisitos nao funcionais

### RNF01 - Stack

O projeto deve utilizar:

- Python 3.13
- FastAPI
- Pydantic
- Uvicorn
- Pytest

### RNF02 - Padrao de codigo

O codigo deve seguir boas praticas de legibilidade, tipagem e separacao de responsabilidades.

### RNF03 - Configuracao por ambiente

Configuracoes sensiveis ou variaveis por ambiente devem ser carregadas via variaveis de ambiente.

Arquivos `.env` nao devem ser versionados.

### RNF04 - Testabilidade

As regras principais e endpoints criticos devem ser cobertos por testes automatizados.

### RNF05 - Observabilidade basica

A API deve permitir evolucao para logs estruturados e rastreabilidade de erros.

No MVP, erros devem retornar respostas HTTP consistentes e compreensiveis.

### RNF06 - Documentacao

O projeto deve manter documentacao minima para instalacao, execucao local e escopo funcional.

### RNF07 - Evolutividade

A arquitetura deve permitir evolucao posterior para:

- persistencia em banco de dados
- autenticacao
- integracao com IA externa
- deploy em ambiente controlado

## Fora de escopo

Os itens abaixo nao fazem parte do MVP inicial:

- Interface web ou mobile
- Autenticacao e autorizacao completas
- Controle granular de permissoes por usuario
- Integracao obrigatoria com provedor externo de IA
- Persistencia definitiva em banco de dados gerenciado
- Fila de processamento assincrono
- Notificacoes por e-mail, Slack ou outros canais
- Multi-tenant
- Relatorios analiticos avancados
- Auditoria completa de alteracoes
- Deploy em producao

## Premissas

- A API sera consumida por sistemas internos ou ferramentas tecnicas.
- O primeiro ciclo prioriza contrato da API, organizacao do projeto e endpoints basicos.
- A integracao com IA deve ser introduzida de forma incremental, sem bloquear o CRUD inicial de tarefas.
- O armazenamento pode iniciar em memoria ou camada simples, desde que a evolucao para banco de dados seja considerada no desenho.

## Criterios de aceite do MVP

- A aplicacao inicia localmente com Uvicorn.
- O endpoint `/health` retorna status `ok` e timestamp.
- O projeto possui README com instrucoes de execucao.
- O projeto possui arquivo de dependencias.
- O escopo funcional do MVP esta documentado.
- A estrutura inicial permite adicionar rotas, modelos e testes sem reorganizacao significativa.
