import fitz
from pathlib import Path

current_dir = Path(__file__).parent
project_dir = current_dir.parent
data_dir = Path(project_dir, "data")
file_path = Path(data_dir, "jeniffer_full.pdf")
output_path = Path(data_dir, "output.txt")

document = fitz.open(file_path)

size_hash = set()

sizes = [1.9800000190734863, 6.960000038146973, 7.019999980926514, 7.980000019073486, 9.0, 9.479999542236328, 9.960000038146973, 10.020000457763672, 12.0, 13.979999542236328, 14.399999618530273, 18.0, 19.979999542236328, 24.959999084472656, 30.0, 34.97999954223633, 45.0, 79.9800033569336]
files = {x:{} for x in sizes}
print(files)

for i, page in enumerate(document):
    text_page = page.get_text("dict")
    text_blocks = []
    for block in text_page["blocks"]:
        if block["type"] == 0:
            for page in block["lines"]:
                for span in page["spans"]:
                    if i not in files[span["size"]]:
                        files[span["size"]][i] = []
                    files[span["size"]][i].append(span["text"])

for key, value in files.items():
    print(key, len(value))
    file_name = f"jen_{key}.txt"
    with open(Path(data_dir, file_name), 'w', encoding='utf-8') as file:
        for page in value:
            file.write(f"\n{page+1} page :\n")
            for line in value[page]:
                file.write(line)
                file.write(' ')
