import json
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox

import paho.mqtt.client as mqtt

from Functions import save_user_info_on_database_for_signup, save_user_info_on_device, show_frame, add_placeholder, \
    add_placeholder_for_password, authenticate_user_for_login, get_username


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg):
    message_payload = json.loads(msg.payload.decode("utf-8"))

    if msg.topic == "application/signup":
        if message_payload["identity"] == random_digit_for_signup:
            print(message_payload)
            global mqtt_message_data_for_signup, mqtt_message_received_for_signup
            mqtt_message_received_for_signup = True
            mqtt_message_data_for_signup = json.loads(msg.payload.decode("utf-8"))

    if msg.topic == "application/login":
        if message_payload["identity"] == random_digit_for_login:
            print(message_payload)
            global mqtt_message_data_for_login, mqtt_message_received_for_login
            mqtt_message_received_for_login = True
            mqtt_message_data_for_login = json.loads(msg.payload.decode("utf-8"))


mqtt_message_received_for_signup = False
mqtt_message_data_for_signup = None
mqtt_message_received_for_login = False
mqtt_message_data_for_login = None
random_digit_for_signup = random.randint(0, 100000)
random_digit_for_login = random.randint(0, 100000)

broker = "4dbbebee01cb4916af953cf932ac5313.s1.eu.hivemq.cloud"
port = 8883
topic1 = "application/signup"
topic2 = "application/login"
username = "Reader"
password = "Reader123"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()

client.subscribe(topic1)
client.subscribe(topic2)


def validate_inputs(username, password):
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

    button_for_login = tk.Button(page1, text="Login", font=("Helvetica", 15), padx=10, pady=10,
                                 width=10,
                                 bd=0, bg="light gray", fg="black", command=lambda: page2(parent, chat_list_frame))
    button_for_login.place(x=140, y=75)

    button_for_signup = tk.Button(page1, text="Signup", font=("Helvetica", 15), padx=10, pady=10, relief="raised",
                                  width=10,
                                  bd=0, bg="light green", fg="black", cursor="hand2")
    button_for_signup.place(x=265, y=75)

    enter_username_label = tk.Label(page1, text="Username", font=("Helvetica", 15))
    enter_username_label.place(x=75, y=200)

    input_field_for_username = tk.Entry(page1, font=("Helvetica", 15), highlightthickness=2)
    input_field_for_username.place(x=200, y=200)
    add_placeholder(input_field_for_username, "Enter Username here")

    enter_password_label = tk.Label(page1, text="Password", font=("Helvetica", 15))
    enter_password_label.place(x=75, y=250)

    input_field_for_password = tk.Entry(page1, font=("Helvetica", 15), show="*", highlightthickness=2)
    input_field_for_password.place(x=200, y=250)
    add_placeholder_for_password(input_field_for_password, "Enter Password here")

    def handle_signup():
        username = input_field_for_username.get()
        password = input_field_for_password.get()

        if validate_inputs(username, password):
            save_user_info_on_database_for_signup(input_field_for_username.get(), input_field_for_password.get(),
                                                  random_digit_for_signup)
            submit_button.config(state="disabled", text="Signing Up...")

            threading.Thread(target=loading_credentials_for_signup, args=(username, password)).start()

    def loading_credentials_for_signup(username, password):
        global mqtt_message_data_for_signup, mqtt_message_received_for_signup

        for _ in range(50):
            if mqtt_message_received_for_signup:
                break
            time.sleep(0.1)

        if mqtt_message_received_for_signup:
            if mqtt_message_data_for_signup and mqtt_message_data_for_signup.get("user_taken") == "True":
                messagebox.showerror("Login Error", "Username Already Taken")
            else:
                save_user_info_on_device(input_field_for_username.get(), input_field_for_password.get())
                show_frame(chat_list_frame)
        else:
            messagebox.showerror("Error", "Failed to connect, Please try again")

        mqtt_message_received_for_signup = False
        mqtt_message_data_for_signup = None

        submit_button.config(state="normal", text="Sign Up")

    submit_button = tk.Button(page1, text="Sign Up", font=("Helvetica", 10), padx=10, pady=10, relief="raised",
                              width=10,
                              bd=0, bg="light green", fg="black", cursor="hand2", command=handle_signup)
    submit_button.place(x=325, y=350)

    return page1


def page2(parent, chat_list_frame):  # Login Page
    page2 = tk.Frame(parent, width=500, height=700)
    page2.grid(row=0, column=0, sticky='nsew')

    button_for_login = tk.Button(page2, text="Login", font=("Helvetica", 15), padx=10, pady=10,
                                 width=10,
                                 bd=0, bg="light green", fg="black")
    button_for_login.place(x=140, y=75)

    button_for_signup = tk.Button(page2, text="Signup", font=("Helvetica", 15), padx=10, pady=10, relief="raised",
                                  width=10,
                                  bd=0, bg="light gray", fg="black", cursor="hand2",
                                  command=lambda: page1(parent, chat_list_frame))
    button_for_signup.place(x=265, y=75)

    enter_username_label = tk.Label(page2, text="Username", font=("Helvetica", 15))
    enter_username_label.place(x=75, y=200)

    input_field_for_username = tk.Entry(page2, font=("Helvetica", 15), highlightthickness=2)
    input_field_for_username.place(x=200, y=200)
    add_placeholder(input_field_for_username, "Enter Username here")

    enter_password_label = tk.Label(page2, text="Password", font=("Helvetica", 15))
    enter_password_label.place(x=75, y=250)

    input_field_for_password = tk.Entry(page2, font=("Helvetica", 15), show="*", highlightthickness=2)
    input_field_for_password.place(x=200, y=250)
    add_placeholder_for_password(input_field_for_password, "Enter Password here")

    def handle_login():
        username = input_field_for_username.get()
        password = input_field_for_password.get()

        if validate_inputs(username, password):
            authenticate_user_for_login(input_field_for_username.get(), input_field_for_password.get(),
                                        random_digit_for_login)
            submit_button.config(state="disabled", text="logging in...")

            threading.Thread(target=loading_credentials_for_login, args=(username, password)).start()

    def loading_credentials_for_login(username, password):
        global mqtt_message_data_for_login, mqtt_message_received_for_login

        for _ in range(50):
            if mqtt_message_received_for_login:
                break
            time.sleep(0.1)

        if mqtt_message_received_for_login:
            if mqtt_message_data_for_login and mqtt_message_data_for_login.get('success') == False:
                messagebox.showerror("Login Error", "Incorrect Username or Password")
                print("success")
            else:
                save_user_info_on_device(input_field_for_username.get(), input_field_for_password.get())
                show_frame(chat_list_frame)
        else:
            messagebox.showerror("Error", "Failed to connect, Please try again")

        mqtt_message_received_for_login = False
        mqtt_message_data_for_login = None

        submit_button.config(state="normal", text="login")

    submit_button = tk.Button(page2, text="login", font=("Helvetica", 10), padx=10, pady=10, relief="raised", width=10,
                              bd=0, bg="light green", fg="black", cursor="hand2", command=handle_login)
    submit_button.place(x=325, y=350)

    return page2
