from dbfread import DBF
import dataset

db = dataset.connect('sqlite:///latex.sqlite')
table = db['latex']

print(table.find_one(codigo="BRB172"))

