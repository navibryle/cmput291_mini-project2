import os
import sys
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
        pass
    def emails_index(self):
        pass
    def dates_index(self):
        pass
    def recs_index(self):
        pass