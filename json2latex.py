import json
from docx import Document
from docx.shared import Pt

def generate_docx_with_tabs_spaces_fontsize(input_file='ocr_results.json', output_filename="output.docx", dpi=96):
    with open(input_file, 'r') as f:
        ocr_results = json.load(f)

    doc = Document()

    for result in reversed(ocr_results):
        x1, y1, x2, y2 = result["coordinates"]
        text = result["text"]
        text_height = y2 - y1

        # Calculate number of tabs and spaces needed for positioning
        # This is a rough approximation and may need adjustment
        tab_count = x1 // 100  # Assuming each tab approximates 100 pixels
        space_count = (x1 % 100) // 10  # Assuming each space approximates 10 pixels

        # Calculate font size
        font_size = text_height * 72 / dpi  # Convert pixels to points

        # Construct the line with tabs and spaces for positioning
        line = '\t' * tab_count + ' ' * space_count + text

        # Add the line to the document and set font size
        paragraph = doc.add_paragraph(line)
        run = paragraph.runs[0]
        run.font.size = Pt(font_size)

    doc.save(output_filename)
    return output_filename

docx_file = generate_docx_with_tabs_spaces_fontsize(input_file='ocr_results.json')
print(f"DOCX file '{docx_file}' generated successfully with adjusted font size and simulated positioning.")
