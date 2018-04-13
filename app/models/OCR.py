from PIL import Image
from pytesseract import pytesseract, Output


class OCR():

    pytesseract.tesseract_cmd = 'C:/tesseract/Tesseract-OCR/tesseract.exe'

    def __init__(self,filename):
        self.filename = filename

    def __str__(self):
        return 'filename', self.filename,

    def scan_text(self):
        return pytesseract.image_to_string(Image.open(self.filename), output_type=Output.STRING)

    def scan_data(self):

        dict_data = pytesseract.image_to_data(Image.open(self.filename), output_type=Output.DICT)
        json_array = []

        for i in range(len(dict_data['text'])):

            # if is empty
            if len(dict_data['text'][i]) != 0:
                json_line = {
                    'text': dict_data['text'][i],
                    'left': dict_data['left'][i],
                    'top': dict_data['top'][i],
                    'width': dict_data['width'][i],
                    'height': dict_data['height'][i]
                }
                json_array.append(json_line)

        return json_array
