
class OutputFormatsEnum:
    full = "full"
    brief = "brief"


class QueryProgram:
    __currentOutputFormat = OutputFormatsEnum.brief
    __argStatus = True
    # query session
    def startSession():
        # run a loop in the terminal for the user to perform actions
        while True:
            command = input("enter a command")
            arguments = command.split(" ")
            __argStatus = True
            # check if one of the arguments specifies a change in format (output=brief or output=full)
            for arg in arguments:
                if "output=" in arg:
                    newFormat = arg[7:]
                    if newFormat == OutputFormatsEnum.brief:
                        __currentOutputFormat = OutputFormatsEnum.brief
                    elif newFormat = OutputFormatsEnum.full:
                        __currentOutputFormat = OutputFormatsEnum.full
                    else:
                        print("{0} is not a correct argument").format(arg)
                        __argStatus = False

            if __argStatus:
                # arguments are correctly formatted, perform various queries here
                # other wise return to loop and request a new command
                PerformQueries(arguments)

    def PerformQueries(arguments):
        # perform various queries here, based on arguments
        # returns to session loop afterwards
            
