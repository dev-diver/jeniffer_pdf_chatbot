import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from vectorstore import retriever

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

model = ChatOllama(model="EEVE:latest")
parser = StrOutputParser()

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

summary_prompt = (
    "You are an AI language model designed to summarize texts. Your goal is to provide concise and accurate summaries while preserving the main points and essential information of the original text. Follow these guidelines:"
    "1. **Understand the Text**: Read the entire text to grasp the main ideas and overall context."
    "2. **Identify Key Information**: Extract sentences or phrases that contain the most critical information."
    "3. **Eliminate Redundancies**: Remove repetitive or non-essential details, focusing on the core message."
    "4. **Write Concisely**: Rewrite the key information in a brief, clear, and coherent manner."

    "Ensure the summary:"
    "- Captures the main points of the original text."
    "- Is significantly shorter than the original text."
    "- Maintains the original text's meaning and context."

    "Example:"

    "Original Text:"
    "'Climate change is a significant issue affecting the entire planet. Recent studies show that it causes sea levels to rise, impacting coastal areas significantly. Additionally, climate change leads to extreme weather patterns, increasing the frequency of natural disasters such as floods and droughts.'"

    "Summary:"
    "'Climate change causes sea level rise and extreme weather patterns, leading to more frequent natural disasters.'"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", summary_prompt),
        ("human", "{input}"),
    ]
)

chain = prompt | model
# question_answer_chain = create_stuff_documents_chain(model, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)

results = chain.invoke({"input": "애플리케이션 성능 관리(Application Performance Management, 이하 APM)는 애플리케이션 서비스에 대한 효율적인 성능 모니터링 및 성능 장애 대응 전략을 수립하고 미래 예측을 가늠하는 일련의 지속적인 성능 관리 체계를 구축하는 것이다."})

print(results)