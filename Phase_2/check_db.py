from bsddb3 import db 

database = db.DB()
database.open('te.idx')
curr = database.cursor()
iter = curr.first()
while iter:
    print(iter)
    iter = curr.next()