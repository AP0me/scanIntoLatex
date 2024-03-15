import cv2
import pytesseract
import re
import json

def extract_text_regions(image_path, output_file='ocr_results.json'):
  image = cv2.imread(image_path)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
  morph = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
  thresh = cv2.threshold(morph, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  ocr_results = []
  for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    roi = gray[y:y+h, x:x+w]
    text = pytesseract.image_to_string(roi, lang='eng', config="--psm 7").strip()
    
    whitelist_pattern = re.compile(r'[^a-zA-Z0-9\s,.!?;:\'\"-]')
    text = whitelist_pattern.sub('', text)
    if text:
      ocr_results.append({"text": text, "coordinates": (x, y, x+w, y+h)})
  with open(output_file, 'w') as f:
    json.dump(ocr_results, f)
  return image.shape

# Example usage
image_path = 'input.png'  # Replace with your image path
image_shape = extract_text_regions(image_path)
