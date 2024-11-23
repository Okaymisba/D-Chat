import json
import tkinter as tk
from tkinter import messagebox

from Functions import hide_frame, create_chatroom, get_username


def validate_inputs_for_chatroom_creation(username, chat_with, code):
    with open("room.txt", "r") as f:
        room_data = json.load(f)
        for data in room_data:
            print(data[0])
            if chat_with == data[0]:
                messagebox.showerror("Invalid Username", "A chatroom with this user already exists")
                return False

    if not username or ' ' in username:
        messagebox.showerror("Invalid Input", "Username cannot be empty or contain spaces.")
        return False

    if not chat_with or ' ' in chat_with:
        messagebox.showerror("Invalid Input", "Person to chat with cannot be empty or contain spaces.")
        return False

    if not code or ' ' in code:
        messagebox.showerror("Invalid Input", "Code cannot be empty or contain spaces.")
        return False

    return True


def add_chatroom(parent):
    add_chatroom_frame = tk.Frame(parent, width=500, height=700)
    add_chatroom_frame.grid(row=0, column=0, sticky='nsew')

    label_for_username = tk.Label(add_chatroom_frame, text="Username", font=("Helvetica", 15))
    label_for_username.place(x=100, y=70)

    label_for_username_of_the_person_to_chat = tk.Label(add_chatroom_frame,
                                                        text="Enter the username of the person to chat with", fg="red")
    label_for_username_of_the_person_to_chat.place(x=98, y=130)

    input_field_for_person_to_chat_with = tk.Entry(add_chatroom_frame, width=25, font=("Helvetica", 12),
                                                   highlightthickness=2)
    input_field_for_person_to_chat_with.place(x=100, y=100)

    label_for_code = tk.Label(add_chatroom_frame, text="Code", font=("Helvetica", 15))
    label_for_code.place(x=100, y=175)

    input_field_for_code = tk.Entry(add_chatroom_frame, width=25, font=("Helvetica", 12), highlightthickness=2)
    input_field_for_code.place(x=100, y=205)

    label_for_chatroom_code = tk.Label(add_chatroom_frame, text="Enter Unique Code For your chat room", fg="red")
    label_for_chatroom_code.place(x=100, y=235)

    def handle_create_room():
        username = get_username()
        chat_with = input_field_for_person_to_chat_with.get()
        code = input_field_for_code.get()

        if validate_inputs_for_chatroom_creation(username, chat_with, code):
            hide_frame(add_chatroom_frame)
            create_chatroom(username, chat_with, code)

    button_for_creating_room = tk.Button(add_chatroom_frame, text="Create Room", font=("Helvetica", 12), padx=2, pady=2,
                                         bd=0, bg="light green", cursor="hand2", relief="solid",
                                         activebackground="light green",
                                         command=handle_create_room)
    button_for_creating_room.place(x=275, y=300)

    back_button = tk.Button(add_chatroom_frame, text='Back', font=("Helvetica", 12), padx=2, pady=2,
                            bd=0, bg="light green", cursor="hand2", relief="solid",
                            activebackground="light green", command=lambda: hide_frame(add_chatroom_frame))
    back_button.place(x=200, y=300)

    return add_chatroom_frame
