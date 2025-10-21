from ObjectRex import Capture_date, Paint_date, Database
import glob
import sqlite3
import os

PATH_POINT = "point"
PATH_DB = "db/dbink.db"

def dell(file):
    return os.remove(file)

product_ink = []
codes = []
db = Database(PATH_DB)
index = 0

nota_file = next(iter(glob.glob(PATH_POINT +  "/*.txt", recursive=False)))

if not nota_file:
	print("Não ha notas")
else:
	nota = Capture_date(nota_file)
	paint_date = Paint_date(nota_file)

	for i, product in enumerate(nota.product()):
		if paint_date.base_produto(nota.code_product()[i]) is not None:
			product_ink.append(product)
			codes.append(nota.code_product()[i])
			
	if product_ink:
		cor = paint_date.color()
		for i in codes:
			for j in cor:
				if paint_date.busca_cor(j) != paint_date.base_produto(i):
					index += 1
	else:
		print("Não a produtos")

	if index >= len(product_ink):
			print(f"[ATENÇÂO] Algumas das bases não condiz com a cor, por favor de uma olhada na nota!.\nNúmero: {nota.nmov()}\nData: {nota.date()}\nCliente: {nota.client()}")
	else:
		db.conectar()
		for item in product_ink:
			db.executar("INSERT INTO recordink (nmov, client, data, produto, cor, obs) VALUES (?, ?, ?, ?, ?, ?)", (nota.nmov(), nota.client(), nota.date(), item, str(paint_date.color()), nota.observ()))

dell(nota_file)
db.desconectar()
