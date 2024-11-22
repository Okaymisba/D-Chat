import json
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox

import paho.mqtt.client as mqtt

from Functions import save_user_info_on_database, save_user_info_on_device, show_frame, add_placeholder, \
    add_placeholder_for_password


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg):
    message_payload = json.loads(msg.payload.decode("utf-8"))

    if message_payload["identity"] == random_digit:
        print(message_payload)
        global mqtt_message_data, mqtt_message_received
        mqtt_message_received = True
        mqtt_message_data = json.loads(msg.payload.decode("utf-8"))


mqtt_message_received = False
mqtt_message_data = None
random_digit = random.randint(0, 100000)

broker = "4dbbebee01cb4916af953cf932ac5313.s1.eu.hivemq.cloud"
port = 8883
topic = "application/login"
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


def validate_inputs_for_login(username, password):
    if not username or ' ' in username:
        messagebox.showerror("Invalid Input", "Username cannot be empty or contain spaces")
        return False
    if not password or ' ' in password:
        messagebox.showerror("Invalid Input", "Password cannot be empty or contain spaces")
        return False
    return True


def page1(parent, chat_list_frame):
    page1 = tk.Frame(parent, width=500, height=700)
    page1.grid(row=0, column=0, sticky='nsew')

    enter_username_label = tk.Label(page1, text="Username", font=("Helvetica", 15))
    enter_username_label.place(x=75, y=200)

    input_field_for_username = tk.Entry(page1, font=("Helvetica", 12), highlightthickness=2)
    input_field_for_username.place(x=200, y=200)
    add_placeholder(input_field_for_username, "Enter Username here")

    enter_password_label = tk.Label(page1, text="Password", font=("Helvetica", 15))
    enter_password_label.place(x=75, y=250)

    input_field_for_password = tk.Entry(page1, font=("Helvetica", 12), show="*", highlightthickness=2)
    input_field_for_password.place(x=200, y=250)
    add_placeholder_for_password(input_field_for_password, "Enter Password here")

    def handle_login():
        username = input_field_for_username.get()
        password = input_field_for_password.get()

        if validate_inputs_for_login(username, password):
            save_user_info_on_database(input_field_for_username.get(), input_field_for_password.get(), random_digit)
            submit_button.config(state="disabled", text="Submitting...")

            threading.Thread(target=loading_credentials, args=(username, password)).start()

    def loading_credentials(username, password):
        global mqtt_message_data, mqtt_message_received

        for _ in range(50):
            if mqtt_message_received:
                break
            time.sleep(0.1)

        if mqtt_message_received:
            if mqtt_message_data and mqtt_message_data.get("user_taken") == "True":
                messagebox.showerror("Login Error", "Username Already Taken")
            else:
                save_user_info_on_device(input_field_for_username.get(), input_field_for_password.get())
                show_frame(chat_list_frame)
        else:
            messagebox.showerror("Error", "Failed to connect, Please try again")

        mqtt_message_received = False
        mqtt_message_data = None

        submit_button.config(state="normal", text="Submit")

    submit_button = tk.Button(page1, text="Submit", font=("Helvetica", 10), padx=10, pady=10, relief="raised", width=10,
                              bd=0, bg="light green", fg="black", cursor="hand2", command=handle_login)
    submit_button.place(x=225, y=350)

    return page1
