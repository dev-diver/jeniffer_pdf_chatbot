from langchain_community.document_loaders import PyPDFLoader
import fitz
import re
import math
from pathlib import Path

font_size = {
    "chapter_num": 79,
    "chapter": 24,
    "h1": 19,
    "h2": 13,
    "h3": 12,
    "p": 9,
    "tr": 7,
}

page_margin = 730

def classify_text(text_size, block_font, last_y):
    text_size = math.floor(text_size)
    if(last_y >= page_margin):
        return "page"
    for text_type, size_value in font_size.items():
        if text_size == size_value:
            return text_type
    return "u"

def group_text_by_proximity(text_blocks, threshold=10):

    def append_group_text():
        current_text = "".join(current_group)
        grouped_text.append({
            "class": classify_text(current_size, current_font,last_y),
            "text": current_text,
            "y": last_y
        })

    current_size = None
    grouped_text = []
    current_group = []
    last_y = None
    
    current_size = text_blocks[0]['size']
    current_font = text_blocks[0]['font']
    for block in text_blocks:
        block_text, block_bbox, block_size, block_font = block['text'], block['bbox'], block['size'], block['font']
        block_y = block_bbox[1]

        if last_y is not None and abs(block_y - last_y) > threshold:
            append_group_text()
            current_size = block_size
            current_font = block_font
            current_group = []
        
        current_group.append(block_text)
        last_y = block_y
    
    if current_group:
        append_group_text()
    
    grouped_text = sorted(grouped_text, key=lambda x: x['y'])
    return grouped_text

def print_page(document, page_num):
    page = document.load_page(page_num)
    text_page = page.get_text("dict")
    
    text_blocks = []
    for block in text_page["blocks"]:
        if block["type"] == 0:
            for line in block["lines"]:
                for span in line["spans"]:
                    text_blocks.append({
                        "text": span["text"],
                        "bbox": span["bbox"],
                        "size" : span["size"],
                        "font" : span["font"],
                    })
    
    grouped_text = group_text_by_proximity(text_blocks, threshold=16)
    return grouped_text

def split_sentences(obj):
    if obj['class'] != 'p':
        return [obj]
    text = obj['text']
    class_ = obj['class']
    splits = re.split(r'(?<=\.)\s+', text)
    objs = []
    for s in splits:
        if s.strip() == "":
            continue
        objs.append({
            "class": class_,
            "text": s
        })
    return objs

def extract_structure(document):
    output = []
    for page_num in range(document.page_count):
        objs = print_page(document, page_num)
        for obj in objs:
            split_objs = split_sentences(obj)
            for split_obj in split_objs:
                output.append(split_obj)
    return output

def output_with_tag(output):
    lines = []
    for obj in output:
        lines.append(f"{obj['class']}: {obj['text']}")
    return lines

def prettier_output(output):
    lines = []
    for obj in output:
        if obj['class'] == 'page':
            continue
        if obj['class'] == 'chapter_num':
            lines.append("-" * 50)
        if obj['class'] == 'h1':
            lines.append("-" * 10)
        if obj['class'] == 'h2':
            lines.append("")
        if obj['class'] == 'h3':
            lines.append("")
        lines.append(obj['text'])
    return lines

def write_output(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(lines))

current_dir = Path(__file__).parent
project_dir = current_dir.parent
chroma_path = Path(project_dir, "chroma")
file_path = Path(project_dir, "data", "jeniffer1-2.pdf")
output_path = Path(project_dir, "data", "output.txt")
print("chromapath: ", str(chroma_path))
print(file_path)

document = fitz.open(file_path)
output = extract_structure(document)
write_output(output_path, prettier_output(output))


        
