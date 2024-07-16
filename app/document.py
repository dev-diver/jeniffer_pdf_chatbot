from pathlib import Path
import pandas as pd
from pymongo import MongoClient
current_dir = Path(__file__).parent
project_dir = current_dir.parent
file_path = Path(project_dir, "data", "jeniffer.csv")
print(file_path)

df = pd.read_csv(file_path)

client = MongoClient('mongodb://localhost:27017/')
db = client['jeniffer']
collection = db['raw']

collection.insert_many(df.to_dict('records'))