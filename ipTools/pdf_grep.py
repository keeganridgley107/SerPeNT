# importing required modules

import os
from os.path import isfile, join
import PyPDF2

########################
# TODO: input dir, open all pdfs in dir, search for text, copy results to report_file
########################

def get_pdf_dir():
    """get path to dir containing pdfs"""
    dir_path = input("[?] Enter the path of the folder to grep: ")
    try:
        # check if dir exists
        dir_check = os.path.isdir(dir_path)
        # check if the dir has any pdf files in it
        pdf_check = os.path.exists(dir_path + "/*.pdf")
        print(dir_check, pdf_check, " CHECK dem VALS")
        dir_files = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]
        print("[+] Folder has %d files" % len(dir_files))
    except Exception as e:
        # exit DEBUG
        print("[-] Error: Input: %s" % dir_path)
        print("[-] Exception: ", e)
        exit(0)
    return dir_path


def pdf_search_loop(pdf_dir):
    """LOOP over files in dir, open pdfs and copy text to results array"""

    # TESTING DEBUG
    print(pdf_dir)
    results = pdf_dir
    # TESTING DEBUG
    ####################################################
    # TODO: add a loop over the files in pdf_dir
    ##########################pdf########################
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

    ##########################################################
    # TODO: add a grep function here
    ##########################################################

    # closing the pdf file object
    pdfFileObj.close()

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
