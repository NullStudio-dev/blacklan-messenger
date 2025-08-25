import socket
import threading
import json
import sys
import os

from config.settings import *
from utils.colors import Colors
from utils.animation import Animation
from utils.encryption import xor_encrypt_decrypt

colors = Colors()
animation = Animation()

class Client:
    def __init__(self, host=HOST, port=PORT, buffer_size=BUFFER_SIZE):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def connect(self):
        try:
            animation.spinner(message=f"{colors.INFO} Connecting to {self.host}:{self.port}")
            self.client_socket.connect((self.host, self.port))
            print(f"{colors.OK} Connected successfully.")

            # Handle initial prompt for username
            initial_data = json.loads(self.client_socket.recv(self.buffer_size).decode("utf-8"))
            if initial_data.get("type") == "prompt":
                prompt_message = initial_data.get("message")
                self.username = input(prompt_message)
                self.client_socket.sendall(json.dumps({"username": self.username}).encode("utf-8"))
                print(f"{colors.INFO} Logged in as {self.username}")

            threading.Thread(target=self.receive_messages).start()
            self.send_messages()
        except ConnectionRefusedError:
            print(f"{colors.ERROR} Connection refused. Make sure the server is running.")
        except Exception as e:
            print(f"{colors.ERROR} Client error: {e}")
        finally:
            self.client_socket.close()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(self.buffer_size).decode("utf-8")
                if not data:
                    print(f"{colors.INFO} Disconnected from server.")
                    break
                message_data = json.loads(data)
                if message_data.get("type") == "chat":
                    print(message_data.get("message"))
            except Exception as e:
                print(f"{colors.ERROR} Error receiving message: {e}")
                break

    def send_messages(self):
        while True:
            try:
                message = input("\n >>>")
                if message.startswith("/"):
                    self.client_socket.sendall(json.dumps({"type": "command", "content": message}).encode("utf-8"))
                else:
                    encrypted_message = xor_encrypt_decrypt(message, ENCRYPTION_KEY)
                    self.client_socket.sendall(json.dumps({"type": "chat", "content": encrypted_message}).encode("utf-8"))
            except Exception as e:
                print(f"{colors.ERROR} Error sending message: {e}")
                break

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LAN Messenger Client")
    parser.add_argument("--host", default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=PORT, help="Server port")
    args = parser.parse_args()

    # Load settings from config/settings.json
    import json
    with open("config/settings.json", "r") as f:
        settings = json.load(f)
    ENCRYPTION_KEY = settings.get("ENCRYPTION_KEY", "default_key")

    client = Client(args.host, args.port, BUFFER_SIZE)
    client.connect()