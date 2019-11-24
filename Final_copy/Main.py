
from QueryProgram import QueryProgram
import os,sys
from Create_files import Create_files
from Create_indexes import Create_indexes
if __name__ == '__main__':
    #os.system('python3 ../Phase_1/Create_files.py {}'.format(sys.argv[1]))
    #os.system('python3 ../Phase_2/Create_indexes.py' )
    text_file = input("Create text files (Y/N): ").upper()
    while text_file != 'Y' and text_file != 'N':
        text_file = input("Enter Y or N: ").upper()
    if text_file == 'Y':
        txt = Create_files(sys.argv[1])
        txt.create_file()
    index_file = input("Create index files (Y/N): ").upper()
    while index_file != 'Y' and index_file != 'N':
        index_file = input("Enter Y or N: ").upper()
    if index_file == 'Y':
        txt = Create_indexes()
        txt.create_indexes()
    program = QueryProgram()
    program.startSession()
