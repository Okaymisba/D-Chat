import json
import os
import tkinter as tk
import paho.mqtt.client as mqtt

from Add_chatroom import add_chatroom
from Functions import show_frame, get_username
from chat_list_page import chat_list_frame
from chat_room import chat_room
from page1 import page1

root = tk.Tk()
root.geometry("500x700")
root.title("D Chat")
root.resizable(False, False)

chat_room_frame = chat_room(root)
add_chatroom_frame = add_chatroom(root)
chat_list_frame, create_chat_room = chat_list_frame(root, add_chatroom_frame)
page1_frame = page1(root, chat_list_frame)

file = "info.json"

if os.path.exists(file):
    show_frame(chat_list_frame)
else:
    show_frame(page1_frame)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe("application/create")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg, properties=None):
    global chat_room_frame
    chat_room_data = json.loads(msg.payload.decode("utf-8"))
    application_username = get_username()
    if application_username == chat_room_data["username"]:
        create_chat_room(root, chat_room_data["recipient"], chat_room_frame)
    print(chat_room_data)


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

root.mainloop()
