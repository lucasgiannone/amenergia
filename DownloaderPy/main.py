import logging
import os
from queue import Queue
from threading import Thread
from time import time
from download import get_bills, download_link
import re


logging.basicConfig(filename='download.log', filemode='w', level=logging.CRITICAL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            bill = self.queue.get()
            try:
                if bill['Tensao'] == 'mt':
                    bill['Tensao'] = 'Media'
                elif bill['Tensao'] == 'bt':
                    bill['Tensao'] = 'Baixa'
                link = "https://storage.googleapis.com/faturas-amenergia/{Tensao}/1704/{Cod_UC}/{Nome_Upload}".format(
                    Tensao=bill['Tensao'],Cod_UC=bill['Cod_UC'], Nome_Upload=bill['Nome_Upload'])
                # print(str(bill["UC"]))
                print(link)
                path = "./download/"
                os.makedirs(path, exist_ok=True)
                mesRef = bill['Mes_Ref']
                mesRef = mesRef.strftime("%y_%m")
                numFatura = str(bill['Nome_Upload'])
                numFatura = numFatura.split('_')
                numFatura = re.sub(r"[0-9]", "", str(numFatura[2]))
                Unidade = str(bill['UC']).strip()
                filename = "{UC} {Mes_Ref}{EXT}".format(UC=(Unidade),Mes_Ref=str(mesRef),EXT=(numFatura))
                # print(numFatura)
                download_link(path, filename, link)

                logger.critical('Queue Complete {} {}'.format(Unidade,link))
            except Exception as e:
                print(e)
                logger.critical('Queue Failed {}'.format(Unidade,link))

            finally:
                self.queue.task_done()


def main():
    ts = time()
    queue = Queue()

    bills = get_bills()

    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()

    for bill in bills:
        queue.put(bill)

    queue.join()
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()
