import customtkinter

#frame
#system, dark, or light
customtkinter.set_appearance_mode("system")
#blue, green, and dark-blue
customtkinter.set_default_color_theme("dark-blue")

#add list
root = customtkinter.CTk()

label = customtkinter.CTkLabel(master=root, text="Checklist", font=("Roboto", 24))
label.pack(pady=12, padx=100)

def new_entry(entry):
    checkbox = customtkinter.CTkCheckBox(master=root, text=entry.get())
    checkbox.pack(pady=12, padx=10)

user_input = customtkinter.StringVar(root)

entry = customtkinter.CTkEntry(master=root, placeholder_text="New Task", textvariable=user_input)
entry.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=root, text="Add New Task", command=lambda : new_entry(entry))
button.pack(pady=12, padx=10)

root.mainloop()