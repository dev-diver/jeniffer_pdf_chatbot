import fitz
from pathlib import Path
import json

current_dir = Path(__file__).parent
project_dir = current_dir.parent
data_dir = Path(project_dir, "data")
file_path = Path(data_dir, "jeniffer1-2.pdf")
output_path = Path(data_dir, "paragrah.txt")

document = fitz.open(file_path)

def get_font_sizes(document):
    font_size = set()
    for page in document:
        text_page = page.get_text("dict")
        for block in text_page["blocks"]:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_size.add(round(span["size"]))
    return font_size

font_size = get_font_sizes(document)
font_size_degree = {size: i for i, size in enumerate(sorted(font_size, reverse=True))}
print(font_size_degree)

root = {}

def make_hiearachy():
    sector_orders = [0]*len(font_size)
    for page in document:
        text_page = page.get_text("dict")
        for block in text_page["blocks"]:
            if block["type"] == 0:
                texts = {}
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        size = round(span["size"])
                        if(size not in texts):
                            texts[size] = []
                        texts[size].append(text)
                texts = dict(sorted(texts.items(), key=lambda x: x[0], reverse=True))
                for size, text in texts.items():
                    sector_degree = font_size_degree[size]
                    sector_orders[sector_degree] += 1
                    join_text = ''.join(text)
                    add_sector(root, 0, sector_degree, sector_orders, join_text)

def add_sector(root, current_degree, target_degree, sector_orders, text):
    sector_key = sector_orders[current_degree]
    if current_degree == target_degree:
        if sector_key not in root:
            root[sector_key] = {"text": text}
        else:
            root[sector_key]["text"] = text
    else:
        if sector_key not in root:
            root[sector_key] = {}
        add_sector(root[sector_key], current_degree+1, target_degree, sector_orders, text)

make_hiearachy()

def get_degree_text_recurssive(root, current_degree, target_degree, texts):
    if current_degree == target_degree:
        if("text" in root):
            texts.append(root["text"])
        return
    for key in root:
        if(key != "text"):
            get_degree_text_recurssive(root[key], current_degree+1, target_degree, texts)

def get_degree_text(degree):
    texts = []
    get_degree_text_recurssive(root, 0, degree, texts)
    return texts

texts = get_degree_text(6)
print(texts)

with open(output_path, "w", encoding='utf-8') as file:
    for line in texts:
        text = line.strip()
        if(text != ""):
            file.write(text + "\n")