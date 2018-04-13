import datetime
import os
import random



"""
      Create the file with time and random value
  """

def create_file_name():
    return str(datetime.datetime.today().strftime('%Y%m%d')) + str(random.randint(0, 1000))

FILE_UPLOAD_NAME = 'fileUpload[]'

"""
    Module manage upload file 
"""

"""
    Check if file exist
"""
def file_exist(files):
    if FILE_UPLOAD_NAME not in files or files[FILE_UPLOAD_NAME] == '':
        raise Exception('Please select a file')

    return files[FILE_UPLOAD_NAME]


class UploadFileSystem():

    """
    Constructor
    """
    def __init__(self):
        pass

    """
    Check if the file is a pdf
    """
    def is_pdf(self, file):

        if str(file.mimetype).lower() == "application/pdf".lower():
            return
        else:
            """this extension is not supported"""
            raise Exception('This extension  (' + file.mimetype + ') is not supported')



    """
    Save the file with dest
    """
    def save_file(self, file, dest):

        numRandom = create_file_name()

        # create the file name
        filename = numRandom + '.pdf'

        new_file_pdf_path = os.path.join(dest, filename)

        try:
            # save the file
            file.save(new_file_pdf_path)

            return numRandom

        except Exception as E:

            raise Exception('Writing error' + str(E) + new_file_pdf_path)

