import sys
import xml.etree.ElementTree as ET

class Create_files:
    def __init__(self,filename):
        self.__filename = filename
        self.__tree = ET.parse(filename)
        self.__root = self.__tree.getroot()
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
    #========HELPER METHODS====================================================================================
    @staticmethod
    #
    def format_text(txt):
        return txt.replace('&',' ').replace(',',' ').replace('.',' ').replace('<',' ').replace('>',' ')\
                .replace("'" ,' ').replace('"',' ').replace(':',' ').replace(';',' ').replace('/',' ')\
                    .replace('?',' ').replace("!",' ').replace('|',' ').replace("\\",' ').replace('(',' ').replace(')','')\
                        .replace('%',' ').replace('=',' ').replace('$',' ').replace('+',' ').lower()
    @staticmethod
    def check_if_empty(txt):
        if  txt == None: return ''
        else: return txt
    @staticmethod
    def convert_to_xml(txt):
        if txt == None:return ''
        else:
            return txt.replace('&','&amp;').replace('\n','&#10;').replace('<','&lt;').replace('>','&gt;')\
            .replace("'",'&apos;').replace('"','&quot;')
    #==========================================================================================================
    def terms(self):
        #this method will create terms.txt
        subj = self.format_text(self.check_if_empty(self.__elem[4].text)).split()
        body = self.format_text(self.check_if_empty(self.__elem[7].text)).split()
        max_length = max(len(subj),len(body))
        output = open('../Phase_2/terms.txt','a')
        for item in range(max_length):
            if item < len(subj):
                subj_txt = subj[item]
                if not(len(subj_txt) <= 2):
                    output.write('s-{}:{}\n'.format(subj_txt.lower(),self.__elem[0].text))
            if item < len(body) :
                body_txt = body[item]
                if not(len(body_txt) <= 2):
                    output.write('b-{}:{}\n'.format(body_txt.lower(),self.__elem[0].text))
        output.close()
    def emails(self):
        #this method will create emails.txt
        #this method will assume that from,to,cc,bcc will only contain emails
        from_mail = self.check_if_empty(self.__elem[2].text).split()
        to = self.check_if_empty(self.__elem[3].text).split()
        cc = self.check_if_empty(self.__elem[5].text).split()
        bcc = self.check_if_empty(self.__elem[6].text).split()
        max_length = max(len(from_mail),len(to),len(cc),len(bcc))
        output = open('../Phase_2/emails.txt','a')
        for item in range(max_length):
            if len(from_mail) > item and from_mail[item] != '':
                output.write('from-{}:{}\n'.format(from_mail[item].replace(',','').lower(),self.__elem[0].text))
            if len(to) > item and to[item] != '':
                output.write('to-{}:{}\n'.format(to[item].replace(',','').lower(),self.__elem[0].text))
            if len(cc) > item and cc[item] != '':
                output.write('cc-{}:{}\n'.format(cc[item].replace(',','').lower(),self.__elem[0].text))
            if len(bcc) > item and bcc[item] != '':
                output.write('bcc-{}:{}\n'.format(bcc[item].replace(',','').lower(),self.__elem[0].text))
        output.close()
    def dates(self):
        #this will create dates.txt
        output = open('../Phase_2/dates.txt','a')
        output.write('{}:{}\n'.format(self.__elem[1].text,self.__elem[0].text))
        output.close()
    def recs(self):
        #this will create recs.txt
        output = open('../Phase_2/recs.txt','a')
        output.write('{}:<mail><row>{}</row><date>{}</date><from>{}</from><to>{}</to><subj>{}</subj><cc>{}</cc><bcc>{}</bcc><body>{}</body></mail>\n'\
            .format(self.__elem[0].text,self.__elem[0].text,self.__elem[1].text,self.__elem[2].text,self.__elem[3].text,\
                self.convert_to_xml(self.__elem[4].text),self.convert_to_xml(self.__elem[5].text),self.convert_to_xml(self.__elem[6].text),self.convert_to_xml(self.__elem[7].text)))
        output.close()
x = Create_files(sys.argv[1])
x.create_file()