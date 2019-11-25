import sys
for item in sys.stdin:
    item = item.replace('\\','')
    key = item[:item.index(':')]
    val = item[item.index(':')+1:]
    sys.stdout.write(key.strip()+'\n')
    sys.stdout.write(val.strip()+'\n')