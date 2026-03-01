# Chatbot MVP —  (Inova )

Este repositório contém um **MVP funcional** de um chatbot corporativo, desenvolvido como resposta ao desafio do processo seletivo (PROJ_1182728334), contemplando:
- apresentação conceitual do modelo;
- funcionalidades mínimas;
- testes com usuários (via registro de feedback);
- validação (técnica e de negócio) por critérios objetivos;
- documentação e código versionado em Git.

---

## Visão geral (conceitual)

O chatbot foi projetado para atender demandas corporativas com foco em:
- **clareza e rastreabilidade** (respostas e fontes);
- **segurança e governança** (higienização de entradas e possibilidade de evolução para políticas mais robustas);
- **evolução incremental** (MVP → piloto com usuários → ajustes → escala).

### Componentes principais
- **API (FastAPI)**: expõe endpoints de saúde, conversa, feedback e métricas.
- **Roteamento por intenção**: classifica a mensagem (saudação, suporte, financeiro, fallback).
- **Base de Conhecimento (KB / RAG simples)**: busca conteúdo em `docs/knowlege/` e retorna resposta com **referência de fonte**.
- **Feedback do usuário**: registra avaliações para evidenciar testes com usuários e apoiar melhoria contínua.

---

## Funcionalidades implementadas

- `GET /health` — verificação de disponibilidade do serviço.
- `POST /chat` — recebe mensagem, higieniza, classifica intenção e responde:
  - tenta recuperar conhecimento em `docs/knowlege/*` (retorna com fonte);
  - se não encontrar, usa fallback por intenção.
- `POST /feedback` — registra feedback estruturado (útil/não útil + comentário opcional).
- `GET /metrics` — sumariza feedbacks (total, taxa de utilidade, distribuição por intenção).

