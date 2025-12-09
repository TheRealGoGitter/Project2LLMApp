import streamlit as st
from langchain_ollama import ChatOllama
from pdfminer.high_level import extract_text
import docx2txt
from bs4 import BeautifulSoup

llm = ChatOllama(
    model='llama3.2',
    temperature=0.1
)

st.title('Input to AI')

question = st.text_input('Enter your question:')
files = st.file_uploader('Upload attachment:', type=['txt', 'pdf', 'docx', 'html'], accept_multiple_files=True)

context_text = ''

if files is not None:
    try:
        for file in files:
            if file.name.endswith('.pdf'):
                context_text = extract_text(file)
                
            elif file.name.endswith('.docx'):
                context_text = docx2txt.process(file)
                
            elif file.name.endswith('.html'):
                soup = BeautifulSoup(file, 'html.parser')
                context_text = soup.text
                
            elif file.name.endswith(".txt"):
                context_text = file.read().decode("utf-8")
            
    except Exception as e:
        st.error(f'Error reading file: {e}')

final_prompt = f'Context from file:\n{context_text}\n\nQuestion:\n{question}'

ai_msg = llm.invoke(final_prompt)

st.title('AI Response:')
st.text(ai_msg.content)