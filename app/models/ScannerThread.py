import os
import time
from threading import Thread

from app.config import UPLOAD_DIR_PDF, UPLOAD_DIR_JPG
from app.models.OCR import OCR
from app.models.Pdf import convert_to_jpg, page_number


class ScannerThread(Thread):
    """
    Construct
    """

    def __init__(self):
        super().__init__()
        print("init ")
        self.__list_file = []
        self.__percent = 0
        self.cal = lambda current, total: int(current * 100 / total)

    """ 
    Loop infinit and if detect a file in list , the 
    """

    def run(self):
        super().run()
        print("Thread Run")
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

    def get_last_file_scaned(self):
        """
        :return: the last or current file which has been scanned
        """
        return self.__list_file[0]

    def delete_last_file_scaned(self):
        """Thread init
            Delete the last file to be scan
        """
        del self.__list_file[0]

    def append_file(self, pdf_file_id):
        """
        Add the file to the list of files that will be scanned
        :param pdf_file_id: the pdf id
        """
        print("Add file : " + str(pdf_file_id))
        self.__list_file.append(pdf_file_id)

    def convert_pdf_to_jpg(self, pdf_page_number):
        """

        :param pdf_page_number: number page of pdf
        :return: the page number of the file
        """
        if os.path.isfile(os.path.join(UPLOAD_DIR_PDF, str(self.get_last_file_scaned()) + ".pdf")):

            file_path = os.path.join(UPLOAD_DIR_PDF, str(self.get_last_file_scaned()) + ".pdf")
            dir_dest = os.path.join(UPLOAD_DIR_JPG, str(self.get_last_file_scaned()))

            for index in range(pdf_page_number):
                print("Convertion of image (" + str(index) + ")")
                convert_to_jpg(file_path, dir_dest, num_page=index)
                self.set_percent(int(self.cal(current=index, total=pdf_page_number)/2))


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

                print("Scan file : "+str(index))

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

                # commit all word box in folder
                db.session.commit()

                self.set_percent(int(self.cal(current=index, total=number_file)/2+50))

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

            # the page  number pdf
            file_path = os.path.join(UPLOAD_DIR_PDF, str(self.get_last_file_scaned()) + ".pdf")
            pdf_page_number = page_number(file_path)

            print("pdf page number : " + str(pdf_page_number))

            # convert to jpg
            self.convert_pdf_to_jpg(pdf_page_number)

            # ocr the image
            self.ocr_jpg(pdf_page_number)

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

    def __str__(self):
        return str(self.get_percent())

    def get_percent(self):
        return self.__percent

    def set_percent(self, percent):
        print(str(percent) + "%")
        self.__percent = percent
