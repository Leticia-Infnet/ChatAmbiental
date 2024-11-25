import streamlit as st
import requests
from requests.exceptions import RequestException

st.set_page_config(page_title='ChatAmbiental',
                   page_icon='🤖')

# Configuration
API_URL = 'http://localhost:8000/query'
ERROR_MESSAGE = 'Desculpe, ocorreu um erro ao processar sua pergunta. Por favor, tente novamente.'

# Initialize chat session state if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# App header
st.title('🤖Converse com o ChatAmbiental, seu jornalista ambiental particular!')
st.markdown('<div style="text-align: justify;">Este é o ChatAmbiental: ele faz scraping das últimas notícias ambientais do site jornal ((o))eco e responde suas perguntas baseando-se nelas! Faça perguntas sobre queimadas, desmatamento, mudanças climáticas etc e veja o que ele responde.</div>', unsafe_allow_html=True)
st.info('Esse chatbot se lembra da conversa e produz respostas de acordo com o contexto')

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Handle user input
if user_input := st.chat_input('Faça uma pergunta'):
    # Add user message to chat
    st.session_state.messages.append({'role': 'user', 'content': user_input})

    # Show user message immediately
    with st.chat_message('user'):
        st.write(user_input)

    # Show assistant response with spinner
    with st.chat_message('assistant'):
        try:
            with st.spinner('Pensando...'):
                response = requests.post(
                    API_URL,
                    json={'question': user_input},
                )
                response.raise_for_status()  # Raise exception for bad status codes
                answer = response.json().get('answer', ERROR_MESSAGE)
                st.write(answer)

            # Add assistant response to chat history
            st.session_state.messages.append(
                {'role': 'assistant', 'content': answer})

        except RequestException as e:
            error_message = f'Erro de conexão: {str(e)}'
            st.error(error_message)
            st.session_state.messages.append(
                {'role': 'assistant', 'content': ERROR_MESSAGE})
