class Create_files:
    def __init__(self,filename):
        self.__filename = filename
        self.__elem = ['<row>','<date>','<from>','<to>','<subj>','<cc>','<bcc>','<body>']
        self.__rec = None
        self.__terms = open('terms.txt','a')
        self.__emails = open('emails.txt','a')
        self.__dates = open('dates.txt','a')
        self.__recs = open('recs.txt','a')
    def create_file(self):
        #this function will call the four methods below to create files and will also itreate through the xml doc
        xml_file = open(self.__filename)
        line = xml_file.readline()
        line = xml_file.readline()
        line = xml_file.readline()
        while line[:6] == '<mail>':
            #each child node of parent can accesssed by index. 0 = row,1 = date,2 = from,3 = to,4 =subj,5 = cc, 6= bcc,7 = body
            self.__rec = line[6:-8]
            self.sep_tags()
            self.__dates.write('{}:{}\n'.format(self.__elem[1],self.__elem[0]))
            self.__recs.write('{}:<mail>{}</mail>\n'.format(self.__elem[0],self.__rec))
            self.__elem = ['<row>','<date>','<from>','<to>','<subj>','<cc>','<bcc>','<body>']
            self.__rec = None
            line = xml_file.readline()
        self.__terms.close()
        self.__emails.close()
        self.__dates.close()
        self.__recs.close()
        xml_file.close()
    def sep_tags(self):
        count = 0
        pointer = 0
        for item in self.__elem:
            pointer += len(item)
            output = ''
            if item == '<subj>' or item =='<body>':
                while self.__rec[pointer] != '<':
                    if self.__rec[pointer] == '&':#means this term is to be ignored
                        while self.__rec[pointer] != ';':#each of the terms to be ignored ends with ;
                            pointer += 1
                        pointer += 1
                        if item == '<subj>' and len(output) > 2: 
                            self.__terms.write('s-{}:{}\n'.format(output.lower(),self.__elem[0]))
                            output = ''
                        elif item == '<body>' and len(output) > 2: 
                            self.__terms.write('b-{}:{}\n'.format(output.lower(),self.__elem[0]))
                            output =''
                        elif len(output) <= 2 : output = ''
                    elif (self.__rec[pointer] not in '-_' and not(self.__rec[pointer].isalnum())):
                        if item == '<subj>' and len(output) > 2: 
                            self.__terms.write('s-{}:{}\n'.format(output.lower(),self.__elem[0]))
                            output = ''
                        elif item == '<body>' and len(output) > 2: 
                            self.__terms.write('b-{}:{}\n'.format(output.lower(),self.__elem[0]))
                            output = ''
                        elif len(output) <= 2 : output = ''
                        pointer += 1
                    else:
                        output += self.__rec[pointer]
                        pointer += 1
                output = ''
                pointer += len(item)+1
            elif item in ['<from>','<to>','<cc>','<bcc>']:
                while self.__rec[pointer] != '<':
                    if self.__rec[pointer] == ' ' or self.__rec[pointer] == ',' or self.__rec[pointer+1] == '<':
                        if self.__rec[pointer+1] == '<':output = output + self.__rec[pointer]
                        if item== '<from>':
                            self.__emails.write('from-{}:{}\n'.format(output.lower(),self.__elem[0]))
                        elif item== '<to>':
                            self.__emails.write('to-{}:{}\n'.format(output.lower(),self.__elem[0]))
                        elif item== '<cc>':
                            self.__emails.write('cc-{}:{}\n'.format(output.lower(),self.__elem[0]))
                        elif item== '<bcc>':
                            self.__emails.write('bcc-{}:{}\n'.format(output.lower(),self.__elem[0]))
                        output = ''
                        pointer += 1
                    else:
                        output += self.__rec[pointer]
                        pointer += 1
                pointer += len(item)+1
            else:
                while self.__rec[pointer] != '<':
                    output += self.__rec[pointer]
                    pointer += 1
                self.__elem[count] = output
                output = ''
                pointer += len(item)+1
            count += 1
        
        
