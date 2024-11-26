import os
import torch
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Bibliotecas de terceiros
from llama_index.readers.file import PagedCSVReader
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
import google.generativeai as genai

# Módulos locais
from .utils.web_scraper import scrape_all_news, save_results_to_csv

# Constantes
MEMORY_TOKEN_LIMIT = 3900
NEWS_DATA_DIRECTORY = os.path.abspath(os.path.join('.', 'Data', 'news_data'))
ENV_PATH = os.path.abspath(os.path.join('.env'))
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=ENV_PATH)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError('GOOGLE_API_KEY não encontrada nas variáveis de ambiente')
genai.configure(api_key=GOOGLE_API_KEY)

# Template de prompt
CONTEXT_PROMPT = '''
Você é um chatbot especialista em meio ambiente, capaz de ter conversas normais e prover informações sobre o contexto abaixo:
{context_str}
Instruções: Apresente uma lista contendo os assuntos os quais você tem conhecimento. Use o histórico da conversa e o contexto 
acima para responder às perguntas do usuário. Não alucine dados e respostas. Não copie trechos direto dos documentos; use-os 
para construir suas respostas. Não diga ao usuário que você está consultando documentos, fale como se fosse seu próprio conhecimento. 
As respostas devem possuir no máximo 6 linhas. Se não souber responder a uma pergunta, diga: "Não possuo o conhecimento necessário para 
responder esta pergunta" e liste os assuntos sobre os quais você tem conhecimento.
'''

# Modelos para API


class QueryRequest(BaseModel):
    '''Modelo que representa a pergunta do usuário.'''
    question: str


class QueryResponse(BaseModel):
    '''Modelo que representa a resposta gerada pela IA.'''
    answer: str

# Funções auxiliares para inicialização


def initialize_llm() -> Gemini:
    '''Inicializa o modelo Gemini com configurações otimizadas para RAG.'''
    generation_config = {
        'temperature': 0.4,
        'top_p': 1,
        'top_k': 40,
    }
    safety_settings = [
        {'category': 'HARM_CATEGORY_HARASSMENT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
        {'category': 'HARM_CATEGORY_HATE_SPEECH',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
    ]
    return Gemini(
        model='models/gemini-1.5-flash',
        generation_config=generation_config,
        safety_settings=safety_settings,
        transport='rest',
    )


def initialize_embeddings() -> HuggingFaceEmbedding:
    '''Inicializa HuggingFaceEmbedding com configurações otimizadas para RAG.'''
    embed_batch_size = (
        min(int(torch.cuda.get_device_properties(
            0).total_memory / 1024**3 * 32), 256)
        if DEVICE == 'cuda' else 32
    )
    return HuggingFaceEmbedding(
        model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        query_instruction='Represent the question for retrieving supporting documents: ',
        text_instruction='Represent the document for retrieval: ',
        normalize=True,
        embed_batch_size=embed_batch_size,
        device=DEVICE,
        model_kwargs={'trust_remote_code': True},
    )


def initialize_chat_engine() -> VectorStoreIndex:
    '''Inicializa a engine de chat com contexto dos documentos e memória conversacional.'''
    Settings.embed_model = initialize_embeddings()

    csv_reader = PagedCSVReader(encoding='latin-1')

    csv_directory = Path(NEWS_DATA_DIRECTORY)

    documents = []

    for csv_file in csv_directory.glob('*.csv'):
        docs = csv_reader.load_data(file=csv_file)
        documents.extend(docs)

    index = VectorStoreIndex.from_documents(
        docs,
        transformations=[SentenceSplitter(chunk_size=2000, chunk_overlap=300)],
    )
    memory = ChatMemoryBuffer.from_defaults(token_limit=MEMORY_TOKEN_LIMIT)

    return index.as_chat_engine(
        chat_mode='condense_plus_context',
        memory=memory,
        llm=initialize_llm(),
        context_prompt=CONTEXT_PROMPT,
        verbose=True,
    )

# Aplicação FastAPI e gerenciamento do ciclo de vida


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Gerencia o ciclo de vida do app, incluindo scraping inicial e inicialização da engine de chat.'''
    print('Iniciando scraping inicial de notícias...')
    news_results = scrape_all_news(
        'https://oeco.org.br/category/noticias', pages=5)
    save_results_to_csv(news_results, 'news_results.csv')
    articles_results = scrape_all_news(
        'https://oeco.org.br/category/reportagens', pages=5)
    save_results_to_csv(articles_results, 'articles_results.csv')
    print('Scraping de notícias concluído.')

    print('Inicializando engine de chat...')
    global chat_engine
    chat_engine = initialize_chat_engine()

    print('Engine de chat inicializada.')

    yield

    # Cleanup
    del chat_engine


app = FastAPI(lifespan=lifespan)


@app.post('/query', response_model=QueryResponse)
async def query(request: QueryRequest):
    '''Processa as perguntas do usuário e retorna respostas geradas pela IA.'''
    global chat_engine
    response = chat_engine.chat(request.question)
    return QueryResponse(answer=response.response)


@app.get('/status')
async def status():
    '''Checa o status do servidor'''
    return {'message': 'O servidor está rodando!'}


# Executar o servidor
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
