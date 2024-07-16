from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from document import splits

embeddings_model = HuggingFaceEmbeddings()
vectorstore = Chroma.from_documents(
    splits,
    embedding=embeddings_model,
)
print("embed complete")
retriever = vectorstore.as_retriever()