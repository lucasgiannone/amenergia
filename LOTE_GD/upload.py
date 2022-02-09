from dotenv import load_dotenv
import logging
import os
from datetime import datetime, timedelta
from google.cloud import storage
import csv

import pytz
utc = pytz.UTC

load_dotenv()

logger = logging.getLogger('LOTE_GD')


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


def move_files_expired():
    bucket_name = "faturas-amenergia"
    path_storage = "relatorios/"
    new_path_storage = "relatorios_historico_amee/"

    logger.info(f'Move Expired Files')

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = client.list_blobs(bucket_name, prefix=path_storage)

        date_now = datetime.today().replace(tzinfo=utc)

        for blob in blobs:
            if(blob.name == f"{path_storage}"):
                continue
            
            date_limit = blob.updated + timedelta(days=180)

            if(date_limit < date_now):
                try:
                    print(blob.name)
                    print(blob.updated)
                    print("")
                    bucket.rename_blob(blob, new_name=blob.name.replace(
                        path_storage, new_path_storage))
                    logger.info(f'Movido {blob.name}')
                except Exception as e:
                    print(e)
                    logger.error(f'Error on Move: {blob.name}')

    except Exception as e:
        print(e)
        logger.error(f'Error on Move Expired Files')

    finally:
        logger.info(f'Move Expired Files Finished')

def reactivate_link():
    bucket_name = "faturas-amenergia"

    ##REATIVAR
    # path_storage = "relatorios_historico_amee/"
    # new_path_storage = "relatorios/"

    ##DESATIVAR
    path_storage = "relatorios/"
    new_path_storage = "relatorios_historico_amee/"

    logger.info(f'Move Expired Files')

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = client.list_blobs(bucket_name, prefix=path_storage)
        links = []
        file = open('links.csv')
        csvreader = csv.reader(file)
        for blob in blobs:
            print(blob)
            try:
                for row in csvreader:
                    search = str(row)[2:-2]
                    links.append(search)
                for link in links:
                    if str(blob.name).find(link) != -1:
                        newname = blob.name.replace(
                            path_storage, new_path_storage)
                        print("Encontrando em:")
                        print("     " + blob.name)
                        print("Movido para:")
                        print("     " + newname)
                        print("")
                        # bucket.rename_blob(blob, newname)
            except Exception as e:
                print(e)
                logger.error(f'Error on Move: {blob.name}')
    except Exception as e:
        print(e)
        logger.error(f'Error on Move Expired Files')

    finally:
        logger.info(f'Move Expired Files Finished')


if __name__ == '__main__':
    ## MOVER ARQUIVOS EXPIRADOS
    # move_files_expired()
    ## RESTAURAR ARQUIVOS EXPIRADOS
    reactivate_link()
