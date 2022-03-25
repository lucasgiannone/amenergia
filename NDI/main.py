import logging
import os
from queue import Queue
from threading import Thread
from time import time
from download import get_bills, download_link
import re


logging.basicConfig(filename='download.log', filemode='w', level=logging.INFO,
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
                    Tensao=bill['Tensao'], Cod_UC=bill['Cod_UC'], Nome_Upload=bill['Nome_Upload'])
                # print(str(bill["UC"]))
                path = "./download/"
                
                mesRef1 = bill['Mes_Ref']
                mesRef2 = mesRef1.strftime("%y_%m")
                mesRef3 = mesRef1.strftime("%d/%m/%Y")
                numFatura = str(bill['Nome_Upload'])
                numFatura = numFatura.split('_')
                numFatura = re.sub(r"[0-9]", "", str(numFatura[2]))
                Unidade = str(bill['UC']).strip()
                # path = path + '{Mes_Ref}/'.format(Mes_Ref=str(str(mesRef1)))
                path = path + '{Concess}/'.format(Concess=str(bill['Sigla']))
                ## FORMATO NOME 1 || /UC.pdf
                # filename = "{UC}.pdf".format(
                #     UC=(Unidade), EXT=(numFatura))
                ## FORMATO NOME 2 || /Mes/ UC Mes ABC.pdf
                filename = "{UC} {Mes_Ref}{EXT}".format(
                UC=(Unidade), Mes_Ref=str(mesRef2), EXT=(numFatura))
                ##mkdir
                os.makedirs(path, exist_ok=True)
                print(filename)
                # return

                DataEnvio = str(bill['Data_Envio'])
                CodLink = str(bill['Cod_Link'])
                NomeUpload = str(bill["Nome_Upload"])
                NomeConcess = str(bill["Sigla"])

            # JÁ ENVIADO
                if bill["Arquivo_Envio"] == 1:
                    print(Unidade)
                    print("Já enviado " + str(bill["Arquivo_Envio"]))
                    print(link)
                    logger.info('	Enviado	{}	{}	{}	{}	{}	{}	{}'.format(
                        Unidade, NomeConcess, mesRef3, CodLink, DataEnvio, NomeUpload, link))
                    # download_link(path, filename, link)
            # NÃO ENVIAR
                elif bill["Arquivo_Envio"] == 2:
                    print(Unidade)
                    print("N enviar " + str(bill["Arquivo_Envio"]))
                    print(link)
                    logger.info('	N enviar	{}	{}	{}	{}	{}	{}	{}'.format(
                        Unidade, NomeConcess, mesRef3, CodLink, DataEnvio, NomeUpload, link))
                    # download_link(path, filename, link)
            # ENVIAR FATURA
                elif bill["Arquivo_Envio"] == 0:
                    print(Unidade)
                    print("Enviar " + str(bill["Arquivo_Envio"]))
                    print(link)
                    logger.info('	Enviar	{}	{}	{}	{}	{}	{}	{}'.format(
                        Unidade, NomeConcess, mesRef3, CodLink, DataEnvio, NomeUpload, link))
                    download_link(path, filename, link)
            except Exception as e:
                print(e)
                logger.critical('Download Erro {}'.format(Unidade, link))

            finally:
                self.queue.task_done()


def main():
    ts = time()
    queue = Queue()

    bills = get_bills()
    logger.critical('	Enviado	{}	{}	{}	{}	{}	{}	{}'.format(
        "Unidade", "Concessionária", "Mês Referência", "Lote", "Data Lote", "Nome Upload", "Link"))

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
