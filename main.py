import json
import os
import tkinter as tk

import paho.mqtt.client as mqtt

from Add_chatroom import add_chatroom
from Functions import show_frame, get_username, add_to_room_data
from chat_list_page import chat_list_frame
from page1 import page1

root = tk.Tk()
root.geometry("500x700")
root.title("D Chat")
root.resizable(False, False)

add_chatroom_frame = add_chatroom(root)
chat_list_frame, create_chat_room = chat_list_frame(root, add_chatroom_frame)
page1_frame = page1(root, chat_list_frame)

file_for_user_credentials = "info.json"
file_for_room_data = "room.txt"
room_data = []

if os.path.exists(file_for_user_credentials):
    show_frame(chat_list_frame)

    if os.path.exists(file_for_room_data):
        with open(file_for_room_data, 'r') as f:
            room_data = json.load(f)

            for data in room_data:
                create_chat_room(root, data[0], data[1])
else:
    show_frame(page1_frame)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe("application/create")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg, properties=None):
    chat_room_data = json.loads(msg.payload.decode("utf-8"))
    application_username = get_username()
    if application_username == chat_room_data["username"]:
        room_information = [chat_room_data["recipient"], chat_room_data["topic"]]
        add_to_room_data(room_data, room_information)
        create_chat_room(root, chat_room_data["recipient"], chat_room_data["topic"])
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
