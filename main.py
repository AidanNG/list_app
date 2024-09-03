import customtkinter
import pandas as pd
from datetime import datetime
from entry import Entry

# Read CSV files
active_df = pd.read_csv('Active_Tasks.csv')
closed_df = pd.read_csv('Closed_Tasks.csv')

# Clean up DataFrames
active_df = active_df.loc[:, ~active_df.columns.str.contains('^Unnamed')]
closed_df = closed_df.loc[:, ~closed_df.columns.str.contains('^Unnamed')]

# Ensure all necessary columns exist
columns = ['task', 'completion_status', 'date_created', 'due_date', 'tag']
for df in [active_df, closed_df]:
    for col in columns:
        if col not in df.columns:
            df[col] = ''
    df['completion_status'] = df['completion_status'].astype(bool)
    df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
    df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')

# Save cleaned DataFrames
active_df.to_csv("Active_Tasks.csv", index=False)
closed_df.to_csv("Closed_Tasks.csv", index=False)

# GUI setup
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Task Manager")

label = customtkinter.CTkLabel(master=root, text="Task Manager", font=("Roboto", 24))
label.pack(pady=12, padx=100)

entries = []
checkboxes = []

def new_entry(entry_widget, due_date_widget, tag_widget):
    task = entry_widget.get()
    due_date_str = due_date_widget.get()
    tag = tag_widget.get()
    
    if task:
        due_date = pd.to_datetime(due_date_str, errors='coerce') if due_date_str else pd.NaT
        new_entry = Entry(task, due_date=due_date, tag=tag)
        entries.append(new_entry)
        
        checkbox = customtkinter.CTkCheckBox(master=root, text=str(new_entry))
        checkbox.configure(command=lambda e=new_entry, c=checkbox: toggle_completion(e, c))
        checkbox.pack(pady=5, padx=10)
        checkboxes.append(checkbox)
        
        # Clear input fields
        entry_widget.delete(0, 'end')
        due_date_widget.delete(0, 'end')
        tag_widget.delete(0, 'end')
        
        # Update active_df
        active_df.loc[len(active_df)] = [new_entry.task, new_entry.completion_status, new_entry.date_created, new_entry.due_date, new_entry.tag]
        active_df.to_csv("Active_Tasks.csv", index=False)

def toggle_completion(entry, checkbox):
    if entry.completion_status:
        entry.uncomplete()
    else:
        entry.complete()
    checkbox.configure(text=str(entry))
    update_dataframes()

def delete_completed():
    global entries, checkboxes
    entries_to_remove = []
    checkboxes_to_remove = []
    
    for entry, checkbox in zip(entries, checkboxes):
        if entry.completion_status:
            entries_to_remove.append(entry)
            checkboxes_to_remove.append(checkbox)
            checkbox.pack_forget()
            
            # Move to closed_df
            closed_df.loc[len(closed_df)] = [entry.task, entry.completion_status, entry.date_created, entry.due_date, entry.tag]
    
    for entry in entries_to_remove:
        entries.remove(entry)
    for checkbox in checkboxes_to_remove:
        checkboxes.remove(checkbox)
    
    update_dataframes()

def update_dataframes():
    global active_df, closed_df
    active_df = pd.DataFrame([vars(entry) for entry in entries])
    active_df.to_csv("Active_Tasks.csv", index=False)
    closed_df.to_csv("Closed_Tasks.csv", index=False)

# Input fields
task_input = customtkinter.CTkEntry(master=root, placeholder_text="New Task")
task_input.pack(pady=5, padx=10)

due_date_input = customtkinter.CTkEntry(master=root, placeholder_text="Due Date (YYYY-MM-DD)")
due_date_input.pack(pady=5, padx=10)

tag_input = customtkinter.CTkEntry(master=root, placeholder_text="Tag")
tag_input.pack(pady=5, padx=10)

add_button = customtkinter.CTkButton(master=root, text="Add New Task", command=lambda: new_entry(task_input, due_date_input, tag_input))
add_button.pack(pady=5, padx=10)

delete_button = customtkinter.CTkButton(master=root, text="Remove Completed Tasks", command=delete_completed)
delete_button.pack(pady=5, padx=10)

# Initialize existing tasks
for _, row in active_df.iterrows():
    entry = Entry(
        row['task'],
        row['completion_status'],
        row['date_created'] if pd.notna(row['date_created']) else None,
        row['due_date'] if pd.notna(row['due_date']) else None,
        row['tag']
    )
    entries.append(entry)
    checkbox = customtkinter.CTkCheckBox(master=root, text=str(entry))
    checkbox.configure(command=lambda e=entry, c=checkbox: toggle_completion(e, c))
    checkbox.pack(pady=5, padx=10)
    checkboxes.append(checkbox)
    if entry.completion_status:
        checkbox.select()

root.mainloop()
