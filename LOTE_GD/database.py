import logging
import os
from urllib.request import urlretrieve
import mysql.connector
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


def connect_db():
    dbSge = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB')
    )

    return dbSge

def get_bills(bills_data):
    sql_query = '''
        ### MT
        (SELECT
            f.Cod_Empresa,
            f.Cod_UC,
            f.Cod_Fatura,
            z.Cod_Usina,
            UPPER(z.Rz_Social_UTF8) Usina,
            c.Sigla Concess,
            u.UC,
            IFNULL(i.Nome_Arquivo, i.Nome_Arquivo_Antigo) Nome_Upload,
            f.Mes_Ref,
            u.Tensao
        FROM
            Tab_Fatura_Dados f
        LEFT JOIN Tab_UC u ON f.Cod_UC = u.Cod_UC AND f.Cod_Empresa = u.Cod_Empresa
        LEFT JOIN Tbl_Concessionaria c ON u.Cod_Concess = c.Cod_Concess 
        LEFT JOIN Tab_Usinas z ON z.Cod_Usina = u.Cod_Usina AND z.Cod_Empresa = u.Cod_Empresa
        LEFT JOIN Tab_Upload_Faturas i ON i.Cod_Empresa = f.Cod_Empresa AND i.Cod_UC = f.Cod_UC AND f.Cod_Fatura = i.Cod_Fatura
        WHERE
            f.Cod_Empresa = %(Cod_Empresa)s 
            AND f.Mes_Ref > %(Mes_Ref)s
            AND u.Cod_Usina <> 0
            AND i.Arquivo_Envio_GD = 0
        )

        UNION

        ### BT
        (SELECT
            f.Cod_Empresa,
            f.Cod_UC,
            f.Cod_Fatura,
            z.Cod_Usina,
            UPPER(z.Rz_Social_UTF8) Usina,
            c.Sigla Concess,
            u.UC,
            IFNULL(i.Nome_Arquivo, i.Nome_Arquivo_Antigo) Nome_Upload,
            f.Mes_Ref,
            u.Tensao
        FROM
            Tab_Fatura_BT f
        LEFT JOIN Tab_UC u ON f.Cod_UC = u.Cod_UC AND f.Cod_Empresa = u.Cod_Empresa
        LEFT JOIN Tbl_Concessionaria c ON u.Cod_Concess = c.Cod_Concess 
        LEFT JOIN Tab_Usinas z ON z.Cod_Usina = u.Cod_Usina AND z.Cod_Empresa = u.Cod_Empresa
        LEFT JOIN Tab_Upload_Faturas i ON i.Cod_Empresa = f.Cod_Empresa AND i.Cod_UC = f.Cod_UC AND f.Cod_Fatura = i.Cod_Fatura
        WHERE
            f.Cod_Empresa = %(Cod_Empresa)s 
            AND f.Mes_Ref > %(Mes_Ref)s
            AND u.Cod_Usina <> 0
            AND i.Arquivo_Envio_GD = 0
        )
    '''
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute(sql_query, bills_data)
    bills = cursor.fetchall()

    cursor.close()
    db.close()

    return bills

def send_to_database(Usinas_Links, Usinas_Bills):
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    upload_date = datetime.today()

    sql_log = f'''INSERT INTO USINAS_CLARO_LOG SET 
        Cod_Lote = %(Cod_Lote)s,
        Cod_UC = %(Cod_UC)s,
        Cod_Empresa = %(Cod_Empresa)s,
        Cod_Fatura = %(Cod_Fatura)s,
        UC = %(UC)s,
        Mes_Ref = %(Mes_Ref)s,
        Nome_Arquivo = %(Nome_Arquivo)s,
        Data_Envio = %(Data_Envio)s
    '''

    sql_update = f'''UPDATE Tab_Upload_Faturas SET
        Arquivo_Envio_GD = 1,
        Data_Envio_GD = %(Data_Envio_GD)s,
        Cod_Link_GD = %(Cod_Lote)s
    WHERE
        Cod_Empresa = %(Cod_Empresa)s
        AND Cod_UC = %(Cod_UC)s
        AND Cod_Fatura = %(Cod_Fatura)s
        AND Arquivo_Envio_GD = 0;
    '''

    sql_insert = f'''INSERT INTO USINAS_CLARO SET
        link = %(link)s,
        excel = %(excel)s,
        lote = %(lote)s,
        loteclaro = %(loteclaro)s,
        conc = %(conc)s,
        faturasolicitada = %(faturasolicitada)s,
        faturaenviada = %(faturaenviada)s,
        data = %(data)s,
        envio = %(envio)s
    '''
    
    for Usina in Usinas_Links:
        Usina_Link = Usinas_Links[Usina]
        Usina_Bills = Usinas_Bills[Usina]

        data_insert = {
            'link': Usina_Link["zip"],
            'excel': Usina_Link["excel"],
            'lote': Usina,
            'loteclaro': "",
            'conc': Usina_Bills[0]["Concess"],
            'faturasolicitada': len(Usina_Bills),
            'faturaenviada': len(Usina_Bills),
            'data': upload_date,
            'envio': upload_date,
        }

        cursor.execute(sql_insert, data_insert)

        Cod_Lote = cursor.lastrowid

        for Bill in Usina_Bills:
            data_update = {
                'Data_Envio_GD': upload_date,
                'Cod_Lote': Cod_Lote,
                'Cod_Empresa': Bill["Cod_Empresa"],
                'Cod_UC': Bill["Cod_UC"],
                'Cod_Fatura': Bill["Cod_Fatura"],
            }

            cursor.execute(sql_update, data_update)

            data_log = {
                'Cod_Lote': Cod_Lote,
                'Cod_UC': Bill["Cod_UC"],
                'Cod_Empresa': Bill["Cod_Empresa"],
                'Cod_Fatura': Bill["Cod_Fatura"],
                'UC': Bill["UC"],
                'Mes_Ref': Bill["Mes_Ref"],
                'Nome_Arquivo': Bill["Nome_Upload"],
                'Data_Envio': upload_date,
            }

            cursor.execute(sql_log, data_log)

    db.commit()

def download_link(directory, link, custom_name = False):
    download_name = os.path.basename(link)
    if(custom_name):
        download_name = custom_name

    download_path = directory + download_name
    urlretrieve(link, filename=download_path)


if __name__ == '__main__':
    print("Execute o arquivo main.py")
    
    # for bill in get_bills():
    #     print(bill)