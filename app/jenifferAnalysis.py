import fitz
from pathlib import Path
from collections import defaultdict

current_dir = Path(__file__).parent
project_dir = current_dir.parent
data_dir = Path(project_dir, "data")
file_path = Path(data_dir, "jeniffer_full.pdf")
output_path = Path(data_dir, "output.txt")

document = fitz.open(file_path)

files = {}

for page_num, page in enumerate(document):
    text_page = page.get_text("dict")
    text_blocks = []
    for block_num, block in enumerate(text_page["blocks"]):
        if block["type"] == 0:
            for line_num, line in enumerate(block["lines"]):
                for span in line["spans"]:
                    obj_key = f'{round(span["size"])}'
                    if obj_key not in files:
                        files[obj_key] = {}
                    if page_num not in files[obj_key]:
                        files[obj_key][page_num] = {}
                    if block_num not in files[obj_key][page_num]:
                        files[obj_key][page_num][block_num] = []
                    if(span["text"].strip() != ''):
                        files[obj_key][page_num][block_num].append(span["text"])

line_counter = defaultdict(int)
for key, file_contents in files.items():
    file_name = f"jen_{key}.txt"
    with open(Path(data_dir, file_name), 'w', encoding='utf-8') as file:
        for page_num, page_contents in file_contents.items():
            file.write(f"\n-- {page_num+1} p --")
            for line_num, line in page_contents.items():
                file.write(f"\n{line_num+1} :")
                line_counter[key] += 1
                for text in line:
                    file.write(text)
                    file.write(' ')

line_count = sorted(line_counter.items(), key=lambda x: x[1], reverse=True)
print("--sizes--")
print(*map(lambda x: x[0], line_count), sep='\n')
print("--blocks--")
print(*map(lambda x: x[1], line_count), sep='\n')
