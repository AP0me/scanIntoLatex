import cv2; import pytesseract; import re;
import json; import numpy as np

def extract_text_regions(image_path, output_file='ocr_results.json', show_image=False, colorize_white=False):
  output_file = "./output/" + output_file
  image = cv2.imread(image_path)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16, 5))
  morph = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
  thresh = cv2.threshold(morph, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  ocr_results = []

  for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    roi_gray = gray[y:y + h, x:x + w]
    
    if colorize_white:
      brightness_threshold = 150
      _, mask = cv2.threshold(roi_gray, brightness_threshold, 255, cv2.THRESH_BINARY)
      roi_gray[mask != 0] = 255

    text = pytesseract.image_to_string(roi_gray, lang='eng', config="--psm 7").strip()
    whitelist_pattern = re.compile(r'[^a-zA-Z0-9\s,.!?;:\'\"-]')
    text = whitelist_pattern.sub('', text)
    if text:
      ocr_results.append({"text": text, "coordinates": (x, y, x + w, y + h)})

    cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

  if show_image:
    cv2.imshow('Detected Text Regions', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  with open(output_file, 'w') as f:
    json.dump(ocr_results, f)

  return image.shape

image_path = './input/sffCapture.png'
image_shape = extract_text_regions(image_path, show_image=True, colorize_white=True)

