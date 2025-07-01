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


def capturedate(notas):
    for nota in notas:
        with open(nota, encoding="latin-1") as file:
            content = file.read()
            nmov = re.search(r'Nr:\s*(\d+)', content)
            date = re.search(r'Emissao:\s*(\d{2}/\d{2}/\d{4})', content)
            client = re.search(r'Cliente\.\:\s*(.+)', content)
            product = re.findall(r'(\d{6}\s+.+?\s+UN\s+\w+\s+[\d,.]+)', content)
            color = re.findall(r'#\w+', content)

            if nmov and date and client and product:
                return nmov.group(), date.group(), client.group(), product, color

def inserintodb(DB, nmov, date, client, products, color):
    cursor = DB.cursor()
    try:
        for item in products:
            for code in CODES:
                if item.find(code) != -1:
                    cursor.execute("""INSERT INTO recordink(nmov, client, data, produto, cor) VALUES(?, ?, ?, ?, ?)""", (nmov, date, client.strip(), item, str(color)))
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

nmov, date, client, product, color = capturedate(notas)
inserintodb(db, nmov, date, client, product, color)
delete_file(notas)
db.close()

