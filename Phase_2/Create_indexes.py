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
        self.tree_index('te.idx',self.__terms)
        self.tree_index('em.idx',self.__emails)
        self.tree_index('da.idx',self.__dates)
        self.hash_index('re.idx',self.__recs)
    def tree_index(self,output_filename,input_filename):
        self.__database.open(output_filename,None,db.DB_BTREE, db.DB_CREATE)
        tree_file = open(input_filename)
        tree_line = tree_file.readline()
        while tree_line != '':
            cut_off = tree_line.index(':')
            self.__database.put(tree_line[:cut_off].encode('utf-8'),tree_line[cut_off+1:].strip())
            tree_line = tree_file.readline()
        tree_file.close()
    def hash_index(self,output_filename,input_filename):
        self.__database.open(output_filename,None,db.DB_HASH, db.DB_CREATE)
        hash_file = open(input_filename)
        hash_line = hash_file.readline()
        while hash_line != '':
            cut_off = hash_line.index(':')
            self.__database.put(hash_line[:cut_off].encode('utf-8'),hash_line[cut_off+1:].strip())
            hash_line = hash_file.readline()
        hash_file.close()
x = Create_indexes()
x.create_indexes()