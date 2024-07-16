from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
current_dir = Path(__file__).parent
project_dir = Path(current_dir, "..")
file_path = Path(project_dir, "data", "jeniffer1-2.pdf")
print(file_path)

loader = PyPDFLoader(file_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
