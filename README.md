# Converse com o ChatAmbiental, seu chatbot particular para notícias de jornalismo ambiental!

Esse é um aplicativo Streamlit que serve como uma interface de chat alimentado pelo modelo gemini-1.5-flash através da API Gemini e por um sistema de RAG. O usuário faz uma pergunta através da interface streamlit, 
que é enviada para o endpoint /query da API onde o LLM processa a mensagem, procura no documento por similaridade, gera o texto, e retorna a resposta para a interface Streamlit. O projeto também conta com uma WordCloud
feita com a mesma base de dados usada pelo ChatBot. A base de dados é um arquivo csv contendo resultados do scraping das páginas do jornal ambiental [O Eco](https://oeco.org.br/).

## Built With
![FastAPI](https://img.shields.io/badge/FastAPI-v0.115.5-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-v2.5.1%2Bcu121-orange)
![Transformers](https://img.shields.io/badge/Transformers-v4.46.3-green)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-v0.12.1-yellow)

## Como rodar localmente o modelo

Primeiro, clone este repositório para sua máquina:

```
git clone https://github.com/Leticia-Infnet/leticia_abreu_PB_TP3.git
```
### Baixando a versão correta do Torch
:warning:ATENÇÃO
A biblioteca Torch não está no requirements.txt, apesar de ser essencial para o funcionamento da aplicação. Isso porque as versões do Pytorch dependem do sistema operacional e arquitetura. Se você possui uma GPU compatível com CUDA
siga o tutorial descrito [neste](https://medium.com/@fernandopalominocobo/installing-cuda-for-pytorch-easily-explained-windows-users-4d3b7db5f2e0) artigo para baixar o CUDA Toolkit certo para sua GPU. Abaixo estão os comandos pip para
Windows:

1. Torch para NVIDIA CUDA versão 11.8:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
2. Torch para NVIDIA CUDA versão 12.1:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
3. Torch para NVIDIA CUDA versão 12.4:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```
4. Torch para CPU:
```
pip3 install torch torchvision torchaudio
```

Após baixar a versão certa do Torch de acordo com seu OS e arquitetura, baixe as libs que estão no requirements.txt:
```
pip install -r requirements.txt
```
### Criando arquivo .env, ativando server e interface Streamlit
Na raíz do diretório, crie um arquivo .env contendo sua chave da API do Gemini, como no exemplo abaixo:

GOOGLE_API_KEY = SUA_CHAVE_API

Ative o server uvicorn local rodando o seguinte comando da raíz do diretório:
```
python -m Code.Back.main
```
Ative a interface Streamlit rodando o seguinte comando da raíz do diretório:
```
streamlit run ./Code/Front/Observatório_da_Conservação.py
```













