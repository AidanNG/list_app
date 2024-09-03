#A file to deal with the definition and handling of the entry class to improve entries.

class entry:
    def __init__(self, task, date_init, date_due, tags):
            self.task = task
            self.date_init = date_init
            self.date_due = date_due
            self.tags = tags