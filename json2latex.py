import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def pixels_to_points(pixels, dpi=72):
  return pixels * dpi / 96  

def generate_pdf(input_file='ocr_results.json', image_shape=(1024, 768), output_filename="output.pdf", dpi=96):
  with open(input_file, 'r') as f:
    ocr_results = json.load(f)

  c = canvas.Canvas(output_filename, pagesize=letter)
  width, height = letter  

  for result in reversed(ocr_results):
    x1, y1, x2, y2 = result["coordinates"]
    text = result["text"]
    font_size = pixels_to_points(y2 - y1, dpi)
    x = pixels_to_points(x1, dpi)
    y = height - pixels_to_points(y2, dpi)  
    c.setFont("Helvetica", font_size)
    c.drawString(x, y, text)

  c.save()
  return output_filename

pdf_file = generate_pdf(input_file='ocr_results.json')
print(f"PDF file '{pdf_file}' generated successfully from JSON data.")
