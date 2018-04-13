import os
import sys
from os import listdir

from app.models.DataBase import PdfFile

pdfs = PdfFile.query.all()

dir = os.path.join(os.getcwd(), 'upload')
pdf_dir = os.path.join(dir, 'pdf')

if __name__ == '__main__':

    file_pdfs = [f.path+'.pdf' for f in pdfs]
    files = [f for f in listdir(pdf_dir) if os.path.isfile(os.path.join(pdf_dir, f))]

    for file in files:
        if file not in file_pdfs:
            path_file = os.path.join(pdf_dir, file)
            print(path_file)
            #os.remove(path_file)
    print('end')