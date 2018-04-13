import os
import time
from pprint import pprint
from threading import Thread

from app.config import UPLOAD_DIR_PDF, UPLOAD_DIR_JPG
from app.models.OCR import OCR
from app.models.Pdf import convert_to_jpg


class ScannerThread(Thread):
    """
    Construct
    """

    def __init__(self):
        super().__init__()
        self.list_file = []

    """
    Start the thread
    """

    def start(self):
        super().start()

    """
    Run 
    Loop infinit and if detect a file in list , the 
    """

    def run(self):
        super().run()
        while True:
            time.sleep(10)
            while self.has_file_on_hold():
                pdf_file = self.get_last_file()[0]
                pdf_file_id = self.get_last_file()[1]
                self.Scan(pdf_file, pdf_file_id)
                self.delete_last_file()

    """
    Return True if a file is in list 
    """

    def has_file_on_hold(self):
        if len(self.list_file) != 0:
            return True
        return False

    """
    Return the first file to be scan
    """

    def get_last_file(self):
        return self.list_file[0]

    """
    Delete the last file to be scan 
    """

    def delete_last_file(self):
        del self.list_file[0]

    """
    Add a file in list to be scan
    """

    def append_file(self, file, pdf_file_id):
        tuple_file = (file, pdf_file_id)
        self.list_file.append(tuple_file)

    """
    convert file in jpg
    """

    def convert_to_jpg(self, file_number):

        if os.path.isfile(os.path.join(UPLOAD_DIR_PDF, str(file_number) + ".pdf")):

            file_path = os.path.join(UPLOAD_DIR_PDF, str(file_number) + ".pdf")
            dir_dest = os.path.join(UPLOAD_DIR_JPG, str(file_number))

            print("convertion started")

            number_page = convert_to_jpg(file_path, dir_dest)

            print("convertion is finished")

            return number_page
        else:
            print("Erreur le fichier n'est pas reconnu")
            raise Exception('The file is not supported')

    """
    Analyse the file 
    """

    def ocr_jpg(self, folder_number, pdf_file_id, number_file):

        from app.models.DataBase import OCRPage, db, OcrBoxWord, PdfFile

        # ckeck if the fodler exist
        if os.path.isdir(os.path.join(UPLOAD_DIR_JPG, str(folder_number))):

            # folder with all jpg
            folder = os.path.join(UPLOAD_DIR_JPG, str(folder_number))

            # for all file
            for index in range(number_file):

                image_ocr = OCRPage(pdf_file_id=pdf_file_id, num_page=index)

                path_file_img = os.path.join(folder, '{}.jpg'.format(str(index)))

                print('Current file : ' + path_file_img)

                scanner_ocr = OCR(path_file_img)
                image_ocr.text = scanner_ocr.scan_text()

                db.session.add(image_ocr)
                db.session.commit()

                id_pdf_page = image_ocr.id

                box_word = scanner_ocr.scan_data()

                for box in box_word:
                    box_word = OcrBoxWord(
                        pdf_page_id=id_pdf_page,
                        size_height=box['height'],
                        size_width=box['width'],
                        position_top=box['top'],
                        position_left=box['left'],
                        text=box['text']
                    )

                    db.session.add(box_word)
                    db.session.commit()

        else:

            print('Le dossier est inconnu')
            raise Exception('The folder is not found')

    """
    Convert the file and scan this 
    """

    def Scan(self, folder_number, pdf_file_id):

        from app.models.DataBase import PdfFile, db

        try:
            pdf_file_db = PdfFile.query.filter_by(id=pdf_file_id).first()

            pdf_file_db.status = 1
            db.session.commit()

            number_jpg = self.convert_to_jpg(folder_number)

            self.ocr_jpg(folder_number, pdf_file_id, number_jpg)

            pdf_file_db.status = 2
            db.session.commit()

        except :
            pdf_file_db.status = -1
            db.session.commit()
