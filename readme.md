Getting things ready
    make sure you have python3, java and an IDE installed as well as a python package installer such as pip
    open the pdfToExcel folder in terminal and install the following python modules 
    1.pyPDF2 - pip install PyPDF2
    2.tabula py - pip install tabula-py
    3.ocrmypdf - this one you can check installation command on their site since am not sure what os you are using, the command is simple though.
    THATS IT!

HOW TO USE THE CODE
For the first pdf navigate to first pdf/pdfs folder and paste the PDFs you intend to parse on the pdfs folder

open the code.py script and run it
the code will first convert the scanned pdfs to standard pdfs using OCR-Optical Character Recognition
then the standard pdfs will be merged to a single pdf and stored in the pdfToExel/root folder in result.pdf file
Lastly the code will extract data from result.pdf and save it on the root folder as final.csv which can be opened as an excel file. 

the instructions for running vip details code are the same as for the first pdf just make sure you are in the vip details folder
and paste the pdfs in the pdf folder

NOTE:
1.Make sure to delete/move to another folder the pasted pdfs, result.pdf and final.csv before running or iterating another batch of pdfs.
2.Ensure the structure/format of data on all the scanned pdfs is similar since the code reads data from specific points of the pdfs.



