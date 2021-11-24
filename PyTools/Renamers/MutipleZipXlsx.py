import os
import glob
from shutil import copy
from datetime import datetime
import subprocess

## CAMINHOS DE PASTAS
xls_dir = r"PATH"
zip_dir = r"PATH"
lnk_dir = r"PATH"

## DATA ATUAL
today = datetime.today().strftime('%Y%m%d')

## EXECUTA 7ZIP EM PASTAS
subprocess.call([r"PATH"])

## RENOMEIA OS ARQUIVOS
zip_files = glob.glob(zip_dir+'*.zip')
for zip_file in zip_files:
    size = os.path.getsize(zip_file)
    if size < 1000:
        os.remove(zip_file)
    else:
        name = os.path.splitext(zip_file)
        name = name[0] + ' - e' + today + name[1]
        os.rename(zip_file,name)
        copy(name,lnk_dir)

xls_files = glob.glob(xls_dir+'*.xlsx')
for xls_file in xls_files:
    name = os.path.splitext(xls_file)
    name = name[0] + ' - e' + today + name[1]
    os.rename(xls_file,name)
    copy(name,lnk_dir)






# link = lname + ' - e' + today + '.zip'
# zip = zname + ' - e' + today + '.zip'