import csv
with open("home/azamat/Desktop/netology-home-work/open and read any format/novosty.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        print(type(row))