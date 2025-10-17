import os
import re
import glob
import sqlite3
from pathlib import Path

PATH = Path(__file__).resolve().parent

class Capture_date:
    def __init__(self, note):
        self.note = note or ""

    def nmov(self):
        m = re.search(r'Nr:\s*(\d+)', self.note)
        return m.group(1) if m else None

    def date(self):
        m re.search(r'Emissao:\s*(\d{2}/\d{2}/\d{4})', self.note)
        return m.group(1) if m else None

    def client(self):
        m = re.search(r'Cliente\.\:\s*(.+)', self.note)
        return m.group(1).strip() if m else None

    def product(self):
        return re.findall(r'(\d{6}\s+.+?\s+UN\s+\w+\s+[\d,.]+\s+[\d,.]+)', self.note)


class Paint_date(Capture_date): 

    CODES = {'020036':'A', '020035':'A', '020034':'A', '020033':'C', '020032':'B', '020031':'A',
             '020030':'C', '020029':'B', '020028':'A', '020027':'C', '020026':'B', '020025':'A',
             '020024':'C', '020023':'B', '020022':'A', '020021':'B', '020020':'A', '020019':'B',
             '020018':'A', '020017':'C', '020016':'B', '020015':'A', '020014':'C', '020013':'B',
             '020012':'A', '020037':'A', '020038':'B', '020039':'C'}

    def __init__(self, note=None):
        super().__init__(note)

    def color(self):
        return re.findall(r'#\w', self.note)

    def base_produto(self, code: str) -> str:
        """Função retorna a base referente ao codigo da tinta"""
        return self.CODES.get(code, None)            

    """Fazer um jeito de essa classe ter um metodo que faça uma busca em um db e esse venha retornar a base da cor, busque codigo e retorna baseapelid"""


class connection():
    def __ini__(self, path)
        self.path = path
        self.connection = connect(self.path)

    def connect(self, path_db):
        try:
            db = sqlite3.connect(path_db)
            return db
        except Excepetion as e:
            print(f'Houve um erro ao conectar no db:{e}')
    
    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        return self.connection.commit()

    def close(self):
        return self.connection.close()


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

file = list(glob.glob(os.path.join("point", "*.txt")))
db_path = PATH.joinpath("db" / "dbink.db")

db = connection(db_path)
notas = note(file)

delete_file(notas)
db.close()

