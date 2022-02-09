import os
import glob
from datetime import datetime 
import shutil

## PASTAS
src_xlsx = ".\excel\\"
src_zips = ".\zip\\"
today = datetime.today()
year = today.strftime("%Y")
monthday = today.strftime("%d-%m")
back_dir = "F:\\LOTE_GD\\backup\\"+year+'\\'+monthday
today = today.strftime('%Y%m%d')
## CONST
def backuplocal():
    os.makedirs(back_dir, exist_ok=True)
    for file in glob.glob(src_xlsx+'*.xlsx'):
        print(file)
        # name = os.path.splitext(file)
        # name = name[0] + name[1]
        # os.rename(file,name)
        shutil.copy(file,back_dir)
    for file in glob.glob(src_zips+'*.zip'):
        print(file)
        # name = os.path.splitext(file)
        # name = name[0] + name[1]
        # os.rename(file,name)
        shutil.copy(file,back_dir)
    shutil.copy('.\lote_gd.log',back_dir)

if __name__ == '__main__':
    backuplocal()