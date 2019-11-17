import os
import sys
from bsddb3 import db 
#hash index for recs
#B+ tree for terms
#B+ tree for emails
#B+ tree for dates
#KEY:DATA
class Create_indexes:
    #This class requires that dates.txt,emails.txt,recs.txt, and terms.txt exist
    def __init__(self):
        self.__terms = 'terms.txt'
        self.__emails = 'emails.txt'
        self.__dates = 'dates.txt'
        self.__recs = 'recs.txt'
        self.__database = db.DB()
    def sort_files(self):
        os.system('sort -u {}'.format(self.__terms))
        os.system('sort -u {}'.format(self.__emails))
        os.system('sort -u {}'.format(self.__emails))
        os.system('sort -u {}'.format(self.__recs))
    def create_indexes(self):
        #This method will call all the methods below which will create the index files
        self.sort_files()
        self.terms_index()
        self.emails_index()
        self.dates_index()
        self.recs_index()
    def terms_index(self):
        file_name = 'te.idx'
        self.__database.open(file_name,None,db.DB_BTREE, db.DB_CREATE)
        terms_file = open(self.__terms)
        terms_line = terms_file.readline()
        while terms_line != '':
            cut_off = terms_line.index(':')
            self.__database.put(terms_line[:cut_off].encode('utf-8'),terms_line[cut_off+1:].strip())
            terms_line = terms_file.readline()
        terms_file.close()
    def emails_index(self):
        pass
    def dates_index(self):
        pass
    def recs_index(self):
        pass
x = Create_indexes()
x.create_indexes()