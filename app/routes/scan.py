import os
import sys

from flask import Blueprint, render_template, request, jsonify, url_for, send_file, redirect
from sqlalchemy import asc

from app.config import UPLOAD_DIR_PDF, UPLOAD_DIR_JPG, UPLOAD_DIR_TXT
from app.models.ScannerThread import ScannerThread
from app.models.UploadFile import UploadFileSystem

scan_app = Blueprint('scan_app', __name__, template_folder='../templates/scan', url_prefix='/scan')

threadScanner = ScannerThread()
threadScanner.start()

"""
    This is a simple redirect
"""


@scan_app.route('/', methods=['GET'])
@scan_app.route('/upload', methods=['GET'])
def show():
    return render_template('upload.html')


"""
    This page allow users to upload a file pdf for to be scan by ocr
"""

# instance of upload system
upload_sys = UploadFileSystem()


@scan_app.route('/upload', methods=['POST'])
def upload():
    try:
        # all file
        uploaded_files = request.files.getlist("fileUpload[]")

        for file in uploaded_files:
            print('file upload : ' + str(file))
            # check if file is upload with good extension
            upload_sys.is_pdf(file)

            # the id where the file is upload
            file_dest_name = upload_sys.save_file(file, UPLOAD_DIR_PDF)

            print(file_dest_name)

            from app.models.DataBase import PdfFile, db

            # save in dbb
            pdf = PdfFile(
                name=file.filename,
                path=file_dest_name
            )

            db.session.add(pdf)
            db.session.commit()

            print(file)

            threadScanner.append_file(file_dest_name, pdf.id)

        return jsonify(url=url_for('scan_app.files'))

    except Exception as error:
        print(error)
        return jsonify(error=error.__str__())


"""
    This page allow correction for user to 
"""


@scan_app.route('/selectionExtract/<int:folder_number>', methods=['GET', 'POST'])
def selection_extract(folder_number):
    # ckeck if the file exist

    from app.models.DataBase import PdfFile, OCRPage
    try:
        file = PdfFile.query.filter_by(path=folder_number).first()
        pages = OCRPage.query.filter_by(pdf_file_id=file.id).all()
        return render_template('selectionExtract.html', pages=pages, folder_number=folder_number)
    except:
        return 'Error selection_extract'


"""
    This page is for downlaod the document after correction
"""


@scan_app.route('/downlaod/<int:pdf_id>')
def download(pdf_id):
    from app.models.DataBase import OCRPage, PdfFile

    pdf_file = PdfFile.query.filter_by(id=pdf_id).first()
    filename = pdf_file.name

    file_path = os.path.join(UPLOAD_DIR_TXT, str(filename) + '.txt')

    pages = OCRPage.query.filter_by(pdf_file_id=str(pdf_id)).all()
    f = open(file_path, "wb")

    for page in pages:
        f.write(("---------------------------------------------------------" +
                 "\n \t\t\tNum : " + page.num_page + "\n" + "---------------------------------------------------------" +
                 "\n").encode(sys.stdout.encoding, errors='Error'))
        f.write((str(page.text) + '\n').encode(sys.stdout.encoding, errors='Error'))

    f.close()
    return send_file(file_path)


"""
    This page list all file in bdd
"""


@scan_app.route('/files', methods=['GET'])
def files():
    from app.models.DataBase import PdfFile
    files = PdfFile.query.order_by(asc(PdfFile.status)).order_by(asc(PdfFile.name)).all()
    return render_template('files.html', files=files)


@scan_app.route('/images/<int:folder_number>/<int:file_number>')
def get_images(folder_number, file_number):
    folder = os.path.join(UPLOAD_DIR_JPG, str(folder_number))
    filename = os.path.join(folder, str(file_number) + '.jpg')
    return send_file(filename, mimetype='image/jpg')


@scan_app.route('/page/<int:folder_number>/<int:file_number>')
def get_boxs(folder_number, file_number):
    from app.models.DataBase import OcrBoxWord, PdfFile, OCRPage

    # get all box of page
    file = PdfFile.query.filter_by(path=folder_number).first()

    page = OCRPage.query.filter_by(pdf_file_id=file.id, num_page=file_number).first()

    boxs = OcrBoxWord.query.filter_by(pdf_page_id=page.id).all()

    json_array = {'box': [e.serialize() for e in boxs],
                  'text': page.text}

    return jsonify(json_array)


@scan_app.route('/delete/<int:pdf_id>')
def delete_file(pdf_id):
    try:
        from app.models.DataBase import PdfFile, db
        PdfFile.query.filter_by(id=pdf_id).delete()
        # return jsonify({'succes': 'The file is deleted'})
        # print(url_for('scan_app.files'))
        return redirect(url_for('scan_app.files'))
    except Exception as error:
        return jsonify({'error': 'During delete ( ' + str(error) + ' )'})
