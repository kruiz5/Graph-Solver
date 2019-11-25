import csv

A = input('Enter your name: ')
A = int(A.strip())

path = [(1,2),(3,4),(5,6)]
header = 'path_1'
with open('output_test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([header])
    writer.writerows(path)

