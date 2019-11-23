import os
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
    def create_indexes(self):
        os.system('sort {}| uniq|python3 re_format.py|db_load -T -c duplicates=1 -t btree te.idx'.format(self.__terms))
        os.system('sort {}| uniq|python3 re_format.py|db_load -T -c duplicates=1 -t btree em.idx'.format(self.__emails))
        os.system('sort {}| uniq|python3 re_format.py|db_load -T -c duplicates=1 -t btree da.idx'.format(self.__dates))
        os.system('sort {}| uniq|python3 re_format.py|db_load -T -t hash re.idx'.format(self.__recs))