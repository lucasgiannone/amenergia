import logging
import os
from urllib.request import urlretrieve
import mysql.connector
import csv
import re
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename='download.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def connect_db():
    dbSge = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB')
    )

    return dbSge


def get_bills():
    with open('.\DownloadList.csv') as csvfile:
        downloadlist = list(csv.reader(csvfile))
    bills = []
    for row in downloadlist:
        row = row[0].split(';')
        # print(row)
        uc = re.sub(r"[\[\]]", "", str(row[0]))
        mes = datetime.strptime(str(row[1]),'%d/%m/%Y').strftime("%Y-%m-%d")
        print(uc,mes)
        sql_query = f'''
            ## BT
            (SELECT C.Sigla, A.Cod_Link, A.Data_Envio, A.Arquivo_Envio, A.Cod_UC, U.UC, B.Mes_Ref, A.Nome_Arquivo_Antigo AS Nome_Upload, B.Cod_Fatura, U.Tensao    
            FROM Tab_Upload_Faturas A
				LEFT JOIN Tab_Fatura_BT B ON A.Cod_UC = B.Cod_UC AND A.Cod_Empresa = B.Cod_Empresa AND A.Cod_Fatura = B.Cod_Fatura
				LEFT JOIN Tab_UC U ON U.Cod_UC = B.Cod_UC AND U.Cod_Empresa = B.Cod_Empresa
				LEFT JOIN Tbl_Concessionaria C ON C.Cod_Concess = B.Cod_Concess
            WHERE 
				A.Cod_Empresa = '1704'
            AND Mes_Ref >= '{mes}'
				AND Mes_Ref <= '{mes}'
				AND Nome_Upload != ''
				AND U.UC = '{uc}'
            )

            UNION

            ## MT
            (SELECT C.Sigla, A.Cod_Link, A.Data_Envio, A.Arquivo_Envio, A.Cod_UC, U.UC, B.Mes_Ref, A.Nome_Arquivo_Antigo AS Nome_Upload, B.Cod_Fatura, U.Tensao
            FROM Tab_Upload_Faturas A
				LEFT JOIN Tab_Fatura_Dados B ON A.Cod_UC = B.Cod_UC AND A.Cod_Empresa = B.Cod_Empresa AND A.Cod_Fatura = B.Cod_Fatura
				LEFT JOIN Tab_UC U ON U.Cod_UC = B.Cod_UC AND U.Cod_Empresa = B.Cod_Empresa
				LEFT JOIN Tbl_Concessionaria C ON C.Cod_Concess = B.Cod_Concess
            WHERE 
				A.Cod_Empresa = '1704'
                AND Mes_Ref >= '{mes}'
				AND Mes_Ref <= '{mes}'
				AND Nome_Upload != ''
				AND U.UC = '{uc}'
            )
            ORDER BY Mes_Ref;
        '''
        # print(sql_query)
        db_sge = connect_db()
        cursor_sge = db_sge.cursor(dictionary=True)
        cursor_sge.execute(sql_query)
        ucbills = cursor_sge.fetchall()
        if cursor_sge.rowcount == 0:
            logger.error(f'{uc}	{mes}	Sem faturamento')
        else:
            for bill in ucbills:
                logger.info(f'{uc}	{mes}	Fatura encontrada')
                bills.append(bill)

    return bills


def download_link(directory, dbname, link):
    download_path = directory + dbname
    urlretrieve(link, filename=download_path)

    return download_path


if __name__ == '__main__':
    for bill in get_bills():
        print(bill["Arquivo_Envio"])
