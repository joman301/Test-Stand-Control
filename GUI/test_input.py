import random
from time import sleep
import csv


file = 'test.csv'
t = 0
p1 = 0
p2 = 0
p3 = 0
p4 = 0
p5 = 0
p6 = 0
p7 = 0
p8 = 0
p9 = 0
row = []

with open('test.csv', 'a', newline='') as my_csv_file:
    csv_writter = csv.writer(my_csv_file)
    i = 0
    while True:
        row = [t, p1, p2, p3, p4, p5, p6, p7, p8, p9]
        csv_writter.writerow(row)
        my_csv_file.flush()

        # writing the data rows

        t += 1
        p1 = str(round(random.uniform(100, 300), 2))
        p2 = str(round(random.uniform(100, 300), 2))
        p3 = str(round(random.uniform(100, 300), 2))
        p4 = str(round(random.uniform(100, 300), 2))
        p5 = str(round(random.uniform(100, 300), 2))
        p6 = str(round(random.uniform(100, 300), 2))
        p7 = str(round(random.uniform(100, 300), 2))
        p8 = str(round(random.uniform(100, 300), 2))
        p9 = str(round(random.uniform(100, 300), 2))
        sleep(0.25)
