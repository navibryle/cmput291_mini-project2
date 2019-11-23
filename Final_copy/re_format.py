import sys
for item in sys.stdin:
    cut_off = item.index(':')
    print(item[:cut_off])
    print(item[cut_off+1:].strip())