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


def pdf_search_loop(dir_path):
    """LOOP over files in dir, open pdfs and copy text to results array"""
    # init the results array
    results = [{"PDF_GREP RESULTS ": dir_path}]
    # print the start msg and dir path
    print("[+] Starting: PDF grep loop on: %s" % dir_path)
    # grab a list of the files in dir_path
    dir_files = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]

    for file in dir_files:
        # open file
        if file.split(".")[1] == "pdf":
            print("[+] PDF Found...")
            pdfFileObj = open(dir_path + file, 'rb')

            # creating a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            # printing number of pages in pdf file
            print(pdfReader.numPages)
            # check if multi page and loop through pages if True
            if pdfReader.numPages > 0:
                print("[+] Multi=page PDF found.")
                for page in pdfReader.numPages:
                    multi_page_obj = pdfReader.getPage(int(page))
                    print("[+] Page data: ", multi_page_obj.extractText())
                    # TODO: GREP data and WRITE to results.txt
                    results.append({"PDF_GREP: " + file + " page: %d" % int(page): multi_page_obj.extractText()})
            # Single page pdf, proceed without looping through pages
            pageObj = pdfReader.getPage(0)
            print(pageObj.extractText())
            # TODO: GREP data and WRITE to results.txt

            results.append({"PDF_GREP: " + file: pageObj.extractText()})

            # closing the pdf file object
            pdfFileObj.close()
        else:
            # file is not a pdf, move along now...
            pass

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
