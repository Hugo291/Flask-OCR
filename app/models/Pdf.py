import os

from pdf2image import pdf2image
from PyPDF2 import PdfFileReader


def page_number(input_pdf_file):
    return PdfFileReader(open(input_pdf_file, 'rb')).getNumPages()


def convert_to_jpg(input_pdf_file, target_dir, num_page=0, fname_fmt="{num_page}.jpg"):
    if not os.path.exists(target_dir):
        # create folder if not exist
        os.makedirs(target_dir)

    images = pdf2image.convert_from_path(input_pdf_file, first_page=num_page+1, last_page=num_page + 2)

    path_file = os.path.join(target_dir, fname_fmt.format(num_page=num_page))
    print('save : ' + path_file)
    images[0].save(path_file)



