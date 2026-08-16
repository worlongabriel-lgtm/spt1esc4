# Análise de Riscos e Narrativa para Stakeholders

## Objetivo do documento

Este documento descreve os principais riscos do MVP da `Task Priority API`, o impacto esperado e as ações de mitigação. Também apresenta uma narrativa simples para stakeholders não técnicos, explicando o propósito, benefício e limitações do projeto.

## Visão geral do projeto

O MVP é uma micro-API REST para gerenciamento de tarefas, com CRUD completo e sugestão de prioridade assistida por IA. A priorização funciona com heurísticas locais e pode usar um provedor externo de IA apenas quando a chave `OPENAI_API_KEY` estiver configurada.

### Componentes principais

- Endpoints para criar, listar, consultar, atualizar e remover tarefas
- Persistência em memória no MVP
- Priorização assistida por regras locais
- Documentação automática via OpenAPI/Swagger
- Testes automatizados básicos

## Principais riscos

### 1. Persistência temporária em memória

- Risco: dados são perdidos ao reiniciar a aplicação.
- Impacto: perda de tarefas criadas e inconsistência no histórico.
- Mitigação: a arquitetura já está preparada para evoluir para banco de dados relacional; a persistência em memória é um facilitador para validar o contrato da API rapidamente.

### 2. Dependência de IA externa opcional

- Risco: se configurada, a chamada à OpenAI pode falhar por timeout, erro de rede ou limite de uso.
- Impacto: degradação na experiência de priorização e possível indisponibilidade parcial do serviço.
- Mitigação: há fallback automático para a priorização local quando a IA externa não estiver disponível ou configurada.

### 3. Ausência de autenticação e autorização

- Risco: qualquer cliente que acesse a API pode criar, alterar ou excluir tarefas.
- Impacto: uso não autorizado e possíveis alterações indevidas nas tarefas.
- Mitigação: este item está fora do escopo do MVP; a arquitetura permite incorporar autenticação/autorização em próximas versões.

### 4. Falta de persistência definitiva e backup

- Risco: não há suporte a banco de dados gerenciado, backup ou recuperação de dados.
- Impacto: operação não adequada para produção e risco de perda de dados em casos reais.
- Mitigação: o MVP valida o fluxo funcional; a evolução prevista é para banco de dados relacional com gerenciamento de estado.

### 5. Cobertura limitada de testes

- Risco: testes podem não cobrir todos os fluxos de erro e borda.
- Impacto: bugs podem chegar ao ambiente de homologação ou usar casos não previstos.
- Mitigação: há base de testes existente e a sugestão é ampliar a cobertura nas próximas entregas.

### 6. Dependências de ambiente e configuração

- Risco: variáveis de ambiente mal configuradas ou ausência de chave de IA.
- Impacto: comportamento diferente do esperado em ambientes de desenvolvimento e teste.
- Mitigação: o projeto já usa `.env.example` e o funcionamento sem IA é suportado nativamente.

## Matriz de riscos resumida

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Persistência em memória | Alta | Alto | Evolução para DB relacional | 
| Falha da IA externa | Média | Médio | Fallback local | 
| Ausência de autenticação | Alta | Alto | Adicionar auth em próximas iterações | 
| Backup/dados permanentes | Alta | Alto | Planejar DB gerenciado | 
| Cobertura de testes limitada | Média | Médio | Ampliação de testes | 
| Configuração de ambiente | Média | Médio | `.env.example` e documentação | 

## O que já está seguro no MVP

- Contrato de API bem definido (`/tasks`, `/health`)
- Documentação automática via FastAPI/Swagger
- Separação de camadas entre rotas, serviços e repositório
- Prioridade sugerida mesmo sem IA externa
- Testes automatizados básicos cobrindo serviço e rotas

## Narrativa para stakeholders não técnicos

### O que entregamos

O produto é uma API para registrar e gerenciar tarefas de forma centralizada. Ele ajuda a equipe a organizar trabalho, acompanhar o status de tarefas e receber uma sugestão de prioridade automática.

### Por que isso importa

- Reduz o tempo gasto em decidir o que é mais urgente
- Padroniza o cadastro de tarefas em um único ponto
- Facilita a futura integração com sistemas internos ou dashboards

### Como funciona hoje

- Um usuário ou sistema cria uma tarefa via API
- O serviço calcula uma prioridade automaticamente
- A tarefa pode ser listada, consultada, alterada ou apagada
- Um endpoint de saúde (`/health`) confirma que a API está operando

### O que está pronto e pode ser usado

- Criação e edição de tarefas
- Consulta e listagem de tarefas
- Remoção de tarefas
- Prioridade sugerida por regras locais
- Documentação interativa no navegador

### O que ainda não é definitivo

- Os dados não são salvos permanentemente entre reinicializações
- Ainda não há login, controle de acesso ou segurança para usuários
- A integração com IA externa é opcional e não obrigatória
- O MVP não é uma solução de produção completa, mas sim um protótipo sólido para validação

### Próximos passos recomendados

1. Adotar uma base de dados relacional para persistência
2. Implementar autenticação/autorização
3. Ampliar os testes de segurança e fluxos de erro
4. Evoluir a priorização assistida com IA integrada de forma segura

## Recomendações para a entrega

- Inclua este documento como parte da entrega junto com o README e o escopo do MVP
- Reforce que o projeto já atende ao contrato funcional básico, mas ainda requer evolução para uso em produção
- Use a narrativa não técnica para explicar os benefícios e as limitações sem jargões técnicos
