import sys
import xml.etree.ElementTree as ET

class Create_files:
    def __init__(self,filename):
        self.__tree = ET.parse(filename)
        self.__root = self.__tree.getroot()
        self.__term = 'gas'
        self.__elem = None
    def create_file(self):
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
        if self.__elem[4].text == None: subj = ''
        else:subj = self.__elem[4].text.split()
        if self.__elem[7].text == None: body = ''
        else:body = self.__elem[7].text.split()
        if len(subj) > len(body): max_length = len(subj)
        else: max_length = len(body)
        output = open('terms.txt','a')
        for item in range(max_length-1):
            if item < len(subj):
                subj_txt = self.format_text(subj[item])
                if subj_txt == self.__term and not(len(subj_txt) <= 2):
                    output.write('s-{}:{}\n'.format(subj_txt.lower(),self.__elem[0].text))
            if item < len(body):
                body_txt = self.format_text(body[item])
                if body_txt == self.__term and not(len(body_txt) <= 2):
                    output.write('b-{}:{}\n'.format(body_txt.lower(),self.__elem[0].text))
        output.close()
    @staticmethod
    def format_text(txt):
        return txt.replace(',','').replace('.','').replace('&#number;','').replace('&#10;','').replace('&lt','').replace('&gt;','')\
                .replace('&amp;','').replace('&apos;','').replace('&quot;','').lower()
    def emails(self):
        pass
    def dates(self):
        pass
    def recs(self):
        pass
x = Create_files(sys.argv[1])
x.create_file()