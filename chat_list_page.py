import tkinter as tk

from Functions import show_frame
from chat_room import chat_room


def chat_list_frame(parent, add_chatroom_frame):
    chat_list_page = tk.Frame(parent, width=500, height=700)
    chat_list_page.grid(row=0, column=0, sticky="nsew")

    app_label = tk.Label(chat_list_page, text="D-Chat", font=("Helvetica", 20, "bold"), fg="Black", pady=10)
    app_label.pack(side="top", fill="x")

    canvas = tk.Canvas(chat_list_page, width=500)
    scrollbar = tk.Scrollbar(chat_list_page, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    add_button = tk.Button(canvas, text="+", font=("Helvetica", 15), bg="light green", width=5, bd=1, cursor="hand2",
                           relief="solid", activebackground="light green",
                           command=lambda: show_frame(add_chatroom_frame))
    add_button.place(x=400, y=575)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def create_chat_box(parent, chat_name, topic):
        chat = chat_room(parent, topic, chat_name)

        y_position = len(scrollable_frame.winfo_children()) * 55

        chat_frame = tk.Frame(scrollable_frame, bg="light green", height=50, width=490)
        chat_frame.grid(row=y_position, column=0, sticky="ew", padx=3, pady=3)

        chat_label = tk.Label(chat_frame, text=chat_name, font=("Arial", 15), bg="light green", anchor="w")
        chat_label.place(x=10, y=15)

        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        chat_frame.bind("<Button-1>", lambda e: show_frame(chat))

    return chat_list_page, create_chat_box
