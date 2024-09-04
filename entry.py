#A file to deal with the definition and handling of the entry class to improve entries.
from datetime import datetime 
import pandas as pd

#Entry Class definition
class Entry:
    def __init__(self, task, completion_status=False, date_created=None, due_date=None, tag=None):
        self.task = task
        self.completion_status = completion_status
        self.date_created = date_created if date_created else datetime.now()
        self.due_date = due_date  # Keep this as a string
        self.tag = tag

    #simple setter/toggle functions for ease of use
    def complete(self):
        self.completion_status = True

    def uncomplete(self):
        self.completion_status = False

    def set_due_date(self, due_date):
        self.due_date = due_date

    def set_tag(self, tag):
        self.tag = tag

    #Checkbox text appearance
    def __str__(self):
        status = "Completed" if self.completion_status else "Not Completed"
        created = f"Created: {self.date_created.strftime('%Y-%m-%d')}" if pd.notna(self.date_created) else "Created: N/A"
        due_date = f", Due: {self.due_date}" if self.due_date else ", Due: EOD"
        return f"{self.task} ({status}, {created}{due_date})" 