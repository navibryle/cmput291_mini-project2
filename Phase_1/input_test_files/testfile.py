file1 = open('1k-terms.txt')
file2 = open('../../Phase_2/terms.txt')
line1 = sorted(file1.readlines())
line2 = sorted(file2.readlines())
#This will test if files are correct
#will be deleted before submission
for item in line1:
    if item not in line2:
        print(item)
