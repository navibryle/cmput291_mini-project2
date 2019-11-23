from bsddb3 import db
database = db.DB()
database.open('Phase_3/da.idx')
curr = database.cursor()
print(type(curr.set("REEEEEEEEEE".encode('utf-8'))))