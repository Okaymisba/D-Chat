import json
import paho.mqtt.client as mqtt
import tkinter as tk


def get_username():
    with open("info.json", 'r') as read_file:
        info = json.load(read_file)
        username = info['username']
        return username


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg, properties=None):
    print(f"{msg.topic}: {msg.payload.decode()}")


def show_frame(frame):
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()


def hide_frame(frame):
    frame.grid_forget()


def save_user_info_on_device(username, password):
    with open("info.json", "w") as f:
        user_data = {"username": username,
                     "password": password}
        json.dump(user_data, f)


def save_user_info_on_database_for_signup(username, password, identity):
    user_data = {"identity": identity,
                 "username": username,
                 "password": password}

    broker = "4dbbebee01cb4916af953cf932ac5313.s1.eu.hivemq.cloud"
    port = 8883
    topic = "server/signup"
    username = "Reader"
    password = "Reader123"

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.username_pw_set(username, password)
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_start()

    client.subscribe(topic)

    client.publish(topic, json.dumps(user_data))


def authenticate_user_for_login(username, password, identity):
    user_data = {"identity": identity,
                 "username": username,
                 "password": password}

    broker = "4dbbebee01cb4916af953cf932ac5313.s1.eu.hivemq.cloud"
    port = 8883
    topic = "server/login"
    username = "Reader"
    password = "Reader123"

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.username_pw_set(username, password)
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_start()

    client.subscribe(topic)

    client.publish(topic, json.dumps(user_data))


def create_chatroom(username, recipient_username, chatroom_code):
    recipient = recipient_username
    code = chatroom_code
    data = {
        "username": username,
        "recipient": recipient,
        "code": code
    }

    broker = "4dbbebee01cb4916af953cf932ac5313.s1.eu.hivemq.cloud"
    port = 8883
    topic = "server/create"
    username = "Reader"
    password = "Reader123"

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.username_pw_set(username, password)
    client.tls_set()
    client.on_connect = on_connect_for_create_chatroom
    client.on_message = on_message_for_create_chatroom
    client.connect(broker, port)
    client.loop_start()

    client.subscribe(topic)

    client.publish(topic, json.dumps(data))
    print(f"Data Published: {data}")


def on_connect_for_create_chatroom(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message_for_create_chatroom(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")


def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def add_placeholder_for_password(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="grey", show="")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black", show="*")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey", show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def add_placeholder_for_text(text_widget, placeholder_text):
    text_widget.insert("1.0", placeholder_text)
    text_widget.config(fg="grey")

    def on_focus_in(event):
        if text_widget.get("1.0", "end-1c") == placeholder_text:
            text_widget.delete("1.0", "end")
            text_widget.config(fg="black")

    def on_focus_out(event):
        if text_widget.get("1.0", "end-1c") == "":
            text_widget.insert("1.0", placeholder_text)
            text_widget.config(fg="grey")

    text_widget.bind("<FocusIn>", on_focus_in)
    text_widget.bind("<FocusOut>", on_focus_out)


def add_to_room_data(room_data, list_to_add):
    room_data.append(list_to_add)

    with open("room.txt", "w") as file:
        file.write(json.dumps(room_data))
