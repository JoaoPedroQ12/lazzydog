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
    '020012', '020037', '020038', '020039'
]

class note:
    def __init__(self, nmov, date, client, product, color):
        self.nmov = nmov
        self.date = date
        self.client = client 
        self.product = product
        self.color = color

    def get_it(self, product: list, regex: str) -> list:
        """Função que retorna qualquer item dando uma lista e um padrao regex""""
        output = []
        for item in product:
            result = re.search(regex)
            output.append(result)
        return output

class paint_can(note):
    
    CODES = {'020036':'A', '020035':'A', '020034':'A', '020033':'C', '020032':'B', '020031':'A',
             '020030':'C', '020029':'B', '020028':'A', '020027':'C', '020026':'B', '020025':'A',
             '020024':'C', '020023':'B', '020022':'A', '020021':'B', '020020':'A', '020019':'B',
             '020018':'A', '020017':'C', '020016':'B', '020015':'A', '020014':'C', '020013':'B',
             '020012':'A', '020037':'A', '020038':'B', '020039':'C'}


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

