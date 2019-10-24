# import pytesseract
# from PIL import Image
# pytesseract.pytesseract.tesseract_cmd = \
#     r"D:\tesseract4win64-master\x64\tesseract.exe"
# image = Image.open('D:/tesseract-master/tesseract_demo/shici.png')
# text = pytesseract.image_to_string(image=image,lang='chi_sim')
# print(text)

import  pytesseract
from PIL import  Image
pytesseract.pytesseract.tesseract_cmd = \
    r"D:\tesseract4win64-master\x64\tesseract.exe"
image = Image.open('D:/tesseract-master/tesseract_demo/shici.png')
text = pytesseract.image_to_data(image,lang='chi_sim')
print(text)