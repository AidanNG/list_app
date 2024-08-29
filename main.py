import customtkinter
import csv
import pandas as pd

#open csvs into a pandas data frame
global active_df, closed_df
active_df = pd.read_csv('Active_Tasks.csv')
closed_df = pd.read_csv('Closed_Tasks.csv')

#frame
#system, dark, or light
customtkinter.set_appearance_mode("system")
#blue, green, and dark-blue
customtkinter.set_default_color_theme("dark-blue")

#add list
root = customtkinter.CTk()

label = customtkinter.CTkLabel(master=root, text="Checklist", font=("Roboto", 24))
label.pack(pady=12, padx=100)

def initialize_checkboxes():
    global checkboxes
    checkboxes = []
    for index, row in active_df.iterrows():
        task_text = row['task']
        checkbox = customtkinter.CTkCheckBox(master=task_frame, text=task_text)
        checkbox.pack(pady=5, padx=10)
        checkboxes.append(checkbox)

def new_entry(entry):
    checkbox = customtkinter.CTkCheckBox(master=task_frame, text=entry.get())
    checkbox.pack(pady=5, padx=10)
    checkboxes.append(checkbox)

    new_index = active_df.index.max() + 1 if not active_df.empty else 0
    active_df.loc[new_index, 'task'] = checkbox.cget("text")

    active_df.to_csv("Active_Tasks.csv", index=True)

    # Clear the entry field after adding the task
    entry.delete(0, 'end')

def delete_entry():
    for check in checkboxes[:]:
        if check.get() == 1:
            task_text = check.cget("text")
            check.pack_forget()
            checkboxes.remove(check)
            
            # Remove from active_df and add to closed_df
            active_df = active_df[active_df['task'] != task_text]
            new_index = closed_df.index.max() + 1 if not closed_df.empty else 0
            closed_df.loc[new_index, 'task'] = task_text
    
    # Save updated DataFrames
    active_df.to_csv("Active_Tasks.csv", index=True)
    closed_df.to_csv("Closed_Tasks.csv", index=True)


user_input = customtkinter.StringVar(root)

entry = customtkinter.CTkEntry(master=root, placeholder_text="New Task", textvariable=user_input)
entry.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=root, text="Add New Task", command=lambda : new_entry(entry))
button.pack(pady=5, padx=10)

button = customtkinter.CTkButton(master=root, text="Remove Done Tasks", command=lambda : delete_entry())
button.pack(pady=5, padx=10)

task_frame = customtkinter.CTkFrame(master=root)
task_frame.pack(pady=12, padx=100)
initialize_checkboxes()

closed_df.to_csv("Closed_Tasks.csv", index=True)
active_df.to_csv("Active_Tasks.csv", index=True)
root.mainloop()
task_frame.mainloop()
