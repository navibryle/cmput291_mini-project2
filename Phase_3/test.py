output_type = input("Enter output type: ").strip().lower()
inp = input("ENTER options:")
while inp != '3' :
    if inp == '1':
        query = input("Enter query: ")
        cur_char = 0
        last_word = None#pointer to where the previous character before the space was
        cur_word = None
        operator = [':','<','=','<=','>=']
        proccessed_query = ''
        while cur_char != len(query)-1:
            if query[cur_char] == ' ' and query[cur_char+1] == ' ':
                cur_char += 1
            elif query[cur_char] == ' ' and (query[cur_char+1] in operator or query[cur_char+1]+query[cur_char+2] in operator):
                if query[cur_char+1] in operator:8
                    proccessed_query += query[cur_char+1]
                    last_word = query[cur_char+1]
                    cur_char+=2
                elif query[cur_char+1]+query[cur_char+2] in operator:
                    proccessed_query += query[cur_char+1]+query[cur_char+2]
                    last_word = query[cur_char+1]+query[cur_char+2]
                    cur_char += 3
            elif query[cur_char] == ' ' and query[cur_char+1] != ' ' and (last_word not in operator):
                proccessed_query += ' '
                cur_char += 1
            elif query[cur_char] != ' ':#query[cur_char] is an alphanumeric-_ character
                proccessed_query += query[cur_char]
                last_word = query[cur_char]
                cur_char += 1
            else:
                cur_char += 1
        elif inp == '2':

        print(proccessed_query.split())