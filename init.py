import csv
import os
import subprocess

#install pandas
subprocess.run(["pip", "install", "pandas"]) 

#remove old csvs
os.remove('Active_Tasks.csv')
os.remove('Closed_Tasks.csv')


#insert fresh csvs

#active_df
with open('Active_Tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    #insert fields
    field = ['task','completion_status','date_created','due_date','tag']
    writer.writerow(field)

#closed_df
with open('Closed_Tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    #insert fields
    field = ['task','completion_status','date_created','due_date','tag']
    writer.writerow(field)

