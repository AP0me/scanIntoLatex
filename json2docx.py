from docx import Document
from docx.shared import Pt
import json

def generate_docx_with_tabs_spaces_fontsize(input_file='ocr_results.json', output_filename="output.docx", dpi=96):
    input_file = "./output/" + input_file
    output_filename = "./output/" + output_filename
    with open(input_file, 'r') as f:
        ocr_results = json.load(f)

    doc = Document()
    for result in reversed(ocr_results):
        x1, y1, x2, y2 = result["coordinates"]
        text = result["text"]
        text_height = y2 - y1
        tab_count = x1 // 100  
        space_count = (x1 % 100) // 10  
        font_size = text_height * 72 / dpi  
        line = '\t' * tab_count + ' ' * space_count + text
        paragraph = doc.add_paragraph(line)
        run = paragraph.runs[0]
        run.font.size = Pt(font_size)

    doc.save(output_filename)
    return output_filename

docx_file = generate_docx_with_tabs_spaces_fontsize(input_file='ocr_results.json')
print(f"DOCX file '{docx_file}' generated successfully with adjusted font size and simulated positioning.")
