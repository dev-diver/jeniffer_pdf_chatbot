from langchain_chroma import Chroma
import chromadb
from pathlib import Path
import pandas as pd
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

current_dir = Path(__file__).parent
project_dir = current_dir.parent
chroma_path = Path(project_dir, "chroma")
file_path = Path(project_dir, "data", "jeniffer_text.csv")
print("chromapath: ", str(chroma_path))
print(file_path)

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
croma_client = chromadb.PersistentClient(path=str(chroma_path))
collection = croma_client.get_or_create_collection("text")

df = pd.read_csv(file_path)
*ids, = map(lambda x :str(x),df.index.tolist())
documents = df['contents'].tolist()
metadatas = df[['class','path','page','order']].to_dict('records')

collection.add(
  documents=documents,
  metadatas=metadatas,
  ids=ids
)


