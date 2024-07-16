from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from document import docs

embeddings_model = HuggingFaceEmbeddings()
vectorstore = Chroma.from_documents(
    docs,
    embedding=embeddings_model,
)
print("embed complete")
retriever = vectorstore.as_retriever()