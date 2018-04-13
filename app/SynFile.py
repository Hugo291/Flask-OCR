import os
import shutil
from os import listdir

from app.models.DataBase import PdfFile

pdfs_db = PdfFile.query.all()

dir = os.path.join(os.getcwd(), 'upload')
pdf_dir = os.path.join(dir, 'pdf')
jpg_dir = os.path.join(dir, 'jpg')

if __name__ == '__main__':
    file_folder_path = [f.path for f in pdfs_db]
    file_pdfs_path = [f.path + '.pdf' for f in pdfs_db]
    files_pdf = [f for f in listdir(pdf_dir) if os.path.isfile(os.path.join(pdf_dir, f))]
    folder_jpg_list = [f for f in listdir(jpg_dir) if os.path.isdir(os.path.join(jpg_dir, f))]

    for file in files_pdf:
        # print('fiel : ',file ,'pdf : ', file in file_pdfs)
        if file not in file_pdfs_path:
            path_file_pdf = os.path.join(pdf_dir, file)
            folder_number = os.path.splitext(os.path.basename(path_file_pdf))[0]
            folder_jpg_element = os.path.join(jpg_dir, folder_number)

            try:
                print(folder_number, listdir(os.path.join(jpg_dir, folder_number)))
                shutil.rmtree(folder_jpg_element)

            except Exception as E:
                pass
            finally:
                os.remove(path_file_pdf)

            # print(folder_jpg, path_file_pdf)
            # os.remove(path_file_pdf)
        else:
            pass
            # print('in : ',file)
    print('end')
