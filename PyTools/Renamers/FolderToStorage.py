import os
import glob
from shutil import copy
from datetime import datetime

# CAMINHOS DE PASTAS
zip_dir = r"PATH"
# INPUT
concessname = input("CONCESSIONARIA:\n")
# DATA ATUAL
now = datetime.now()

today = now.strftime("%Y%m%d-%H%M")
print(today)

# RENOMEIA OS ARQUIVOS
zip_files = glob.glob(zip_dir+'*.zip')
for zip_file in zip_files:
    size = os.path.getsize(zip_file)
    if size < 1000:
        os.remove(zip_file)
    else:
        name = os.path.split(zip_file)
        name = name[0] + '\\' + concessname.upper() + '_L259_e' + \
            today + '.zip'
        print(name)
        os.rename(zip_file,name)
        # copy(name,lnk_dir)
