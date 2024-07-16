from langchain_chroma import Chroma
from pathlib import Path
import chromadb
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

current_dir = Path(__file__).parent
project_dir = current_dir.parent
chroma_path = Path(project_dir, "chroma")
print("chromapath: ", str(chroma_path))

chroma_client = chromadb.PersistentClient(path=str(chroma_path))
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    client=chroma_client,
    collection_name="text",
    embedding_function=embedding_function,
)

query = "APM이란"
docs = vectorstore.similarity_search(query)
print(docs)

# retriever = vectorstore.as_retriever()