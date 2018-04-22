import os
import sys

from flask import Blueprint, render_template, request, jsonify, url_for, send_file, redirect
from sqlalchemy import asc

from app.config import UPLOAD_DIR_PDF, UPLOAD_DIR_JPG, UPLOAD_DIR_TXT
from app.models.ScannerThread import ScannerThread

scan_app = Blueprint('scan_app', __name__, template_folder='../templates/scan', url_prefix='/scan')

threadScan = ScannerThread()
threadScan.start()


def add_file(file):
    threadScan.append_file(file)


@scan_app.route('/', methods=['GET'])
@scan_app.route('/upload', methods=['GET'])
def show():
    from app.models.Form import ScanDocumentForm
    form = ScanDocumentForm()
    return render_template('upload.html', form=form)


"""
    This page allow users to upload a pdf file for to be scan by ocr
"""


@scan_app.route('/upload', methods=['POST'])
def upload():
    from app.models.Form import ScanDocumentForm

    form = ScanDocumentForm()

    if form.validate_on_submit():

        # save in dbb
        from app.models.DataBase import PdfFile, db

        file = form.filePdf.data

        pdf = PdfFile(name=file.filename)

        db.session.add(pdf)
        db.session.commit()

        file.save(os.path.join(UPLOAD_DIR_PDF, str(pdf.id) + '.pdf'))

        add_file(pdf.id)

        return redirect(url_for('scan_app.files'))
    else:
        return str(form.errors)


"""
    This page allow correction for user to 
"""


@scan_app.route('/selectionExtract/<int:pdf_id>', methods=['GET', 'POST'])
def selection_extract(pdf_id):
    # ckeck if the file exist

    from app.models.DataBase import OCRPage
    try:
        pages = OCRPage.query.filter_by(pdf_file_id=pdf_id).all()
        return render_template('selectionExtract.html', pages=pages, pdf_id=pdf_id)
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


@scan_app.route('/images/<int:pdf_id>/<int:page_number>')
def get_images(pdf_id, page_number):
    folder = os.path.join(UPLOAD_DIR_JPG, str(pdf_id))
    filename = os.path.join(folder, str(page_number) + '.jpg')
    return send_file(filename, mimetype='image/jpg')


@scan_app.route('/page/<int:pdf_id>/<int:page_number>')
def get_boxs(pdf_id, page_number):
    from app.models.DataBase import OcrBoxWord, OCRPage

    # get all box of page

    page = OCRPage.query.filter_by(pdf_file_id=pdf_id, num_page=page_number).first()

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


"""
    correction file
    GET [text]
"""


@scan_app.route('/correct')
def correction():
    return "text : " + request.data
