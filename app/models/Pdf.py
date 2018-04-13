import os

import PyPDF2
import pdf2image as pdf2image


def split_pdf_pages(input_pdf_path, target_dir, fname_fmt="{num_page}.pdf"):
    # default number page
    num_page = 0

    if not os.path.exists(target_dir):
        # create repository
        os.makedirs(target_dir)

    with open(input_pdf_path, "rb") as input_stream:

        # si ouverture du fichier Pdf a split
        input_pdf = PyPDF2.PdfFileReader(input_stream)

        # si page dans le fichier
        if input_pdf.flattenedPages is None:
            num_page = input_pdf.getNumPages()

        for num_page, page in enumerate(input_pdf.flattenedPages):
            # creation de la page de sortie
            output = PyPDF2.PdfFileWriter()
            # ajout de la page PyPDF2.Pdf.PageObject
            output.addPage(page)

            # le nom du fichier
            file_name = os.path.join(target_dir, fname_fmt.format(num_page=num_page))

            # ouverture du fihier cree
            with open(file_name, "wb") as output_stream:
                # ecriture dans le fichier
                output.write(output_stream)

    return num_page


def convert_to_jpg(input_pdf_file, target_dir, fname_fmt="{num_page}.jpg"):

    filename_output = os.path.splitext(input_pdf_file)[0]

    if not os.path.exists(target_dir):
        # creation du rep
        os.makedirs(target_dir)
    else:
        if os.path.exists(os.path.join(target_dir, filename_output)):
            raise Exception('Error the file exist already')

    images = pdf2image.convert_from_path(input_pdf_file)
    for index, image in enumerate(images):
        path_file = os.path.join(target_dir , fname_fmt.format(num_page=index))
        image.save(path_file)

    return len(images)


if __name__ == '__main__':
    print(convert_to_jpg('4.pdf', '', ))
