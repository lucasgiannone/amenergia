import os
import glob
from shutil import copy
from datetime import datetime

## CAMINHOS DE PASTAS
xls_dir = r"PATH"
zip_dir = r"PATH"
lnk_dir = r"PATH"

## INPUT
# concessname = input("NOME DA CONCESSIONARIA:\n")
# period = input("PERIODO BAIXADO: \n")

## DATA ATUAL
today = datetime.today().strftime('%Y%m%d')

## RENOMEIA OS ARQUIVOS
zip_files = glob.glob(zip_dir+'*.zip')
for zip_file in zip_files:
    size = os.path.getsize(zip_file)
    if size < 1000:
        os.remove(zip_file)
    else:
        name = os.path.split(zip_file)
        name = name[0] + r'\fatsolicit_solicitacao_diversos_e'+ today + '.zip'
        # print(name)
        os.rename(zip_file,name)
        copy(name,lnk_dir)

xls_files = glob.glob(xls_dir+'*.xlsx')
for xls_file in xls_files:
        name = os.path.split(xls_file)
        name = name[0] +'\\Diversos - agua - e' + today + '.xlsx'
        # print(name)
        os.rename(xls_file,name)
        copy(name,lnk_dir)
