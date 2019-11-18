
class OutputArgsEnum:
    full = "full"
    brief = "brief" # only print out (id) and (title)


class QueryProgram:
    __currentOutputFormat = OutputArgsEnum.brief
    __argStatus = True
    __keywords = ["subj:", "body:", "from:", "to:", "bcc:", "cc:"]
    # query session
    def startSession(self):
        # run a loop in the terminal for the user to perform actions
        while True:
            command = input("enter a command: ")
            command = command.lower()
            arguments = command.split(" ")
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
            while index < len(filteredArguments) and __argStatus:
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


            #print(arguments)
            #print(__argStatus)
            if __argStatus:
                # arguments are correctly formatted, perform various queries here
                # other wise return to loop and request a new command
                ParseQueries(arguments)

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
                    __currentOutputFormat = OutputArgsEnum.full
                elif (arg[2] == "brief"):
                    __currentOutputFormat = OutputArgsEnum.brief
                else:
                    # invalid format argument specified, keep previous format
                    print("invalid format type specified, please use either brief or full: {0}").format(arg[2])



        if (__currentOutputFormat == OutputArgsEnum.brief):
            # return all records in a brief format (id and title only)
            EvaluateArgumentsBriefFormat(arguments)
            pass
        elif (__currentOutputFormat == OutputArgsEnum.full):
            # return all records in full format
            EvaluateArgumentsFullFormat(arguments)
            pass
        else:
            print("output format is not correct")




    def EvaluateArgumentsBriefFormat(self, arguments):
        # print out arguments in brief format
        # paramter: arguments is a list of tuple of two possible formats below [(argument), (argument), (argument), ... , (argument)]
        # (1) argument = (search term)
        # (2) argument = (keyword, operator, value) eg. (bcc, :, brian@gmail.com)
        for arg in arguments:
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
    
    def EvaluateArgumentsFullFormat(self, arguments):
        # print out arguments in full format
        # paramter: arguments is a list of tuple of two possible formats below [(argument), (argument), (argument), ... , (argument)]
        # (1) argument = (search term)
        # (2) argument = (keyword, operator, value) eg. (bcc, :, brian@gmail.com)
        for arg in arguments:
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

