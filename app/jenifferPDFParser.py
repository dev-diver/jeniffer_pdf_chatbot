import fitz
import re
import math
from pathlib import Path
from dataclasses import dataclass

font_size = {
    "chapter_num": 79,
    "chapter": 24,
    "header1": 19,
    "header2": 13,
    "header3": 12,
    "text": 9,
    "table_row": 7,
}

page_margin = 730

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

def group_text_by_proximity(text_blocks, threshold=10):

    def append_group_text():
        current_text = "".join(current_group)
        grouped_text.append({
            "tag": classify_text(current_size ,last_y),
            "contents": current_text,
            "y": last_y
        })

    current_size = None
    grouped_text = []
    current_group = []
    last_y = None
    
    current_size = text_blocks[0]["size"]
    # current_font = text_blocks[0]["font"]
    for block in text_blocks:
        block_text, block_bbox, block_size = block["text"], block["bbox"], block["size"]
        # block_font = block["font"]
        block_y = block_bbox[1]

        if last_y is not None and abs(block_y - last_y) > threshold:
            append_group_text()
            current_size = block_size
            # current_font = block_font
            current_group = []
        
        current_group.append(block_text)
        last_y = block_y
    
    if current_group:
        append_group_text()
    
    grouped_text = sorted(grouped_text, key=lambda x: x["y"])
    return grouped_text

def classify_text(text_size, last_y):
    text_size = math.floor(text_size)
    if(last_y >= page_margin):
        return "page"
    for text_type, size_value in font_size.items():
        if text_size == size_value:
            return text_type
    return "u"

def split_sentences(obj):
    if obj["tag"] != "text":
        return [obj]
    text = obj["contents"]
    splits = re.split(r'(?<=\.)\s+', text)
    objs = []
    for s in splits:
        if s.strip() == "":
            continue
        objs.append({
            "tag": obj["tag"],
            "contents": s,
            "path": obj['path'],
            "page": obj['page'],
        })
    return objs

def extract_structure(document):

    chapter = 0
    h1 = 0
    h2 = 0
    h3 = 0
    p = 0

    def tag(obj, page_num):
        nonlocal chapter, h1, h2, h3, p
        if obj["tag"] == "chapter_num":
            chapter += 1
            h1, h2, h3, p = 0, 0, 0, 0
        if obj["tag"] == "header1":
            h1 += 1
            h2, h3, p = 0, 0, 0
        if obj["tag"] == "header2":
            h2 += 1
            h3, p = 0, 0
        if obj["tag"] == "header3":
            h3 += 1
            p = 0
        if obj["tag"] == "text":
            p += 1
        obj['path'] = "/".join([str(chapter), str(h1), str(h2), str(h3), str(p)])
        obj['page'] = page_num + 1
        
    output = []
    for page_num in range(document.page_count):
        objs = print_page(document, page_num)
        for obj in objs:
            tag(obj, page_num)
            split_objs = split_sentences(obj)
            for split_obj in split_objs:
                output.append(split_obj)
    return output

def output_with_tag(output):
    lines = []
    for obj in output:
        formatted_string = f'{obj["tag"]:<10} : {obj["path"]:<10} : {obj["contents"]:<20}'
        lines.append(formatted_string)
    return lines

def prettier_output(output):
    lines = []
    for obj in output:
        if obj["tag"] == "page":
            # lines.append(f"{'>' * 50} {obj['text']} {'<' * 50}")
            continue
        if obj["tag"] == "chapter_num":
            lines.append("-" * 50)
        if obj["tag"] == "header1":
            lines.append("-" * 10)
        if obj["tag"] == "header2":
            lines.append("")
        if obj["tag"] == "header3":
            lines.append("")
        lines.append(obj['contents'])
    return lines

def write_output(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(lines))

current_dir = Path(__file__).parent
project_dir = current_dir.parent
data_dir = Path(project_dir, "data")
chroma_path = Path(project_dir, "chroma")
file_path = Path(data_dir, "jeniffer1-2.pdf")
output_path = Path(data_dir, "output_with_page.txt")

document = fitz.open(file_path)
structure = extract_structure(document)
output = output_with_tag(structure)
# output = prettier_output(structure)
print(*output, sep="\n")
# write_output(output_path, output)


        
