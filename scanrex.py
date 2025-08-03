import os
import re
import glob
import sqlite3
from pathlib import Path

PATH = Path(__file__).resolve().parent
CODES = [
    '020036', '020035', '020034', '020033', '020032', '020031',
    '020030', '020029', '020028', '020027', '020026', '020025',
    '020024', '020023', '020022', '020021', '020020', '020019',
    '020018', '020017', '020016', '020015', '020014', '020013',
    '020012'
]

class note:
    def __init__(self, nmov, date, client, product, color):
        self.nmov = nmov
        self.date = date
        self.client = client 
        self.product = product
        self.color = color

    def get_code_product(self, product: list) -> list:
        """Função retorna somente os codigos dos produtos'"""
        codes = []
        for item in product:
            code = re.search(r'(\d{6})')
            codes.append(code)
        return codes

    def base(self, product):
        pass

    def price(self, product):
        pass

class paint_can(note):
    
    CODES = {'020036':'A', '020035':'A', '020034':'A', '020033':'A', '020032':'A', '020031':'A',
             '020030':'A', '020029':'A', '020028':'A', '020027':'A', '020026':'A', '020025':'A',
             '020024':'A', '020023':'A', '020022':'A', '020021':'A', '020020':'A', '020019':'A',
             '020018':'A', '020017':'A', '020016':'A', '020015':'A', '020014':'A', '020013':'A',
             '020012':'A'}

    def its_paint(self, products: list) -> int:
        """Função recebe os codigos dos produtos e retorn 1 se e uma lata de tinta e 0 caso não"""
        flag = 0
        for item in products:
            if item == CODES.keys():
                flag += 1
        return flag

    def base_paint(self, code: str) -> str:
        """Função retorna a base referente ao codigo da tinta"""
        return CODES[code]
            

class verefication(note):
    pass

class send(verefication):
    pass

def capturedate(notas):
    result = []
    for nota in notas:
        with open(nota, encoding="latin-1") as file:
            content = file.read()
            nmov = re.search(r'Nr:\s*(\d+)', content)
            date = re.search(r'Emissao:\s*(\d{2}/\d{2}/\d{4})', content)
            client = re.search(r'Cliente\.\:\s*(.+)', content)
            product = re.findall(r'(\d{6}\s+.+?\s+UN\s+\w+\s+[\d,.]+\s+[\d,.]+)', content)
            color = re.findall(r'#\w+', content)

            if nmov and date and client and product:
                result.append((nmov.group(), date.group(), client.group(), product, color))
    return result

def inserintodb(DB, nmov, date, client, products, color):
    cursor = DB.cursor()
    try:
        for item in products:
            for code in CODES:
                if item.find(code) != -1:
                    cursor.execute("""INSERT INTO recordink(nmov, client, data, produto, cor) VALUES(?, ?, ?, ?, ?)""", (nmov, client.strip(), date, item, str(color)))
                    DB.commit()
    except Exception as e:
        print(f"Houve um erro em inserir no DB: {e}")
    finally:
        cursor.close()

def delete_file(files):
    try:
        for file in files:
            os.remove(file)
    except Exception as e:
        print(f"Houve um erro ao deletar os arquivos {e}")
    
def connectdb():
    try:
        db = sqlite3.connect(PATH.joinpath("db") / "dbink.db")
        return db
    except:
        print("Something was wrong in connect db.")

nmov = ""
date = ""
client = ""
product = ""
color = ""

db = connectdb()

path_db = Path(__file__).resolve().parent

#Point for acess TXT
notas = list(glob.glob(os.path.join("point", "*.txt")))

results = capturedate(notas)

for date in results:
    nmov, date, client, product, color = date
    inserintodb(db, nmov, date, client, product, color)

delete_file(notas)
db.close()

