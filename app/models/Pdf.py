import os

import pdf2image as pdf2image


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
