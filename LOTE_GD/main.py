from threading import Thread
from queue import Queue
from time import time
import logging
import os
from datetime import datetime
from soupsieve import match
from database import get_bills, download_link, send_to_database
from excel import write_bills_xlsx, clean_usina_name
from zip import delete_folders, zip_usinas
from upload import upload_to_storage, move_files_expired
from backup import backuplocal

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename='lote_gd.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('LOTE_GD')

BillsResult = []


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            bill = self.queue.get()
            try:
                Cod_Empresa = bill['Cod_Empresa']
                Cod_UC = bill['Cod_UC']
                Nome_Upload = bill['Nome_Upload']
                Usina = bill["Usina"]
                Mes_Ref = bill["Mes_Ref"]
                Uc = bill["UC"]
                Tensao = bill["Tensao"]
                if Tensao == 'mt':
                    Tensao = 'Media'
                elif Tensao == 'bt':
                    Tensao = 'Baixa'

                # LINK
                link = f'https://storage.googleapis.com/faturas-amenergia/{Tensao}/{Cod_Empresa}/{Cod_UC}/{Nome_Upload}'

                # CREATE FOLDER
                Usina = clean_usina_name(Usina)
                path = f'./download/{Usina}/'
                os.makedirs(path, exist_ok=True)

                # FILENAME
                Mes_Ref_Format = Mes_Ref.strftime("%y_%m")
                filename = f'{Uc} {Mes_Ref_Format}.pdf'

                # DOWNLOAD
                download_link(path, link, filename)

                # ADD TO BILL ARRAY
                BillsResult.append(bill)

                logger.info(f'Download Completo {link}')

            except Exception as e:
                print(e)
                logger.error(f'Download Falhou {link}')

            finally:
                self.queue.task_done()


def main():
    ts = time()
    queue = Queue()

    move_files_expired()

    delete_folders()
    logger.info(f'Folders Deleted')

    bills_data = {
        'Cod_Empresa': 1704,
        'Mes_Ref': '2021-07-01'
    }

    bills = get_bills(bills_data)
    logger.info(f'Bills Fetched from Mysql')

    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()

    for bill in bills:
        if bill['Usina'] == 'LYON IV':
            if bill['Mes_Ref'] >= (datetime.strptime('2022-01-01', "%Y-%m-%d").date()):
                print(bill['Usina'],bill['Mes_Ref'])
                queue.put(bill)
        elif bill['Usina'] == 'LYON V':
            if bill['Mes_Ref'] >= (datetime.strptime('2022-01-01', "%Y-%m-%d").date()):
                print(bill['Usina'],bill['Mes_Ref'])
                queue.put(bill)
        elif bill['Usina'] == 'LIBERA MARIA':
            if bill['Mes_Ref'] >= (datetime.strptime('2022-01-01', "%Y-%m-%d").date()):
                print(bill['Usina'],bill['Mes_Ref'])
                queue.put(bill)
        else:
            print(bill['Usina'],bill['Mes_Ref'])
            queue.put(bill)


    queue.join()
    logger.info(f'Download Finished')

    Usinas_Bills = write_bills_xlsx(BillsResult)
    logger.info(f'XLSX Generated')

    zip_usinas()
    logger.info(f'ZIP Generated')

    Usinas_Links = upload_to_storage(Usinas_Bills)
    logger.info(f'Upload Finished')

    backuplocal()
    logger.info(f'Backup Finished')

    send_to_database(Usinas_Links, Usinas_Bills)
    logger.info(f'Update on Database Finished')

    logging.info('Tempo de execucao: %s', time() - ts)


if __name__ == '__main__':
    main()
