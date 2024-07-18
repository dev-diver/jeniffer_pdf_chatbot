import fitz
from pathlib import Path
import json

current_dir = Path(__file__).parent
project_dir = current_dir.parent
data_dir = Path(project_dir, "data")
file_path = Path(data_dir, "jeniffer1-2.pdf")
output_path = Path(data_dir, "output.json")

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
                        if(text.strip() != ''):
                            texts[size].append(text)
                    texts = dict(sorted(texts.items(), key=lambda x: x[0], reverse=True))
                for size, text in texts.items():
                    sector_degree = font_size_degree[size]
                    sector_orders[sector_degree] += 1
                    join_text = ' '.join(text)
                    add_sector(root, 0, sector_degree, sector_orders, join_text)

def add_sector(root, current_degree, target_degree, sector_orders, text):
    sector_key = sector_orders[current_degree]
    if current_degree == target_degree:
        # print(text)
        if sector_key not in root:
            root[sector_key] = {"text": text}
        else:
            root[sector_key]["text"] = text
    else:
        current_degree_key = sector_orders[current_degree]
        if sector_key not in root:
            root[sector_key] = {}
        if current_degree_key not in root[sector_key]:
            root[sector_key][current_degree_key] = {}
        add_sector(root[sector_key][current_degree_key], current_degree+1, target_degree, sector_orders, text)

make_hiearachy()

def get_degree_text(root, current_degree, target_degree, texts):
    print(current_degree, root.keys())
    if current_degree == target_degree:
        if("text" in root):
            texts.append(root["text"])
            return
    if(current_degree > target_degree):
        return
    for key in root:
        if(key != "text"):
            get_degree_text(root[key], current_degree+1, target_degree, texts)
            
texts = []
get_degree_text(root, 0, 5, texts)
print(texts)
# pretty_json = json.dumps(root, indent=2, ensure_ascii=False)
# print(pretty_json)

# with open(output_path, "w", encoding='utf-8') as file:
#     file.write(pretty_json)