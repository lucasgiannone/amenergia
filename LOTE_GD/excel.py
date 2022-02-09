import os
import re
import xlsxwriter
from datetime import datetime
from unidecode import unidecode

def clean_usina_name(name):
    name = unidecode(name)
    name = re.sub(r' [0-9|IV]{0,4}$', '', name)
    name = name.strip()

    return name  

def usinas_dict_from_bills(bills):
    Usinas = {}

    for bill in bills:
        Usina = clean_usina_name(bill["Usina"])

        if Usina not in Usinas:
            Usinas[Usina] = []

        Usinas[Usina].append(bill)
    
    return Usinas

def write_bills_xlsx(bills):
    Usinas = usinas_dict_from_bills(bills)
        
    date_name = datetime.today().strftime('%Y%m%d')
    for Usina in Usinas:
        path = f'./excel'
        os.makedirs(path, exist_ok=True)

        filename = f'{Usina} - e{date_name}.xlsx'
        wb = xlsxwriter.Workbook(f'{path}/{filename}')
        ws = wb.add_worksheet()

        ws.write('A1', 'UC')
        ws.write('B1', 'Concessionária')
        ws.write('C1', 'Mês de Referência')

        for index in range(len(Usinas[Usina])):
            bill = Usinas[Usina][index]
            xlsx_index = str(index + 2)

            Uc = str(bill["UC"])
            Concess = str(bill["Concess"])
            Mes_Ref = bill["Mes_Ref"].strftime("%d/%m/%Y")

            ws.write(f'A{xlsx_index}', Uc)
            ws.write(f'B{xlsx_index}', Concess)
            ws.write(f'C{xlsx_index}', Mes_Ref)

        wb.close()

    return Usinas

if __name__ == '__main__':
    print("Execute o arquivo main.py")
    # var = clean_usina_name('MARABÁ 1')
    # print(var)