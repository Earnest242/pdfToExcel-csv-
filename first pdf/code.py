
from PyPDF2 import PdfFileMerger
import os
import ocrmypdf
import tabula
import pandas as pd
import logging
import subprocess
import sys
import time

#Function to extract data and save to a csv file called final.csv
def extractToExcel():
    file_ToRead = '../result.pdf'
    dfs = tabula.read_pdf(file_ToRead, guess=False,stream=True, pages='all',columns=(263.835, 310.365 ,402.435,517.275, 610.335,
    667.755, 716.265))
    #converting list data frame to dataframe
    df = pd.concat(dfs)

    #dropping the empty columns
    df.drop(df.columns[[0,2]], axis = 1, inplace = True)
    df.drop([0,1,2,3], axis=0, inplace=True)
    #naming the columns
    df.columns=['HQ ITEM','DESCRIPTION','DEAL SHEET PERFORMANCE PERIOD','BILLBACK AMOUNT','MOVEMENT QUANTITY','TOTAL BILLBACK',]
    #df.dropna(axis=1, how="all", inplace=False)

        #converting the data drom to csv
    df.to_csv('../final.csv', index=False)
    print(df)

#function to combine multiple PDFs to a single pdf for easier of extraction
def  merge_PDFs():
    folder = os.getcwd()+'/'
    pdfs = [folder + fn for fn in os.listdir(folder) if fn.endswith('.pdf')]

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)
    
    merger.write("../result.pdf")
    merger.close()

    #calling extract function
    extractToExcel()


    
#function to convert scanned PDFs to standard pdfs using ocr(Optical character Recognition)
def ConvertPDFs():
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
                cmd = ["ocrmypdf",  "--deskew", filename, filename]
                logging.info(cmd)
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result = proc.stdout.read()
                if proc.returncode == 6:
                    print("Skipped document because it already contained text")
                elif proc.returncode == 0:
                    print("OCR complete")
                logging.info(result)
                
                #calling merging function
                merge_PDFs()

#calling the convert function
ConvertPDFs()


