import customtkinter
import pandas as pd
from entry import Entry
import sys

def list_app():
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

    # Main frame
    main_frame = customtkinter.CTkFrame(master=root)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=main_frame, text="Task Manager", font=("Roboto", 24))
    label.pack(pady=12, padx=100)

    entries = []
    checkboxes = []

    #Grabs text from the text boxes and inserts to list
    def new_entry(entry_widget, due_date_widget, tag_widget):
        #retrieve text
        task = entry_widget.get()
        due_date_str = due_date_widget.get()
        tag = tag_widget.get()
        
        #if the task box is populated, create Entry and add the input text
        if task:
            due_date = pd.to_datetime(due_date_str, errors='coerce') if due_date_str else pd.NaT
            new_entry = Entry(task, due_date=due_date, tag=tag)
            entries.append(new_entry)
            
            #create check box
            checkbox = customtkinter.CTkCheckBox(master=main_frame, text=str(new_entry))
            checkbox.configure(command=lambda e=new_entry, c=checkbox: toggle_completion(e, c))
            checkbox.pack(pady=5, padx=10)
            checkboxes.append(checkbox)
            
            # Clear input fields
            entry_widget.delete(0, 'end')
            due_date_widget.delete(0, 'end')
            tag_widget.delete(0, 'end')
            
            # Update active_df csv
            new_row = pd.DataFrame({
                'task': [new_entry.task],
                'completion_status': [new_entry.completion_status],
                'date_created': [new_entry.date_created],
                'due_date': [new_entry.due_date],
                'tag': [new_entry.tag]
            })
            global active_df
            active_df = pd.concat([active_df, new_row], ignore_index=True)
            active_df.to_csv("Active_Tasks.csv", index=False)
            
            # Update tag frames
            update_tag_frames()

    #function to update dataframes and tag frames based on completion status
    def toggle_completion(entry, checkbox):
        if entry.completion_status:
            entry.uncomplete()
        else:
            entry.complete()
        checkbox.configure(text=str(entry))

        #update dataframes and tag_frames
        update_dataframes()
        update_tag_frames()

    #if a checkbox is checked, on button press, delete all checked boxes and update UI
    def delete_completed():
        global entries, checkboxes
        entries_to_remove = []
        checkboxes_to_remove = []
        
        #collect completed entries and add to closed_df
        for entry, checkbox in zip(entries, checkboxes):
            if entry.completion_status:
                entries_to_remove.append(entry)
                checkboxes_to_remove.append(checkbox)
                checkbox.pack_forget()
                
                # Move to closed_df
                closed_df.loc[len(closed_df)] = [entry.task, entry.completion_status, entry.date_created, entry.due_date, entry.tag]
        
        #remove completed from UI
        for entry in entries_to_remove:
            entries.remove(entry)
        for checkbox in checkboxes_to_remove:
            checkboxes.remove(checkbox)
        
        #update dataframes and tag_frames to reflect changes
        update_dataframes()
        update_tag_frames()

    #Function to update csvs and active_df to reflect actions
    def update_dataframes():
        global active_df, closed_df
        active_df = pd.DataFrame([vars(entry) for entry in entries])
        active_df = active_df[columns]  # Ensure only necessary columns are present
        active_df.to_csv("Active_Tasks.csv", index=False)
        closed_df.to_csv("Closed_Tasks.csv", index=False)

    # Input fields
    task_input = customtkinter.CTkEntry(master=main_frame, placeholder_text="New Task")
    task_input.pack(pady=5, padx=10)

    due_date_input = customtkinter.CTkEntry(master=main_frame, placeholder_text="Due Date")
    due_date_input.pack(pady=5, padx=10)

    tag_input = customtkinter.CTkEntry(master=main_frame, placeholder_text="Tag")
    tag_input.pack(pady=5, padx=10)

    add_button = customtkinter.CTkButton(master=main_frame, text="Add New Task", command=lambda: new_entry(task_input, due_date_input, tag_input))
    add_button.pack(pady=5, padx=10)

    delete_button = customtkinter.CTkButton(master=main_frame, text="Remove Completed Tasks", command=delete_completed)
    delete_button.pack(pady=5, padx=10)

    # Tag frames
    tag_frames = {}
    
    #update tag frames to reflect current list
    def update_tag_frames():
        global tag_frames
        
        # Clear existing tag frames
        for frame in tag_frames.values():
            frame.destroy()
        tag_frames.clear()
        
        # Create new tag frames
        tags = active_df['tag'].unique()
        for i, tag in enumerate(tags):
            if pd.notna(tag) and tag != '':
                tag_frame = customtkinter.CTkFrame(master=root)
                tag_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)
                
                tag_label = customtkinter.CTkLabel(master=tag_frame, text=f"{tag}", font=("Roboto", 18))
                tag_label.pack(pady=5, padx=10)
                
                tag_tasks = active_df[active_df['tag'] == tag]
                for _, row in tag_tasks.iterrows():
                    task_label = customtkinter.CTkLabel(master=tag_frame, text=row['task'])
                    task_label.pack(pady=2, padx=10)
                
                tag_frames[tag] = tag_frame

    # Initialize existing tasks
    for _, row in active_df.iterrows():
        entry = Entry(
            row['task'],
            row['completion_status'],
            pd.to_datetime(row['date_created']) if pd.notna(row['date_created']) else None,
            pd.to_datetime(row['due_date']) if pd.notna(row['due_date']) else None,
            row['tag']
        )
        entries.append(entry)
        checkbox = customtkinter.CTkCheckBox(master=main_frame, text=str(entry))
        checkbox.configure(command=lambda e=entry, c=checkbox: toggle_completion(e, c))
        checkbox.pack(pady=5, padx=10)
        checkboxes.append(checkbox)
        if entry.completion_status:
            checkbox.select()

    # Initial update of tag frames
    update_tag_frames()

    root.mainloop()

def main():
    try:
        list_app()
    except TypeError:
        pass


if __name__ == '__main__':
    try:
        sys.exit(main())
    except TypeError:
        pass