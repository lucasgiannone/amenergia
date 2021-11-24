import os
from datetime import datetime
from google.cloud import storage

from dotenv import load_dotenv
load_dotenv()

def upload_file(bucket_name, path_storage, file):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        filename = os.path.basename(file)

        blob = bucket.blob(f'{path_storage}/{filename}')
        blob.upload_from_filename(file)

        return blob.public_url

    except Exception as e:
        print(e)

        return False

def upload_to_storage(Usinas):
    bucket = "faturas-amenergia"
    path_storage = "relatorios"

    date_name = datetime.today().strftime('%Y%m%d')

    Usinas_Links = {}

    for Usina in Usinas:
        excel_file = f'./excel/{Usina} - e{date_name}.xlsx'
        zip_file = f'./zip/{Usina} - e{date_name}.zip'

        if(os.path.isfile(excel_file) and os.path.isfile(zip_file)):
            upload_excel = upload_file(bucket, path_storage, excel_file)
            upload_zip = upload_file(bucket, path_storage, zip_file)

            if(upload_excel and upload_zip):
                Usinas_Links[Usina] = {
                    "zip": upload_zip,
                    "excel": upload_excel
                }

    return Usinas_Links

if __name__ == '__main__':
    print("Execute o arquivo main.py")