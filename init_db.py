import sqlite3
import os
from pathlib import Path

sql_db = """CREATE TABLE IF NOT EXISTS recordink(id INTEGER PRIMARY KEY, nmov TEXT, client TEXT, data TEXT, produto TEXT, cor TEXT, obs TEXT)"""
path_db = Path(__file__).resolve().parent

def creat_db(sql: str):
	try:
		db = sqlite3.connect(path_db.joinpath("db") / "dbink.db")
		cursor = db.cursor()
		cursor.execute(sql)
		db.commit()
		print("Creat of the db was a sucess.")
	except:
		print(f"Something went wrong")
	finally:
		db.close()
	
creat_db(sql_db)
	
