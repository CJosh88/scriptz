import sys
import os
from dotenv import load_dotenv
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

def main():
    #load_dotenv()
    os.environ["OPENAI_API_KEY"] = "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"
    st.set_page_config(page_title="Welcome to your IQConverse™ AI HR assistance-bot!")
    st.header("Ask your PDF 💬")
    
    # upload file
    #pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    # extract the text
    documents = []
    for file in os.listdir("docs"):
        if file.endswith(".pdf"):
            pdf_path = "./docs/" + file
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        elif file.endswith('.docx') or file.endswith('.doc'):
            doc_path = "./docs/" + file
            loader = Docx2txtLoader(doc_path)
            documents.extend(loader.load())
        elif file.endswith('.txt'):
            text_path = "./docs/" + file
            loader = TextLoader(text_path)
            documents.extend(loader.load())
        
      # split into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    documents = text_splitter.split_documents(documents)
      
      # create embeddings
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory="./data")
    vectordb.persist()
      
      # llm chain      
    pdf_qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        vectordb.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True,
        verbose=False
        )
        
      # show user input
    chat_history = []
    user_question = st.text_input("How can I help you today?:")
    if user_question:
        response = pdf_qa(
            {"question": user_question, "chat_history": chat_history}
            )
    
        chat_history.append((user_question, response["answer"]))
        st.write(response["answer"])
        
 
if __name__ == '__main__':
    main()
