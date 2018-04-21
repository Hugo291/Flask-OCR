import os
import time
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
        self.__list_file = []
        self.__percent = 0
        self.cal = lambda current, total: int(current * 100 / total)

    """ 
    Loop infinit and if detect a file in list , the 
    """

    def run(self):
        super().run()
        while True:
            time.sleep(10)
            while self.has_pending_file():
                try:
                    self.set_percent(0)

                    self.convert_scan_file()

                    self.delete_last_file_scaned()

                    self.set_percent(0)
                except Exception as error:

                    print("Erreur (run): " + str(error))
                    print(error)

    """
    Return True if a file is in list 
    """

    def has_pending_file(self):
        if len(self.__list_file) != 0:
            return True
        return False

    """
    Return the first file to be scan
    """

    def get_last_file_scaned(self):
        return self.__list_file[0]

    """
    Delete the last file to be scan 
    """

    def delete_last_file_scaned(self):
        del self.__list_file[0]

    """
    Add a file in list to be scan
    """

    def append_file(self, pdf_file_id):
        self.__list_file.append(pdf_file_id)

    """
    convert file in jpg
    """

    def convert_pdf_to_jpg(self, file_number):

        if os.path.isfile(os.path.join(UPLOAD_DIR_PDF, str(file_number) + ".pdf")):

            file_path = os.path.join(UPLOAD_DIR_PDF, str(file_number) + ".pdf")
            dir_dest = os.path.join(UPLOAD_DIR_JPG, str(file_number))

            number_page = convert_to_jpg(file_path, dir_dest)

            return number_page
        else:
            print("The file is not supported by the system")
            raise Exception('The file is not supported by the system')

    """
    Analyse the file 
    """

    def ocr_jpg(self, number_file):

        from app.models.DataBase import OCRPage, db, OcrBoxWord

        # ckeck if the fodler exist
        if os.path.isdir(os.path.join(UPLOAD_DIR_JPG, str(self.get_last_file_scaned()))):

            # folder with all jpg
            folder = os.path.join(UPLOAD_DIR_JPG, str(self.get_last_file_scaned()))

            # for all file

            for index in range(number_file):

                image_ocr = OCRPage(
                    pdf_file_id=self.get_last_file_scaned(),
                    num_page=index
                )

                path_file_img = os.path.join(folder, '{}.jpg'.format(str(index)))

                scanner_ocr = OCR(path_file_img)
                image_ocr.text = scanner_ocr.scan_text()

                db.session.add(image_ocr)
                db.session.commit()

                id_pdf_page = image_ocr.id

                box_word = scanner_ocr.scan_data()

                for box in box_word:
                    box_word = OcrBoxWord(
                        pdf_page_id=id_pdf_page,
                        box=box
                    )

                    db.session.add(box_word)

                db.session.commit()

                self.set_percent(self.cal(current=index, total=number_file))

        else:

            print('The folder is not found')
            raise Exception('The folder is not found')

    """
    Convert the file and scan this 
    """

    # def convert_scan_file(self, folder_number, pdf_file_id):
    def convert_scan_file(self):

        from app.models.DataBase import PdfFile, db

        # pdf file bd
        pdf_file_db = PdfFile.query.filter_by(
            id=self.get_last_file_scaned()
        ).first()

        try:
            # set status In progress
            pdf_file_db.status = 1
            db.session.commit()

            # convert to jpg
            number_jpg = self.convert_pdf_to_jpg(self.get_last_file_scaned())

            # ocr the image
            self.ocr_jpg(number_jpg)

            # set staus finish
            pdf_file_db.status = 2
            db.session.commit()

        except Exception as exception:
            print(exception)
            print("Erreur (convert_scan_file): " + str(exception))
            pdf_file_db.status = -1
            db.session.commit()

    """
    Get the percent
    """

    def get_percent(self):
        return self.__percent

    def set_percent(self, percent):
        self.__percent = percent
