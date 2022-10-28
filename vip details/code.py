
from PyPDF2 import PdfFileMerger
import os
import ocrmypdf
import tabula
import pandas as pd
import logging
import subprocess
import sys
import time


#Extract
def extractToExcel():
    file_ToRead = '../result.pdf'
    dfs = tabula.read_pdf(file_ToRead,pages='all',area=((134.258,152.618,157.208,249.773),(216.113,53.933,236.768,92.948),
    (216.878,121.253,236.768,161.798), (436.433,56.228,499.163,569.543)))

    #converting list data frame to dataframe
    df = pd.concat(dfs)

        #converting the data drom to csv
    df.to_csv('../final.csv', index=False)
    print(df)

#merger
def merger_PDFs():
    folder = os.getcwd()+'/'
    pdfs = [folder + fn for fn in os.listdir(folder) if fn.endswith('.pdf')]

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write("../result.pdf")
    merger.close()

    extractToExcel()

#convert scanned pdf to standard pdf
def Convert():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(script_dir + '/ocr-tree.py: Start')

    if len(sys.argv) > 1:
     start_dir = sys.argv[1]
    else:
        start_dir = '.'
    if len(sys.argv) > 2:
        log_file = sys.argv[2]
    else:
        log_file = script_dir + '/ocr-tree.log'
    logging.basicConfig(
                level=logging.INFO, format='%(asctime)s %(message)s',
                filename=log_file, filemode='w')

    for dir_name, subdirs, file_list in os.walk(start_dir):
        logging.info('\n')
        logging.info(dir_name + '\n')
        os.chdir(dir_name)
        for filename in file_list:
            file_ext = os.path.splitext(filename)[1]
            if file_ext == '.pdf':
                full_path = dir_name + '/' + filename
                print(full_path)
                cmd = ["ocrmypdf","--force-ocr" , "--deskew", filename, filename]
                logging.info(cmd)
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result = proc.stdout.read()
                if proc.returncode == 6:
                    print("Skipped document because it already contained text")
                elif proc.returncode == 0:
                    print("OCR complete")
                logging.info(result)
                
                merger_PDFs()

Convert()











