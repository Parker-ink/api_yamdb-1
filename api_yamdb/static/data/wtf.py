import csv

with open('category.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        print(row['first_name'], row['last_name'])
