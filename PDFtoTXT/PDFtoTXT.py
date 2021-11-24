from genericpath import isdir
import os
import glob
import shutil
import pdfplumber
from PyPDF2 import PdfFileWriter, PdfFileReader

files_path = input('Cole aqui o caminho do diretório dos arquivos:\n')

## PASTA ARQUIVOS
newdir = files_path+'\Arquivos\\'
if isdir(newdir)==True:
    shutil.rmtree(newdir)
    os.mkdir(newdir)
else:
    os.mkdir(newdir)
## GLOB DOS PDFS
files = glob.glob(files_path+'\\'+'*.pdf')
for file in files:
    pdf = pdfplumber.open(file)
    page = pdf.pages[0]
    text = page.extract_text()
    path = os.path.split(file)
    newdir = path[0]+'\Arquivos\\'
    filename = os.path.splitext(path[1])
    filename = newdir+filename[0]+'.txt'
    # print(text)
    if text is None:
        print('Imagem encontrada!')
        pdf.close()
        imgdir = path[0]+'\Imagens\\'
        if isdir(imgdir)==False:
            os.mkdir(imgdir)
        shutil.move(file,imgdir)
    else:
        print('Ok || '+file)
        txt = open(filename,'w')
        txt.write(text)
        txt.close()
        pdf.close()

os.system('pause')