import os
import shutil
import zipfile
from datetime import datetime

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])

def zip_usinas():
    path_download = "./download"
    usinas_dir = os.listdir(path_download)

    path_zip = "./zip"
    os.makedirs(path_zip, exist_ok=True)

    date_name = datetime.today().strftime('%Y%m%d')
    for usina in usinas_dir:
        zip_directory(f'{path_download}/{usina}', f'{path_zip}/{usina} - e{date_name}.zip')

def delete_folders():
    folders = ['download', 'zip', 'excel']

    for folder in folders:
        shutil.rmtree(f'./{folder}', ignore_errors=True)

if __name__ == '__main__':
    print("Execute o arquivo main.py")