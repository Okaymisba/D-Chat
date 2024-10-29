import tkinter as tk

from Functions import show_frame
from chat_room import chat_room


def chat_list_frame(parent, add_chatroom_frame):
    chat_list_page = tk.Frame(parent, width=500, height=700)
    chat_list_page.grid(row=0, column=0, sticky="nsew")
    canvas = tk.Canvas(chat_list_page)
    scrollbar = tk.Scrollbar(chat_list_page, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    add_button = tk.Button(canvas, text="+", font=("Helvetica", 15), bg="light green", width=5, bd=0, cursor="hand2",
                           relief="solid", activebackground="light green",
                           command=lambda: show_frame(add_chatroom_frame))
    add_button.place(x=400, y=625)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Function to create a chat box dynamically
    def create_chat_box(parent, chat_name, chat_room_frame):
        chat_frame = tk.Frame(scrollable_frame, bg="lightgray", padx=190, pady=5)
        chat_label = tk.Label(chat_frame, text=chat_name, font=("Arial", 12), bg="lightgray")

        chat_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        chat_frame.pack(fill=tk.X, padx=5, pady=2)

        chat_frame.bind("<Button-1>", lambda e: show_frame(chat_room_frame))

    return chat_list_page, create_chat_box
