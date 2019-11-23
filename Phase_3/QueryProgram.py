from bsddb3 import db
class OutputArgsEnum:
    full = "full"
    brief = "brief" # only print out (id) and (title)

class QueryProgram:
    __currentOutputFormat = OutputArgsEnum.brief
    __argStatus = True
    __keywords = ["subj:", "body:", "from:", "to:", "bcc:", "cc:"]
    # query session
    def __init__(self):
        self.__curr = None
        self.__db = None
        self.__output_type = 'brief'
        self.__terms = []#all terms that are to be queried
        self.__emails = []#all emails that are to be queried
        self.__dates = []#all dates that are to be quered
        self.__rowID = []
    def open_db(self,dbname):
        self.__db = db.DB()
        self.__db.open(dbname)
        self.__curr = self.__db.cursor()
    def close_db(self):
        self.__db.close()
    def startSession(self):
        # run a loop in the terminal for the user to perform actions
        inp = 'Y'
        while inp != 'N' :
            #This is a string traversal algorithm that takes out extraneous spaces
            if inp != 'Y' and inp != 'N':
                inp = input('Please enter Y or N: ')
                continue
            else:
                self.get_query()
                self.term_search()
            inp = input("Enter another query (Y/N): ").upper()
    def get_query(self):
        #This is a string traversal algorithm that takes out extraneous spaces
        #it also distributes queries onti terms,dates, or emails
        query = input("Enter query: ").strip().lower()
        cur_char = 0#pointer to chracters of query
        last_word = None#pointer to where the previous character before the space was
        operator = [':','<','=','<=','>=']
        cur_word = ''
        tag = ''
        oper = ''
        data = ''
        while cur_char < len(query):
            if query[cur_char] == ' ' and query[cur_char+1] == ' ':
                cur_char += 1
            elif query[cur_char] == ' ' and (query[cur_char+1] in operator or query[cur_char+1]+query[cur_char+2] in operator):
                if query[cur_char+1] in operator:
                    tag = cur_word
                    oper = query[cur_char+1]
                    cur_word += query[cur_char+1]
                    last_word = query[cur_char+1]
                    cur_char+=2
                elif query[cur_char+1]+query[cur_char+2] in operator:
                    cur_word += query[cur_char+1]+query[cur_char+2]
                    last_word = query[cur_char+1]+query[cur_char+2]
                    cur_char += 3
            elif cur_char == len(query)-1 or (query[cur_char] == ' ' and query[cur_char+1] != ' ' and (last_word not in operator)):
                #if here we completed formatting a query therefore we have the ability to add a space
                #also tag and oper mustve been completed, meaning we have an xml tag and an operator 
                #cur_word must be containing a query
                if cur_char == len(query)-1:
                    cur_word += query[cur_char]
                if cur_word == 'output=brief':
                    self.__output_type = 'brief'
                    cur_word = ''
                elif cur_word == 'output=full':
                    self.__output_type = 'full'
                    cur_word = ''
                else:
                    data = cur_word.replace(tag,'').replace(oper,'')
                    self.distribute_query(tag,oper,data)
                    tag = ''
                    oper =''
                    data = ''
                    cur_word = ''
                cur_char += 1
            elif query[cur_char] != ' ':#query[cur_char] is an alphanumeric-_ character
                last_word = query[cur_char]
                cur_word += query[cur_char]
                cur_char += 1
            else:
                cur_char += 1
    def distribute_query(self,tag,oper,data):
        #this function will help get_query to distribute each parts of the query to the proper list
        if tag.lower() == 'date':#this means that current query is a date search
            self.__dates.append(tag+oper+data)
            sorted(self.__dates)
        elif tag.lower() == 'from' or tag.lower() == 'to' or tag.lower() =='cc' or tag.lower() =='bcc':#thsi means that query is an email search
            self.__emails.append(tag+oper+data)
            sorted(self.__emails)
        else:#this means that query is a term search
            self.__terms.append(tag+oper+data)
            sorted(self.__terms)
    def term_search(self):
        '''
        term_search will break down self.__terms, which contains all the terms that need to be found into terms that are kept in subject and body fields
        a list is also made for terms that dont have any tag to initilize where the term is located.
        '''
        self.__terms = list(set(self.__terms))#remove duplicates
        subj = []
        body = []
        both = []
        for item in self.__terms:
            if ':' in item:
                if 'subj' in item:
                    subj.append(item[item.index(':')+1:])
                elif 'body' in item:
                    body.append(item[item.index(':')+1:])
            else:
                both.append(item)
        self.open_db('te.idx')
        max_length = len(subj)+len(body)+len(both)
        pointer = 0
        subj_point = 0
        body_point = 0
        both_point = 0
        row_result = [] 
        while subj_point+body_point+both_point < max_length:#if sum point == max_length then searches have been performed on all possible terms
            while body_point < len(body):
                if (both_point < len(both) and body[body_point] <= both[both_point]) or both_point >= len(both):
                    #when both_point >= len(both it means that both has been iterated through entirely)
                    body_point += self.find_term(body[body_point],row_result,'b-')
                elif both_point < len(both) and body[body_point] > both[both_point]:
                    both_point += self.find_term(body[body_point],row_result,'b-')
            while subj_point < len(subj):
                if (both_point < len(both) and subj[subj_point] <= both[both_point]) or both_point >= len(both):
                    #when both_point >= len(both it means that both has been iterated through entirely)
                    subj_point += self.find_term(subj[subj_point],row_result,'b-')
                elif both_point < len(both) and subj[subj_point] > both[both_point]:
                    both_point += self.find_term(subj[subj_point],row_result,'b-')
            while subj_point < len(subj):
                if (both_point < len(both) and subj[subj_point] <= both[both_point]) or both_point >= len(both):
                    #when both_point >= len(both it means that both has been iterated through entirely)
                    subj_point += self.find_term(subj[subj_point],row_result,'b-')
                elif both_point < len(both) and subj[subj_point] > both[both_point]:
                    both_point += self.find_term(subj[subj_point],row_result,'b-')
            while subj_point < len(subj):
                if (both_point < len(both) and subj[subj_point] <= both[both_point]) or both_point >= len(both):
                    #when both_point >= len(both it means that both has been iterated through entirely)
                    subj_point += self.find_term(subj[subj_point],row_result,'b-')
                elif both_point < len(both) and subj[subj_point] > both[both_point]:
                    both_point += self.find_term(subj[subj_point],row_result,'b-')
            while both_point < len(both):
                if (both_point < len(both)):
                    #when both_point >= len(both it means that both has been iterated through entirely)
                    both_point += self.find_term(both[both_point],row_result,'b-')
            print(row_result)
    def find_term(self,term,row_result,tag = ''):
        #result[0] is the key and result[1] is the data
        #row_result will be mutated if terms are in the database
        term = tag+term#tag is the prefix to every term in the idx file i.e 's-' or 'b-'
        #a tag is also added to terms that are not initialized by a tag so that the cursor does not iterate the entire database
        pointer_increment = 0#number of times to increment the pointer
        if '%' in term:
            result = self.__curr.set_range(term.encode('utf-8'))
            if result != None:
                row_result.append(result[1].decode('utf-8'))
                result = self.__curr.next()
                while term in result[0].decode('utf-8'):#this while loop is to check duplicates since db is sorted therefore same terms will be next to each other
                    row_result.append(result[1].decode('utf-8'))
                    result = self.__curr.next()
                return 1#to increment the outside pointer to body list
            else:return 1#term does not exist therefore no increment
        else:
            result = self.__curr.set(term.encode('utf-8'))
            if result != None:# if result==None term does not exist
                row_result.append(result[1].decode('utf-8'))
                result = self.__curr.next()
                while term == result[0].decode('utf-8'):#this while loop is to check duplicates since db is sorted therefore same terms will be next to each other
                    row_result.append(result[1].decode('utf-8'))
                    result = self.__curr.next()
                return 1#to increment the outside pointer to body list
            else:return 1#term does not exist therefore no increment
        def execute_query(self):
            self.term_search()
    ''' 
    def EvaluateArgumentsFullFormat(self, arguments):
        # print out arguments in full format
        # paramter: arguments is a list of tuple of two possible formats below [(argument), (argument), (argument), ... , (argument)]
        # (1) argument = (search term)
        # (2) argument = (keyword, operator, value) eg. (bcc, :, brian@gmail.com)
        print("REEEEEEE")
        for arg in arguments:
            if (len(arg) == 1):
                #subj and body
                # argument is a search term:::    argument = (search term)
                searchTerm = arg[0]
                #--------------------Perform search term operation on database below------------------------------#
                self.open_db('te.idx')
                row_id = []
                output = []
                self.iterDB(row_id,'s',searchTerm)
                self.iterDB(row_id,'b',searchTerm)
                self.close_db()
                self.open_db('re.idx')
                for item in row_id:
                    result = self.__db.get(item.encode('utf-8')).decode('utf-8')
                    output.append(result)
                print(output)
            elif (len(arg) == 3):
                # argument is a search term:::    argument = (keyword, operator, value)
                keyWord = arg[0]
                operator = arg[1]
                value = arg[2]
                #--------------------Perform query operation on database below------------------------------#

            else:
                print("argument has too few or too many indices: argument = {0}").format(arg)
    def redirect_query(self,command):
        while True:
                    command = input("enter a command: ")
                    command = command.lower()
                    filteredArguments = command.split(" ")
                    __argStatus = True

                    # filter out blank spaces
                    filteredArguments = []
                    for i in range(len(arguments)):                      
                        if (i != ""):
                            filteredArguments.append(arguments[i]) 
                    # check if one of the arguments specifies a change in format (output=brief or output=full)
                    # for valid __argStatus, arguments must be in the form
                    # (1) (search term)
                    # (2) (keyword, operator, value) eg. (option, =, yep) 
                    arguments = []
                    index = 0
                    previousWord = None
                    acceptableLetters = set("0123456789abcdefghijklmnopqrstuvwxyz_-%=:><)/")
                    while index < len(filteredArguments) and QueryProgram.__argStatus:
                        if (">=" in filteredArguments[index]):
                            queryArgs = filteredArguments[index].split(">=") # [keyword, value]
                            if (queryArgs[0] == "" and queryArgs[1] == ""):
                                # keyword and value missing so use previous word as keyword, next word as value
                                # check acceptable characters
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                argumentPair = (previousWord, ">=", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 2
                            elif (queryArgs[0] == ""):
                                # keyword is missing, so use previous word
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, ">=", queryArgs[1])
                                arguments.append(argumentPair)
                                index += 1
                            elif (queryArgs[1] == ""):
                                # value that would applied to the keyword is missing, so use next word
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], ">=", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                index += 2
                            else:
                                # both keyword and value are provided
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], ">=", queryArgs[1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 1
                                

                        elif ("<=" in filteredArguments[index]):
                            queryArgs = filteredArguments[index].split("<=") # [keyword, value]
                            if (queryArgs[0] == "" and queryArgs[1] == ""):
                                # keyword and value missing so use previous word as keyword, next word as value
                                # check acceptable characters
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, "<=", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 2
                            elif (queryArgs[0] == ""):
                                # keyword is missing, so use previous word
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, "<=", queryArgs[1])
                                arguments.append(argumentPair)
                                index += 1
                            elif (queryArgs[1] == ""):
                                # value that would applied to the keyword is missing, so use next word
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], "<=", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                index += 2
                            else:
                                # both keyword and value are provided
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                    
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                            
                                argumentPair = (queryArgs[0], "<=", queryArgs[1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 1
                                


                        elif (">" in filteredArguments[index]):
                            queryArgs = filteredArguments[index].split(">") # [keyword, value]
                            if (queryArgs[0] == "" and queryArgs[1] == ""):
                                # keyword and value missing so use previous word as keyword, next word as value
                                # check acceptable characters
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                            
                                argumentPair = (previousWord, ">", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 2
                            elif (queryArgs[0] == ""):
                                # keyword is missing, so use previous word
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                    
                                argumentPair = (previousWord, ">", queryArgs[1])
                                arguments.append(argumentPair)
                                index += 1
                            elif (queryArgs[1] == ""):
                                # value that would applied to the keyword is missing, so use next word
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], ">", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                index += 2
                            else:
                                # both keyword and value are provided
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                            
                                argumentPair = (queryArgs[0], ">", queryArgs[1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 1
                                

                        elif ("<" in filteredArguments[index]):
                            queryArgs = filteredArguments[index].split("<") # [keyword, value]
                            if (queryArgs[0] == "" and queryArgs[1] == ""):
                                # keyword and value missing so use previous word as keyword, next word as value
                                # check acceptable characters
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, "<", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 2
                            elif (queryArgs[0] == ""):
                                # keyword is missing, so use previous word
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, "<", queryArgs[1])
                                arguments.append(argumentPair)
                                index += 1
                            elif (queryArgs[1] == ""):
                                # value that would applied to the keyword is missing, so use next word
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], "<", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                index += 2
                            else:
                                # both keyword and value are provided
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], "<", queryArgs[1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 1
                                

                        elif ("=" in filteredArguments[index]):
                            queryArgs = filteredArguments[index].split("=") # [keyword, value]
                            if (queryArgs[0] == "" and queryArgs[1] == ""):
                                # keyword and value missing so use previous word as keyword, next word as value
                                # check acceptable characters
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, "=", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 2
                            elif (queryArgs[0] == ""):
                                # keyword is missing, so use previous word
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, "=", queryArgs[1])
                                arguments.append(argumentPair)
                                index += 1
                            elif (queryArgs[1] == ""):
                                # value that would applied to the keyword is missing, so use next word
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], "=", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                index += 2
                            else:
                                # both keyword and value are provided
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], "=", queryArgs[1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 1
                                

                        elif (":" in filteredArguments[index]):
                            queryArgs = filteredArguments[index].split(":") # [keyword, value]
                            if (queryArgs[0] == "" and queryArgs[1] == ""):
                                # keyword and value missing so use previous word as keyword, next word as value
                                # check acceptable characters
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, ":", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 2
                            elif (queryArgs[0] == ""):
                                # keyword is missing, so use previous word
                                if (any((c not in acceptableLetters) for c in previousWord)):
                                    __argStatus = False
                            
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (previousWord, ":", queryArgs[1])
                                arguments.append(argumentPair)
                                index += 1
                            elif (queryArgs[1] == ""):
                                # value that would applied to the keyword is missing, so use next word
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in filteredArguments[index + 1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], ":", filteredArguments[index + 1])
                                arguments.append(argumentPair)
                                index += 2
                            else:
                                # both keyword and value are provided
                                if (any((c not in acceptableLetters) for c in queryArgs[0])):
                                    __argStatus = False
                                
                                if (any((c not in acceptableLetters) for c in queryArgs[1])):
                                    __argStatus = False
                                
                                argumentPair = (queryArgs[0], ":", queryArgs[1])
                                arguments.append(argumentPair)
                                previousWord = None
                                index += 1
                                
                        else:
                            # arg is a potential search word or potential keyword
                            if (previousWord != None):
                                # arg is a search word
                                argumentPair = (previousWord,)
                                arguments.append(argumentPair)
                            # arg is a keyword
                            previousWord = filteredArguments[index]
                            index += 1


                    print(arguments)
                    print(__argStatus,'REEEEEE')
                    print(QueryProgram.__currentOutputFormat)
                    if __argStatus:
                        # arguments are correctly formatted, perform various queries here
                        # other wise return to loop and request a new command
                        self.ParseQueries(arguments)
            def ParseQueries(self, arguments):
                # perform various queries here, based on arguments
                # returns to session loop afterwards
                # check if an exact match or partial match (%)
                # term searches vs keywords

                # determine output format ('full' or 'brief')
                for arg in arguments:
                    if (len(arg) == 3 and arg[0] == "ouput" and arg[1] == "="):
                        # user wants to change the output format
                        if (arg[2] == "full"):
                            QueryProgram.__currentOutputFormat = OutputArgsEnum.full
                        elif (arg[2] == "brief"):
                            QueryProgram.__currentOutputFormat = OutputArgsEnum.brief
                        else:
                            # invalid format argument specified, keep previous format
                            print("invalid format type specified, please use either brief or full: {0}").format(arg[2])



                if (QueryProgram.__currentOutputFormat == OutputArgsEnum.brief):
                    # return all records in a brief format (id and title only)
                    self.EvaluateArgumentsBriefFormat(arguments)
                    pass
                elif (QueryProgram.__currentOutputFormat == OutputArgsEnum.full):
                    # return all records in full format
                    self.EvaluateArgumentsFullFormat(arguments)
                    pass
                else:
                    print("output format is not correct")
    def EvaluateArgumentsBriefFormat(self):
        # print out in brief format
        # paramter: is a list of tuple of two possible formats below [(argument), (argument), (argument), ... , (argument)]
        # (1) argument = (search term)
        # (2) argument = (keyword, operator, value) eg. (bcc, :, brian@gmail.com)
        print(self.__query)
        for arg in:
            if (len(arg) == 1):
                # argument is a search term:::    argument = (search term)
                searchTerm = arg[0]
                #--------------------Perform search term operation on database below------------------------------#

            elif (len(arg) == 3):
                # argument is a search term:::    argument = (keyword, operator, value)
                keyWord = arg[0]
                operator = arg[1]
                value = arg[2]
                #--------------------Perform query operation on database below------------------------------#

            else:
                print("argument has too few or too many indices: argument = {0}").format(arg)

                '''
            

