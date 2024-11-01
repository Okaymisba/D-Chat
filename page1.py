import tkinter as tk
from tkinter import messagebox

from Functions import save_user_info, show_frame, add_placeholder, add_placeholder_for_password


def validate_inputs_for_login(username, password):
    if not username or ' ' in username:
        messagebox.showerror("Invalid Input", "Username cannot be empty or contain spaces")
        return False
    if not password or ' ' in password:
        messagebox.showerror("Invalid Input", "Password cannot be empty or contain spaces")
        return False
    return True


def page1(parent, chat_list_frame):
    page1 = tk.Frame(parent, width=500, height=700)
    page1.grid(row=0, column=0, sticky='nsew')

    enter_username_label = tk.Label(page1, text="Username", font=("Helvetica", 15))
    enter_username_label.place(x=75, y=200)

    input_field_for_username = tk.Entry(page1, font=("Helvetica", 12), highlightthickness=2)
    input_field_for_username.place(x=200, y=200)
    add_placeholder(input_field_for_username, "Enter Username here")

    enter_password_label = tk.Label(page1, text="Password", font=("Helvetica", 15))
    enter_password_label.place(x=75, y=250)

    input_field_for_password = tk.Entry(page1, font=("Helvetica", 12), show="*", highlightthickness=2)
    input_field_for_password.place(x=200, y=250)
    add_placeholder_for_password(input_field_for_password, "Enter Password here")

    def handle_login():
        username = input_field_for_username.get()
        password = input_field_for_password.get()

        if validate_inputs_for_login(username, password):
            save_user_info(input_field_for_username.get(), input_field_for_password.get())
            show_frame(chat_list_frame)

    submit_button = tk.Button(page1, text="Submit", font=("Helvetica", 10), padx=10, pady=10, relief="raised", width=10,
                              bd=0, bg="light green", fg="black", cursor="hand2", command=handle_login)
    submit_button.place(x=225, y=350)

    return page1
