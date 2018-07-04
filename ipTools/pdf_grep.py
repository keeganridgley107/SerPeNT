# importing required modules

import os
import PyPDF2

########################
# TODO: input dir, open all pdfs in dir, search for text, copy results to report_file
########################

# creating a pdf file object
pdfFileObj = open('example.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(0)

# extracting text from page
print(pageObj.extractText())

# closing the pdf file object
pdfFileObj.close()


def get_pdf_dir():
    """get path to dir containing pdfs"""
    dir_path = input("[?] Enter the path of the folder to grep: ")
    # check if dir exists
    print(os.path.isdir(dir_path))
    # check if the dir has any pdf files in it
    print(os.path.exists(dir_path + "/*.pdf"))
    # exit DEBUG
    return dir_path


def pdf_search_loop(pdf_dir):
    print(pdf_dir)
    results = pdf_dir
    return results


def write_to_report(results):
    print(results)
    pass


def main():
    print("starting pdf_grep...")
    pdf_dir = get_pdf_dir()
    results = pdf_search_loop(pdf_dir)
    write_to_report(results)


if __name__ == '__main__':
    main()
