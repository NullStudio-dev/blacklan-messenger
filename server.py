import socket
import threading
import json
import os

from config.settings import *
from utils.logger import Logger
from utils.colors import Colors
from utils.encryption import xor_encrypt_decrypt
from core.user_session import UserSession
from core.command_handler import CommandHandler

# Initialize logger and colors
logger = Logger()
colors = Colors()

class Server:
    def __init__(self, host=HOST, port=PORT, buffer_size=BUFFER_SIZE):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.sessions = {}
        self.lock = threading.Lock()
        self.colors = Colors()
        self.command_handler = CommandHandler(self)

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            logger.info(f"{self.colors.INFO} Server listening on {self.host}:{self.port}")
            while True:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"{self.colors.INFO} Accepted connection from {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            logger.error(f"{self.colors.ERROR} Server error: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            # Prompt for username
            client_socket.sendall(json.dumps({"type": "prompt", "message": "Enter your username: "}).encode("utf-8"))
            username_data = client_socket.recv(self.buffer_size).decode("utf-8")
            username = json.loads(username_data).get("username", "Anonymous")

            with self.lock:
                self.clients[client_socket] = username
                self.sessions[client_socket] = UserSession(username, client_socket)
            
            logger.info(f"{self.colors.INFO} User {username} has joined.")
            self.broadcast_message(f"{self.colors.INFO} User {username} has joined the chat.")

            while True:
                message = client_socket.recv(self.buffer_size).decode("utf-8")
                if not message:
                    break
                
                data = json.loads(message)
                msg_type = data.get("type")
                content = data.get("content")

                if msg_type == "chat":
                    decrypted_content = xor_encrypt_decrypt(content, ENCRYPTION_KEY)
                    full_message = f"[{username}] {decrypted_content}"
                    logger.info(full_message)
                    self.broadcast_message(full_message, sender_socket=client_socket)
                elif msg_type == "command":
                    self.command_handler.handle_command(content, client_socket, self.clients, self.sessions[client_socket])

        except Exception as e:
            logger.error(f"{self.colors.ERROR} Client error ({self.clients.get(client_socket, 'Unknown')}): {e}")
        finally:
            with self.lock:
                username = self.clients.pop(client_socket, "Unknown")
                self.sessions.pop(client_socket, None)
            client_socket.close()
            logger.info(f"{self.colors.INFO} User {username} has left.")
            self.broadcast_message(f"{self.colors.INFO} User {username} has left the chat.")

    def broadcast_message(self, message, sender_socket=None):
        with self.lock:
            for client_socket, username in list(self.clients.items()):
                if client_socket != sender_socket:
                    try:
                        client_socket.sendall(json.dumps({"type": "chat", "message": message}).encode("utf-8"))
                    except Exception as e:
                        logger.error(f"{self.colors.ERROR} Error broadcasting to {username}: {e}")
                        # Consider removing disconnected client here

if __name__ == "__main__":
    # Create config/settings.py if it doesn't exist
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.py')
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write("HOST = '0.0.0.0'\n")
            f.write("PORT = 4654\n")
            f.write("BUFFER_SIZE = 4096\n")

    # Load settings from config/settings.py
    from config.settings import HOST, PORT, BUFFER_SIZE
    import json
    with open('config/settings.json', 'r') as f:
        settings = json.load(f)
    ENCRYPTION_KEY = settings.get('ENCRYPTION_KEY', 'default_key')

    server = Server(HOST, PORT, BUFFER_SIZE)
    server.start()