import json
import tkinter as tk
import paho.mqtt.client as mqtt

from Functions import get_username, add_placeholder

chat_name = ""
topic = ""


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

    message_box = tk.Text(chat_room, wrap="word", font=("Helvetica", 15), highlightthickness=2, width=37, height=3)
    message_box.place(x=10, y=600)
    # add_placeholder(message_box, "Enter Your Message Here")

    # temporary solution
    scrollbar = tk.Scrollbar(chat_room, command=message_box.yview)
    scrollbar.place(x=1000, y=600)  # Position scrollbar to the right of the text widget
    message_box.config(yscrollcommand=scrollbar.set)

    return chat_room
