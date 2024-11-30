# API de Recuperação e Geração de Respostas com RAG

## Visão Geral

Esta API implementa um sistema de Recuperação e Geração Aumentada (RAG) especificamente projetado para integração com frontend Streamlit, processando consultas de usuários sobre tópicos ambientais.

## Arquitetura de Integração

### Fluxo de Comunicação

1. **Frontend Streamlit**

   - Captura pergunta do usuário
   - Envia requisição POST para `/query`

2. **Backend FastAPI**
   - Recebe consulta
   - Processa com motor de chat RAG
   - Retorna resposta gerada

## Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Modelo de IA**: Google Gemini 1.5 Flash
- **Embeddings**: HuggingFace Multilingual
- **Orquestração**: LlamaIndex

## Endpoint de Consulta

### Detalhes do Endpoint

- **URL**: `/query`
- **Método**: `POST`
- **Função**: Processamento de perguntas ambientais

### Contrato de Requisição

```json
{
  "question": "Qual a situação atual do desmatamento na Amazônia?"
}
```

### Contrato de Resposta

```json
{
  "answer": "Resposta contextualizada baseada nas notícias indexadas"
}
```

## Características Específicas de Integração Streamlit

### Gerenciamento de Estado

- Suporte à memória conversacional
- Manutenção de contexto entre mensagens
- Recuperação dinâmica de informações

### Tratamento de Erros

- Mensagens de erro amigáveis
- Fallback para respostas padrão
- Spinner de carregamento no frontend

## Segurança e Performance

### Configurações de Segurança

- Filtros de conteúdo Gemini
- Prevenção de respostas inadequadas
- Limite de tokens de resposta

### Otimizações

- Embeddings semânticos eficientes
- Fragmentação inteligente de documentos
- Recuperação vetorial rápida

## Diferenciais Técnicos

### Processamento de Linguagem

- Modelo multilíngue
- Recuperação contextual precisa
- Geração de respostas natural

### Fonte de Dados

- Webscraping do jornal ((o)) eco
- Foco em notícias ambientais contemporâneas
- Atualização periódica de fontes

## Limitações

- Dependência de conexão externa
- Qualidade limitada pelo corpus de notícias
- Possíveis vieses das fontes originais
