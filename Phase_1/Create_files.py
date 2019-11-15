import sys
import xml.etree.ElementTree as ET

class Create_files:
    def __init__(self):
        self.__tree = ET.parse(sys.argv[1])
        self.__root = self.__tree.getroot()
        self.__term = None
        self.__elem = None
    def iterate_file(self):
        #this function will call the four methods below to create files and will also itreate through the xml doc
        for parent in self.__root:#gen2 == <mail> will contain all the nested elements
            #each child node of parent can accesssed by index. 0 = row,1 = date,2 = from,3 = to,4 =subj,5 = cc, 6= bcc,7 = body
            self.__elem = parent
            self.terms()
            self.emails()
            self.dates()
            self.recs()
    def terms(self):
        #this method will create the term file
        subj = self.__elem[4].text.split()
        body = self.__elem[7].text.split()
        if len(subj) > len(body): max_length = len(subj)
        else: max_length = len(body)
        output = open('terms.txt','w')
        for item in range(max_length-1):
            if item < len(subj):
                subj_txt = self.format_text(subj[item])
                if subj_txt == self.__term and not(len(subj_txt) <= 2):
                    output.write('s-{}:{}'.format(subj_txt.lower(),self.__elem[0]))
            if item < len(body):
                subj_body = self.format_text(body[item])
                if subj_body == self.__term and not(len(subj_body) <= 2):
                    output.write('b-{}:{}'.format(subj[item].lower(),self.__elem[0]))
        output.close()
    @staticmethod
    def format_text(txt):
        return txt.replace(',','').replace('.','').replace('&#number;','').replace('&#10;','').replace('&lt','').replace('&gt;','')\
                .replace('&amp;','').replace('&apos;','').replace('&quot;','')
    def emails(self):
        pass
    def dates(self):
        pass
    def recs(self):
        pass
            