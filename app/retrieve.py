import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
from langchain.docstore.document import Document

from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
logging.langsmith("jeniffer_RAG")

current_dir = Path(__file__).parent
project_dir = current_dir.parent
data_dir = Path(project_dir, "data")
text_file = Path(data_dir, "paragrah.txt")

docs = []

with open(text_file, "r", encoding="utf-8") as file:
    for line in file:
        if line.strip():  # 빈 줄 제외
            docs.append(Document(page_content=line.strip()))
print("문서 로드 완료")

embeddings = OllamaEmbeddings(model="EEVE:latest")

vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)
print("벡터 저장소 생성 완료")

vectorstore.save_local("fasis_paragraph")
print("벡터 저장소 저장 완료")

retriever = vectorstore.as_retriever()

prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Answer in Korean.

#Question: 
{question} 
#Context: 
{context} 

#Answer:"""
)

llm = ChatOllama(model="EEVE:latest")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("질문중")
question = "어플리케이션 성능 관리에 대해서 알려줘"
response = chain.invoke(question)
print(response)