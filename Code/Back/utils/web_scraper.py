import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from tqdm import tqdm
from typing import List, Dict

# Diretório para salvar dados de notícias
NEWS_DATA_DIRECTORY = os.path.abspath(os.path.join('.', 'Data', 'news_data'))


def get_soup(url: str) -> BeautifulSoup:
    '''Obtém um objeto BeautifulSoup a partir de uma URL.'''
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Garante que erros HTTP são tratados
    return BeautifulSoup(response.content, 'html.parser')


def get_news_urls(main_url: str, pages: int = 1) -> List[str]:
    '''Obtém todas as URLs de artigos de notícia de um número especificado de páginas.'''
    all_urls = []

    for page in range(1, pages + 1):
        page_url = f'{main_url}/page/{page}' if page > 1 else main_url
        print(f'Buscando URLs na página {page}...')

        soup = get_soup(page_url)
        page_urls = [
            tag['href'] for tag in soup.select('div[class="d-none d-md-block col-md-4"] > a')
        ]
        all_urls.extend(page_urls)

        print(f'Encontrados {len(page_urls)} artigos na página {page}.')

    print(f'Total de artigos encontrados: {len(all_urls)}')
    return all_urls


def scrape_news_content(url: str) -> Dict[str, str]:
    '''
    Extrai o conteúdo de um artigo de notícia de uma URL específica.

    Args:
        url (str): URL do artigo de notícia.

    Returns:
        Dict[str, str]: Dicionário com as seguintes chaves:
            - 'title': Título do artigo.
            - 'subtitle': Subtítulo do artigo.
            - 'content': Conteúdo principal do artigo.
        Retorna um dicionário vazio em caso de erro.
    '''
    try:
        soup = get_soup(url)
        title = soup.select_one('h1').text if soup.select_one('h1') else ''
        subtitle = soup.select_one('p[class="lead font-italic mb-5"]').text if soup.select_one('p[class="lead font-italic mb-5"]') else ''
        content_tags = soup.select('div[class="article"] > p')
        content = '\n'.join(tag.text for tag in content_tags) if content_tags else ''

        return {'title': title, 'subtitle': subtitle, 'content': content}
    except Exception as e:
        print(f'Erro ao extrair conteúdo de {url}: {e}')
        return {}


def get_optimal_thread_count() -> int:
    '''Calcula o número ótimo de threads para operações baseadas em I/O.'''
    return multiprocessing.cpu_count() * 4


def scrape_concurrent(urls: List[str], num_threads: int = None) -> List[Dict[str, str]]:
    '''
    Realiza a extração de notícias de forma concorrente.

    Args:
        urls (List[str]): Lista de URLs a serem extraídas.
        num_threads (int, opcional): Número de threads a serem usadas. 
            Se não fornecido, será calculado automaticamente.

    Returns:
        List[Dict[str, str]]: Lista de dicionários contendo os dados extraídos.
    '''
    num_threads = num_threads or get_optimal_thread_count()
    print(f'Extraindo artigos com {num_threads} threads...')

    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scrape_news_content, url) for url in urls]
        for future in tqdm(futures, total=len(urls), desc='Extraindo artigos'):
            result = future.result()
            if result:
                results.append(result)

    return results


def scrape_all_news(main_url: str, pages: int = 1) -> List[Dict[str, str]]:
    '''
    Função principal para realizar a extração de todas as notícias de um site.

    Args:
        main_url (str): URL principal do site de notícias.
        pages (int): Número de páginas a serem extraídas.

    Returns:
        List[Dict[str, str]]: Lista de dicionários contendo os dados extraídos.
    '''
    urls = get_news_urls(main_url, pages)
    return scrape_concurrent(urls)


def save_results_to_csv(results: List[Dict[str, str]], filename: str = 'news_results.csv') -> None:
    '''
    Salva os resultados extraídos em um arquivo CSV.

    Args:
        results (List[Dict[str, str]]): Lista de dicionários contendo os dados extraídos.
        filename (str, opcional): Nome do arquivo CSV. Padrão: 'news_results.csv'.
    '''
    if not results:
        print('Nenhum resultado para salvar.')
        return

    os.makedirs(NEWS_DATA_DIRECTORY, exist_ok=True)
    filepath = os.path.join(NEWS_DATA_DIRECTORY, filename)
    pd.DataFrame(results).to_csv(filepath, index=False)
    print(f'Resultados salvos em: {filepath}')