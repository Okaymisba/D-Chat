import tkinter as tk

from Functions import save_user_info, show_frame


def page1(parent, chat_list_frame):
    page1 = tk.Frame(parent, width=500, height=700)
    page1.grid(row=0, column=0, sticky='nsew')

    enter_username_label = tk.Label(page1, text="Username", font=("Helvetica", 15))
    enter_username_label.place(x=75, y=200)

    input_field_for_username = tk.Entry(page1, font=("Helvetica", 15), highlightthickness=2)
    input_field_for_username.place(x=200, y=200)

    enter_password_label = tk.Label(page1, text="Password", font=("Helvetica", 15))
    enter_password_label.place(x=75, y=250)

    input_field_for_password = tk.Entry(page1, font=("Helvetica", 15), show="*", highlightthickness=2)
    input_field_for_password.place(x=200, y=250)

    submit_button = tk.Button(page1, text="Submit", font=("Helvetica", 10), padx=10, pady=10, relief="raised", width=10,
                              bd=0, bg="light green", fg="black", cursor="hand2", command=lambda: [
            save_user_info(input_field_for_username.get(), input_field_for_password.get()),
            show_frame(chat_list_frame)])
    submit_button.place(x=225, y=350)

    return page1
