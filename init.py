import csv
import os
import subprocess

subprocess.run(["pip", "install", "pandas"]) 
#remove old csvs
os.remove('Active_Tasks.csv')
os.remove('Closed_Tasks.csv')


#insert fresh csvs
with open('Active_Tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ['task']
    writer.writerow(field)

with open('Closed_Tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ['task']
    writer.writerow(field)