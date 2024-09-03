import customtkinter
import pandas as pd

global checkboxes
checkboxes = []
#open csvs into a pandas data frame
active_df = pd.read_csv('Active_Tasks.csv')
closed_df = pd.read_csv('Closed_Tasks.csv')

#autopopulate the checked column
if 'checked' not in active_df.columns:
    active_df['checked'] = False

#frame - defaults
#system, dark, or light
customtkinter.set_appearance_mode("system")
#blue, green, and dark-blue
customtkinter.set_default_color_theme("dark-blue")

#add list
root = customtkinter.CTk()

label = customtkinter.CTkLabel(master=root, text="Checklist", font=("Roboto", 24))
label.pack(pady=12, padx=100)

#functions
def initialize_checkboxes():
    global checkboxes, active_df
    for _, row in active_df.iterrows():
        task_text = row['task']
        is_checked = row['checked']
        checkbox = customtkinter.CTkCheckBox(master=task_frame, text=task_text)
        checkbox.pack(pady=5, padx=10)
        checkbox.select() if is_checked else checkbox.deselect()
        checkboxes.append(checkbox)

def new_entry(entry):
    global active_df
    task_text = entry.get()
    checkbox = customtkinter.CTkCheckBox(master=task_frame, text=entry.get())
    checkbox.pack(pady=5, padx=10)
    checkboxes.append(checkbox)

    new_row = pd.DataFrame({'task': [task_text], 'checked': [False]})
    active_df = pd.concat([active_df, new_row], ignore_index=True)

    active_df.to_csv("Active_Tasks.csv", index=False)

    # Clear the entry field after adding the task
    entry.delete(0, 'end')

def save_checkbox_states():
    global active_df
    for i, checkbox in enumerate(checkboxes):
        active_df.loc[i, 'checked'] = bool(checkbox.get())
    active_df.to_csv("Active_Tasks.csv", index=False)

def delete_entry():
    global active_df, closed_df, checkboxes
    for check in checkboxes[:]:
        if check.get() == 1:
            task_text = check.cget("text")
            check.pack_forget()
            checkboxes.remove(check)
            
            # Move task from active_df to closed_df
            task_row = active_df[active_df['task'] == task_text]
            closed_df = pd.concat([closed_df, task_row], ignore_index=True)
            active_df = active_df[active_df['task'] != task_text]
    
    # Save updated DataFrames
    active_df.to_csv("Active_Tasks.csv", index=False)
    closed_df.to_csv("Closed_Tasks.csv", index=False)


#main script
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

root.protocol("WM_DELETE_WINDOW", lambda: [save_checkbox_states(), root.destroy()])

closed_df.to_csv("Closed_Tasks.csv", index=False)
active_df.to_csv("Active_Tasks.csv", index=False)
root.mainloop()
