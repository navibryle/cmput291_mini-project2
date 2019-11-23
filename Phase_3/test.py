from bsddb3 import db
database = db.DB()
database.open('da.idx')
curr = database.cursor()
r = curr.first()
r = curr.prev()

print(r)