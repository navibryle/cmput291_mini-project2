with open('../Final_copy/terms.txt') as test:
    line1 = test.readlines()
with open('input_test_files/1k-terms.txt') as test2:
    line2 = test2.readlines()
for item in line1:
    if item not in line2:
        print(item)