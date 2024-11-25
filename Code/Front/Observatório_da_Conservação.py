import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import nltk
import re
from wordcloud import WordCloud
from PIL import Image

st.set_page_config(
    page_title='Observatório da Conservação',
    page_icon='🐸'
)


@st.cache_data
def csv_news_to_df(filename) -> pd.DataFrame:
    '''
    Função que lê o arquivo CSV com os resultados da coleta de notícias e retorna um DataFrame.

    Returns:
    df (pd.DataFrame): DataFrame com os resultados da coleta de notícias.
    '''
    df = pd.read_csv(os.path.abspath(
        os.path.join('.', 'Data', 'news_data', filename)))
    return df


@st.cache_data
def remove_stopwords(df: pd.DataFrame) -> str:
    '''
    Função que tokeniza o texto das notícias e retorna uma string com as palavras filtradas.

    Args:
    df (pd.DataFrame): DataFrame com as notícias.

    Returns:
    filtered_words (str): String com as palavras filtradas.
    '''
    nltk.download('stopwords')
    stopwords = set(nltk.corpus.stopwords.words('portuguese'))

    words = [re.sub(r'[^\w\s]|[\d]', '', word.lower().strip())
             for line in df['content']
             for word in line.split()]

    filtered_words = [
        word for word in words if word and word not in stopwords and (len(word) > 3 or word == 'sul')]

    return ' '.join(filtered_words)


@st.cache_data
def generate_wordcloud(text: str) -> tuple:
    '''
    Função que gera a nuvem de palavras e retorna a figura e o eixo.

    Args:
    text (str): Texto das notícias.

    Returns:
    tuple: (figura, eixo) do matplotlib
    '''
    frog_mask = np.array(Image.open(
        os.path.abspath(os.path.join('.', 'Data', 'images', 'frog.png'))))

    stopwords = ['brasil', 'ano', 'ainda',
                 'área', 'estado', 'sobre',
                 'segundo', 'projeto', 'disse',
                 'todo', 'outro', 'outra',
                 'apenas', 'pode', 'grande',
                 'desde', 'gente', 'região',
                 'proposta', 'forma', 'além',
                 'toda', 'onde', 'áreas',
                 'processo', 'ações', 'espécie',
                 'país', 'maior', 'pessoa',
                 'município', 'nova', 'cidade',
                 'dado', 'sendo', 'anos',
                 'estudo', 'bioma', 'outras',
                 'podem', 'espécies', 'parte',
                 'acordo', 'então', 'caso',
                 'pessoas', 'porque', 'total',
                 'desse', 'órgão', 'território',
                 'outros', 'trabalho', 'após',
                 'dados', 'milhões', 'número',
                 'animais', 'impacto', 'parque',
                 'contra', 'atividade', 'pesquisadores',
                 'todos', 'medida', 'assim',
                 'municípios', 'ambiental', 'governo',
                 'nacional', 'problema', 'disso',
                 'hectare', 'hectares', 'plano',
                 'política', 'federal', 'proteção',
                 'presidente', 'dessa', 'estados',
                 'empresa', 'cada', 'afirmou',
                 'conta', 'sistema', 'instituto',
                 'durante', 'exemplo', 'dentro',
                 'relação', 'direito', 'afirmou',
                 'brasileiro', 'servidores', 'importante',
                 'pesquisa', 'novo', 'tema']

    wordcloud = WordCloud(width=800,
                          height=400,
                          scale=1.5,
                          background_color='white',
                          colormap='Dark2',
                          contour_width=3,
                          stopwords=stopwords,
                          contour_color='green',
                          mask=frog_mask).generate(text)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    return fig, ax


def create_word_cloud(text: str) -> None:
    '''
    Função que cria e exibe a nuvem de palavras no Streamlit.

    Args:
    text (str): Texto das notícias.

    Returns:
    None
    '''
    st.markdown('## Nuvem de Palavras:snow_cloud:')
    st.markdown('''A nuvem de palavras abaixo foi gerada a partir do conteúdo das
                notícias do ano de 2024 do site [((o))eco](https://www.oeco.org.br/).''')
    with st.spinner('Aguarde, carregando dados...'):
        fig, _ = generate_wordcloud(text)
        st.pyplot(fig)


def app():
    '''
    Função principal que cria a aplicação Streamlit.
    '''
    st.title('Observatório da Conservação:frog:')
    st.markdown('<div style="text-align: justify;">A conservação da biodiversidade e dos recursos naturais é um tema de extrema importância na sociedade atual. Vários ODS estão diretamente relacionados à conservação, como o ODS 13 (Ação contra a mudança global do clima), ODS 14 (Vida na água) e ODS 15 (Vida terrestre). Em vista desse cenário, o Observatório da Conservação foi criado para disponibilizar análises e informações sobre a conservação da biodiversidade e dos recursos naturais no Brasil.</div>', unsafe_allow_html=True)
    df_news = csv_news_to_df('news_results.csv')
    text = remove_stopwords(df_news)
    create_word_cloud(text)


app()
