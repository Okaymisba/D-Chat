import json
import tkinter as tk
import paho.mqtt.client as mqtt

from Functions import get_username, add_placeholder, add_placeholder_for_text

chat_name = ""
topic = "application/chatrooms/test"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe("application/create")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg, properties=None):
    global chat_name
    global topic

    chat_room_data = json.loads(msg.payload.decode("utf-8"))
    application_username = get_username()
    if application_username == chat_room_data["username"]:
        chat_name = chat_room_data["recipient"]
        topic = chat_room_data["topic"]
        print(chat_name, topic)


broker = "4dbbebee01cb4916af953cf932ac5313.s1.eu.hivemq.cloud"
port = 8883
username = "Reader"
password = "Reader123"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()


def chat_room(parent):
    chat_room = tk.Frame(parent, width=500, height=700)
    chat_room.grid(row=0, column=0, sticky="nsew")

    message_box = tk.Text(chat_room, wrap="word", font=("Helvetica", 12), width=43, height=3)
    message_box.place(x=10, y=600)
    add_placeholder_for_text(message_box, "Type Your Message Here")

    # temporary solution
    scrollbar = tk.Scrollbar(chat_room, command=message_box.yview)
    scrollbar.place(x=1000, y=600)
    message_box.config(yscrollcommand=scrollbar.set)

    message_display = tk.Text(chat_room, wrap="word", state="disabled", height=32, width=53, font=("Helvetica", 12), bd=0)
    message_display.place(x=10, y=10)


    send_button = tk.Button(chat_room, text="Send", font=("Helvetica", 12), padx=20, pady=17,
                            bd=0, bg="light green", cursor="hand2", relief="solid",
                            activebackground="light green", command=lambda: send_message(topic, message_box, message_display))
    send_button.place(x=407, y=602)


    def add_message(text_message, message):
        text_message.config(state=tk.NORMAL)
        text_message.insert(tk.END, message+ "\n")
        text_message.config(state=tk.DISABLED)
        text_message.see(tk.END)


    def send_message(topic, entry_widget, display_widget):
        message = entry_widget.get("1.0", tk.END).strip()
        if message:
            client.publish(topic, message)
            add_message(display_widget, f"You: {message}")
            entry_widget.delete("1.0", tk.END)
            print(topic)

    return chat_room
