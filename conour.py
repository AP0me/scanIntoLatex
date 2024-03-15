
import cv2
import pytesseract
from pytesseract import Output

def extract_text_regions_and_show(image_path):
  image = cv2.imread(image_path)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
  morph = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
  thresh = cv2.threshold(morph, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  text_regions = []
  for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)    
    roi = gray[y:y+h, x:x+w]
    text = pytesseract.image_to_string(roi, lang='eng', config = "--psm 7")
    if text.strip() != '':
      text_regions.append(text.strip())
      print(f"Detected text region: Top-Left: ({x}, {y}), Bottom-Right: ({x+w}, {y+h})")
  cv2.imshow('Detected Text Regions', image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  return text_regions

image_path = 'input.png'
text_regions = extract_text_regions_and_show(image_path)
print(text_regions)

