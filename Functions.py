import json
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("server/create")
    else:
        print(f"Failed to connect, return code: {rc}")


def on_message(client, userdata, msg, properties=None):
    print(f"{msg.topic}: {msg.payload.decode()}")


def show_frame(frame):
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()


def hide_frame(frame):
    frame.grid_forget()


def save_user_info(username, password):
    with open("info.json", "w") as f:
        user_data = {"username": username,
                     "password": password}
        json.dump(user_data, f)

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
    print("Published message")
