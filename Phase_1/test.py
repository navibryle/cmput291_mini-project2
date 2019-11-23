file1  = open('Phase_1/input_test_files/1k-emails.txt')
file2 = open('Phase_2/emails.txt')
line1 = file1.readlines()
line2 = file2.readlines()
for item in line1:
    if item in line2:
        continue
    else:
        print(item)
    