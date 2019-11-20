import os,sys
for item in sys.stdin:
    cut_off = item.index(':')
    #sys.stdout.write(item[:cut_off]+'\n'+item[cut_off+1:]+'\n')
    print(item[:cut_off])
    print(item[cut_off+1:].strip())