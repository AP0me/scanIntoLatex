import json

def pixels_to_inches(pixels, dpi=96):
  return pixels / dpi  # Convert pixels to inches based on DPI

def generate_latex(input_file='ocr_results.json', image_shape=(1024, 768), output_filename="output.tex", dpi=96):
  width_inches = pixels_to_inches(image_shape[1], dpi)
  height_inches = pixels_to_inches(image_shape[0], dpi)

  with open(input_file, 'r') as f:
    ocr_results = json.load(f)

  with open(output_filename, 'w') as file:
    file.write("\\documentclass{article}\n")
    file.write("\\usepackage[margin=0in, paperwidth=" + str(width_inches) + "in, paperheight=" + str(height_inches) + "in]{geometry}\n")
    file.write("\\usepackage[absolute,overlay]{textpos}\n")
    file.write("\\setlength{\\TPHorizModule}{1in}\n")  # 1 unit = 1 inch
    file.write("\\setlength{\\TPVertModule}{1in}\n")
    file.write("\\begin{document}\n")

    for result in ocr_results:
      x1, y1, x2, y2 = result["coordinates"]
      text_height_inches = pixels_to_inches(y2 - y1, dpi)
      font_size = text_height_inches * 72  # Convert inches to points
      baselineskip = font_size * 1.2  # Example baseline skip

      x_inches = pixels_to_inches(x1, dpi)
      y_inches = pixels_to_inches(y2, dpi)  # Flip y-coordinate for LaTeX

      text = result["text"].replace("&", "\\&").replace("%", "\\%")
      file.write(f"\\begin{{textblock*}}{{{width_inches}in}}({x_inches}in,{y_inches}in)\n")
      file.write(f"\\fontsize{{{font_size:.2f}}}{{{baselineskip:.2f}}}\selectfont\n")
      file.write(f"{text}\n")
      file.write("\\end{textblock*}\n")

    file.write("\\end{document}\n")

latex_file = 'output.tex'  # Output LaTeX file name
generate_latex(input_file='ocr_results.json', output_filename=latex_file)
print(f"LaTeX file '{latex_file}' generated successfully with positioned and sized text.")
