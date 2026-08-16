# Relatório Executivo para Stakeholders

## Visão Geral
Este documento apresenta, em termos não técnicos, o propósito, o valor e o status atual do projeto "Task Priority API" — uma micro-API para gerenciamento de tarefas com sugestão automática de prioridade.

## Objetivo do Projeto
Entregar um serviço simples, testável e confiável para criação, acompanhamento e priorização de tarefas internas. A priorização é assistida por uma heurística local e pode usar IA externamente quando configurada.

## Por que isso importa para o negócio
- Melhora a alocação de recursos ao destacar tarefas mais críticas.
- Reduz o tempo de decisão operacional ao sugerir prioridades automaticamente.
- Permite rastreabilidade e filtros por status, prioridade e prazo.
- Projeto pronto para evoluir para armazenamento persistente e integração com outras ferramentas.

## Benefícios Esperados
- Maior agilidade na resolução de incidentes críticos.
- Priorização consistente e auditável de atividades.
- Integração simples via API com sistemas internos (ferramentas de atendimento, dashboards, etc.).

## Principais Funcionalidades (resumo)
- Criar, listar, atualizar e remover tarefas.
- Sugestão automática de prioridade (low/medium/high/urgent).
- Filtros por status, prioridade e data de vencimento.
- Interface de API documentada (Swagger/OpenAPI) para testes e integração.

## Como Funciona (sem jargão técnico)
- Equipe ou sistema cria uma tarefa informando título, descrição e prazo opcional.
- A aplicação sugere uma prioridade com base no texto informado. Se disponível, pode consultar um serviço de IA para uma sugestão adicional; caso contrário, usa regras locais.
- A tarefa fica armazenada e pode ser consultada, filtrada ou atualizada por outras partes da organização.

## Estado Atual (MVP)
- Núcleo funcional implementado e testado com foco em qualidade.
- Priorização funciona com heurística local; integração com OpenAI é opcional mediante configuração de chave.
- Persistência está em memória no MVP; plano para migrar a um banco relacional está no backlog.
- Documentação de API e exemplos prontos para execução local.

## Limitações e Riscos
- Persistência em memória: dados não sobrevivem reinícios — não indicado para produção ainda.
- Dependência opcional de serviço de IA externo: se ativado, gera custo e requer gestão de chaves e privacidade dos dados.
- Validação de entrada é feita, mas a maturidade para carga alta ainda não foi testada.

## Mitigações Propostas
- Priorizar a implementação de persistência (SQLite/Postgres) para garantir durabilidade.
- Avaliar governança de uso de IA (privacidade, custos, limites de taxa) antes de ativar em produção.
- Incluir monitoramento e testes de carga após migração para banco de dados.

## Próximos Passos Recomendados
1. Decisão executiva: habilitar persistência e ambiente de homologação.
2. Planejar migração para banco relacional (escopo e responsáveis).
3. Definir política de uso de IA (quais dados podem ser enviados, limites e custos).
4. Criar documentação de integração para equipes consumidoras.

## Prazo Estimado para Produção (exemplo)
- MVP atual → Homologação com persistência: 2–4 semanas (dependendo de prioridades e disponibilidade).
- Homologação → Produção: 1–2 semanas adicionais (testes, monitoramento e rollout gradual).

## Contatos e Responsáveis
- Time de desenvolvimento: repositório interno (código-fonte e testes automatizados).
- Para dúvidas e priorização de roadmap: indicar sponsor/PO responsável.

---
Documento gerado automaticamente a partir do estado atual do repositório. Se desejar, ajusto o tom, adiciono um resumo executivo ainda mais curto ou incluo cronograma detalhado e estimativas de esforço.
