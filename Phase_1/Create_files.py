import sys
class Create_files:
    def __init__(self,filename):
        self.__filename = filename
        self.__elem = ['<row>','<date>','<from>','<to>','<subj>','<cc>','<bcc>','<body>']
        self.__rec = None
    def create_file(self):
        #this function will call the four methods below to create files and will also itreate through the xml doc
        xml_file = open(self.__filename)
        line = xml_file.readline()
        line = xml_file.readline()
        line = xml_file.readline()
        while line[:6] == '<mail>':
            #each child node of parent can accesssed by index. 0 = row,1 = date,2 = from,3 = to,4 =subj,5 = cc, 6= bcc,7 = body
            self.__rec = line.replace('<mail>','').replace('</mail>','').strip()
            self.sep_tags()
            self.terms()
            self.emails()
            self.dates()
            self.recs()
            self.__elem = ['<row>','<date>','<from>','<to>','<subj>','<cc>','<bcc>','<body>']
            line = xml_file.readline()
        xml_file.close()
    def sep_tags(self):
        pointer = 0
        word_start = 0
        tag_type = 'open'
        tag = ''
        content = ''
        while pointer != len(self.__rec):
            if self.__rec[pointer] == '<' and tag_type == 'open':#starting tag
                while self.__rec[pointer] != '>':
                    tag += self.__rec[pointer]
                    pointer += 1
                tag += self.__rec[pointer]
                pointer += 1
                tag_type = 'close'
            elif self.__rec[pointer] == '<' and tag_type == 'close':#ending tag
                while self.__rec[pointer] != '>':
                    pointer +=1
                self.__elem[self.__elem.index(tag)] = content 
                content = ''
                tag = ''
                tag_type = 'open'
            elif tag_type == 'close':#pointer is currently inside a tag
                content += self.__rec[pointer]
                pointer += 1
            else:
                pointer += 1
    #========HELPER METHODS====================================================================================
    @staticmethod
    def format_text(txt):
        txt = txt.replace('&amp;',' ').replace('&#10;',' ').replace('&lt;',' ').replace('&gt;',' ')\
            .replace('&apos;',' ').replace('&quot;',' ')
        for item in txt:
            if item not in ' -_' and not(item.isalnum()):
                txt = txt.replace(item,' ')
        return txt
    @staticmethod
    def check_if_empty(txt):
        if  txt == None: return ''
        else: return txt
    @staticmethod
    def convert_to_xml(txt):
        if txt == None:return ''
        else:
            return 
    #==========================================================================================================
    def terms(self):
        #this method will create terms.txt
        subj = self.format_text((self.__elem[4])).split()
        body = self.format_text((self.__elem[7])).split()
        max_length = max(len(subj),len(body))
        output = open('../Phase_2/terms.txt','a')
        for item in range(max_length):
            if item < len(subj):
                subj_txt = subj[item]
                if not(len(subj_txt) <= 2):
                    output.write('s-{}:{}\n'.format(subj_txt.lower(),self.__elem[0]))
            if item < len(body) :
                body_txt = body[item]
                if not(len(body_txt) <= 2):
                    output.write('b-{}:{}\n'.format(body_txt.lower(),self.__elem[0]))
        output.close()
    def emails(self):
        #this method will create emails.txt
        #this method will assume that from,to,cc,bcc will only contain emails
        from_mail = self.__elem[2].split(',')
        to = self.__elem[3].split(',')
        cc = self.__elem[5].split(',')
        bcc = self.__elem[6].split(',')
        max_length = max(len(from_mail),len(to),len(cc),len(bcc))
        output = open('../Phase_2/emails.txt','a')
        for item in range(max_length):
            if len(from_mail) > item and from_mail[item] != '':
                output.write('from-{}:{}\n'.format(from_mail[item].replace(' ','').lower(),self.__elem[0]))
            if len(to) > item and to[item] != '':
                output.write('to-{}:{}\n'.format(to[item].replace(' ','').lower(),self.__elem[0]))
            if len(cc) > item and cc[item] != '':
                output.write('cc-{}:{}\n'.format(cc[item].replace(' ','').lower(),self.__elem[0]))
            if len(bcc) > item and bcc[item] != '':
                output.write('bcc-{}:{}\n'.format(bcc[item].replace(' ','').lower(),self.__elem[0]))
        output.close()
    def dates(self):
        #this will create dates.txt
        output = open('../Phase_2/dates.txt','a')
        output.write('{}:{}\n'.format(self.__elem[1],self.__elem[0]))
        output.close()
    def recs(self):
        #this will create recs.txt
        output = open('../Phase_2/recs.txt','a')
        output.write('{}:<mail>{}</mail>\n'.format(self.__elem[0],self.__rec))
        output.close()
x = Create_files(sys.argv[1])
x.create_file()