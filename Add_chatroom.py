import tkinter as tk

from Functions import hide_frame


def add_chatroom(parent):
    add_chatroom_frame = tk.Frame(parent, width=500, height=700)
    add_chatroom_frame.grid(row=0, column=0, sticky='nsew')

    label_for_username = tk.Label(add_chatroom_frame, text="Username", font=("Helvetica", 15))
    label_for_username.place(x=100, y=70)

    label_for_username_of_the_person_to_chat = tk.Label(add_chatroom_frame,
                                                        text="Enter the username of the person to chat with", fg="red")
    label_for_username_of_the_person_to_chat.place(x=98, y=130)

    input_field_for_person_to_chat_with = tk.Entry(add_chatroom_frame, width=25, font=("Helvetica", 15),
                                                   highlightthickness=2)
    input_field_for_person_to_chat_with.place(x=100, y=100)

    label_for_code = tk.Label(add_chatroom_frame, text="Code", font=("Helvetica", 15))
    label_for_code.place(x=100, y=175)

    input_field_for_code = tk.Entry(add_chatroom_frame, width=25, font=("Helvetica", 15), highlightthickness=2)
    input_field_for_code.place(x=100, y=205)

    test = tk.Button(add_chatroom_frame, text='Back', command=lambda: hide_frame(add_chatroom_frame))
    test.grid(row=0, column=0, sticky='nsew')

    return add_chatroom_frame
