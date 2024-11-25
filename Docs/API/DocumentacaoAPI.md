# API de Recuperação e Geração de Respostas com RAG

## Visão Geral

Esta API implementa um sistema de Recuperação e Geração Aumentada (RAG) usando Gemini, HuggingFace Embeddings e LlamaIndex para processamento de perguntas e recuperação de contexto a partir de documentos.

### Tecnologias Utilizadas

- FastAPI
- Gemini (Modelo de IA)
- HuggingFace Embeddings
- LlamaIndex
- Uvicorn

## Endpoints

### 1. Consulta de Pergunta

- **URL**: `/query`
- **Método**: `POST`
- **Descrição**: Processa perguntas do usuário e retorna respostas geradas pela IA

#### Parâmetros de Entrada

```json
{
  "question": "string (obrigatório)"
}
```

#### Resposta de Sucesso

```json
{
  "answer": "string"
}
```

### 2. Status do Servidor

- **URL**: `/status`
- **Método**: `GET`
- **Descrição**: Verifica o status do servidor

#### Resposta de Sucesso

```json
{
  "message": "O servidor está rodando!"
}
```

## Configurações e Inicialização

### Modelo Gemini

- **Modelo**: `gemini-1.5-flash`
- **Configurações**:
  - `temperature`: 0.4
  - `top_p`: 1
  - `top_k`: 40

### Configurações de Segurança

O modelo bloqueia conteúdo nas seguintes categorias:

- Assédio
- Discurso de Ódio
- Conteúdo Sexualmente Explícito
- Conteúdo Perigoso

### Embeddings

- **Modelo**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Características**:
  - Normalização ativada
  - Suporte multilíngue
  - Otimização dinâmica de batch size

## Fluxo de Processamento

1. Scraping inicial de notícias
2. Carregamento de documentos em um índice vetorial
3. Inicialização do motor de chat com memória conversacional
4. Processamento de consultas com recuperação de contexto

## Requisitos

- Python 3.8+
- Bibliotecas listadas no requirements.txt
- Acesso à internet para inicialização dos modelos

## Execução

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Limitações

- Dependente de conexão com serviços externos
- Qualidade das respostas vinculada à qualidade dos documentos indexados
- Limite de tokens na memória conversacional

## Segurança

- Configurações de segurança do Gemini
- Limitação de conteúdo potencialmente nocivo
- Controle de geração de respostas

## Erros Comuns

- Falta de documentos para indexação
- Problemas de conexão com modelos externos
- Estouro de limite de tokens

## Próximos Passos

- Implementar autenticação
- Adicionar mais fontes de dados
- Melhorar tratamento de erro
- Adicionar monitoramento de performance
