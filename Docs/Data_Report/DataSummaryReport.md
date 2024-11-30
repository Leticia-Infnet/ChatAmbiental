# Data Summary Report: ChatAmbiental

## Fonte de Dados: Webscraping do Jornal ((o)) eco

### Caracterização dos Dados

- **Tipo de Dado**: HTML semi-estruturado
- **Fonte**: Portal ((o)) eco (https://oeco.org.br)
- **Período**: Notícias de 2024
- **Categorias Coletadas**:
  - Notícias
  - Reportagens especiais
  - Conteúdo ambiental

### Processo de Coleta de Dados

#### Metodologia de Webscraping

- **Ferramenta**: Biblioteca BeautifulSoup com uso de multithreading
- **Páginas Coletadas**:
  - Categoria Notícias: 5 páginas
  - Categoria Reportagens: 5 páginas
- **Dados Extraídos**:
  - Título da matéria
  - Subtítulo da matéria
  - Texto completo
  - Data de publicação
  - URL

#### Pré-processamento de Dados

- **Limpeza**:
  - Remoção de tags HTML
  - Normalização de texto
  - Remoção de caracteres especiais
- **Transformação**:
  - Conversão para formato CSV
  - Encoding: Latin-1
  - Fragmentação em chunks de 2000 caracteres

### Modelo de Dados

- **Estrutura**:
  ```python
  {
    "title": str,
    "subtitle": str,
    "content": str,
    "published_time": str,
    "url": str
  }
  ```

### Desafios de Coleta

- Variabilidade na estrutura HTML
- Necessidade de tratamento de encoding
- Respeito a limites de requisições

### Métricas de Coleta

- **Total de Documentos Coletados**: ~50-100 documentos
- **Tamanho Médio do Documento**: 3000-5000 caracteres
- **Cobertura Temática**: Meio ambiente, conservação, mudanças climáticas
