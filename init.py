import csv

with open('Active_Tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["task"]
    writer.writerow(field)

with open('Closed_Tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["task"]
    writer.writerow(field)