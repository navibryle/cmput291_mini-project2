import sys
for item in sys.stdin:
    item = item.replace('\\','')
    key_val = item.split(':')
    sys.stdout.write(key_val[0].strip()+'\n')
    sys.stdout.write(key_val[1].strip()+'\n')