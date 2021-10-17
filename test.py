import csv

item_list = list()

with open('itemswithcatalognumber.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        item_list.append(row[0])


print(item_list)