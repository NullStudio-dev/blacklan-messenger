class MessageRouter:
    def __init__(self):
        pass

    def route_message(self, message, clients, sender_socket):
        # This is a placeholder. In a real system, you'd parse the message
        # and decide where to send it (e.g., broadcast, private message, command).
        # For now, we'll just broadcast.
        self.broadcast_message(message, clients, sender_socket)

    def broadcast_message(self, message, clients, sender_socket=None):
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode("utf-8"))
                except:
                    # Handle disconnected client
                    pass


