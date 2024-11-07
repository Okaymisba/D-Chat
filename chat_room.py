import json
import tkinter as tk
import paho.mqtt.client as mqtt

from Functions import get_username, add_placeholder_for_text, hide_frame

chat_rooms = {}


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe("#")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg, properties=None):
    message = json.loads(msg.payload.decode("utf-8"))
    print(message)
    try:
        if message["topic"] in chat_rooms and message["to"] == get_username():
            display_widget = chat_rooms[msg.topic]["display"]
            add_message_for_sender(display_widget, message["message"])
            print(message)
    except KeyError:
        print("Nothing to worry")


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


def chat_room(parent, topic, recipient_name):
    chat_room = tk.Frame(parent, width=500, height=700)
    chat_room.grid(row=0, column=0, sticky="nsew")

    message_box = tk.Text(chat_room, wrap="word", font=("Helvetica", 12), width=43, height=3)
    message_box.place(x=10, y=600)
    add_placeholder_for_text(message_box, "Type Your Message Here")

    # temporary solution
    scrollbar = tk.Scrollbar(chat_room, command=message_box.yview)
    scrollbar.place(x=1000, y=600)
    message_box.config(yscrollcommand=scrollbar.set)

    message_display = tk.Text(chat_room, wrap="word", state="disabled", height=32, width=53, font=("Helvetica", 12),
                              bd=0)
    message_display.place(x=10, y=10)

    chat_rooms[topic] = {"frame": chat_room, "display": message_display}

    back_button = tk.Button(chat_room, text="Back", command=lambda: hide_frame(chat_room))
    back_button.place(x=0, y=0)

    send_button = tk.Button(chat_room, text="Send", font=("Helvetica", 12), padx=20, pady=17,
                            bd=0, bg="light green", cursor="hand2", relief="solid",
                            activebackground="light green",
                            command=lambda: send_message(topic, message_box, message_display, recipient_name))
    send_button.place(x=407, y=602)

    return chat_room


def add_message_for_sender(text_widget, message):
    text_widget.tag_configure("sender", justify="left", background="#e6e6e6", foreground="black", spacing3=5)
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, "\n " + message + "\n", "sender")
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)


def add_message_for_me(text_message, message):
    text_message.tag_configure("me", justify="right", background="#dcf8c6", foreground="black", spacing3=5)
    text_message.config(state=tk.NORMAL)
    text_message.insert(tk.END, "\n " + message + "\n ", "me")
    text_message.config(state=tk.DISABLED)
    text_message.see(tk.END)


def send_message(topic, entry_widget, display_widget, recipient):
    message = entry_widget.get("1.0", tk.END).strip()
    if message:
        json_message = {
            "topic": topic,
            "message": message,
            "to": recipient
        }
        client.publish(topic, json.dumps(json_message))
        add_message_for_me(display_widget, f"You: {message}")
        entry_widget.delete("1.0", tk.END)
        print(topic)
