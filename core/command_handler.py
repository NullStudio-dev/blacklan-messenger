import json


class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.commands = {
            "/users": self._users,
            "/msg": self._msg,
            "/nick": self._nick,
            "/ping": self._ping,
            "/status": self._status,
            "/clear": self._clear,
            "/exit": self._exit,
            "/kick": self._kick,
            "/ban": self._ban,
            "/mute": self._mute
        }

    def handle_command(self, command, client_socket, clients, user_session):
        parts = command.split(" ", 1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd in self.commands:
            self.commands[cmd](client_socket, clients, user_session, args)
        else:
            client_socket.sendall((self.server.colors.ERROR + f"Unknown command: {cmd}\n" + self.server.colors.RESET).encode("utf-8"))

    def _users(self, client_socket, clients, user_session, args):
        user_list = ", ".join([session.username for session in self.server.sessions.values()])
        client_socket.sendall(json.dumps({"type": "chat", "message": (self.server.colors.OK + f" Active users: {user_list}\n" + self.server.colors.RESET)}).encode("utf-8"))

    def _msg(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /msg <username> <message>\n" + self.server.colors.RESET).encode("utf-8"))
            return
        
        parts = args.split(" ", 1)
        recipient_username = parts[0]
        message_content = parts[1] if len(parts) > 1 else ""

        found = False
        for sock, session in self.server.sessions.items():
            if session.username == recipient_username:
                try:
                    sock.sendall((self.server.colors.INFO + f"[PM from {user_session.username}] {message_content}\n" + self.server.colors.RESET).encode("utf-8"))
                    client_socket.sendall((self.server.colors.OK + f"Message sent to {recipient_username}\n" + self.server.colors.RESET).encode("utf-8"))
                    found = True
                    break
                except Exception as e:
                    client_socket.sendall((self.server.colors.ERROR + f"Error sending message to {recipient_username}: {e}\n" + self.server.colors.RESET).encode("utf-8"))
                    found = True
                    break
        if not found:
            client_socket.sendall((self.server.colors.ERROR + f"User {recipient_username} not found.\n" + self.server.colors.RESET).encode("utf-8"))

    def _nick(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /nick <new_username>\n" + self.server.colors.RESET).encode("utf-8"))
            return
        
        old_username = user_session.username
        new_username = args.split(" ", 1)[0]

        with self.server.lock:
            # Check if username already exists
            for session in self.server.sessions.values():
                if session.username == new_username:
                    client_socket.sendall((self.server.colors.ERROR + f"Username {new_username} is already taken.\n" + self.server.colors.RESET).encode("utf-8"))
                    return
            
            user_session.username = new_username
            self.server.clients[client_socket] = new_username # Update in clients dict as well
        
        client_socket.sendall((self.server.colors.OK + f"Your username has been changed to {new_username}\n" + self.server.colors.RESET).encode("utf-8"))
        self.server.broadcast_message(f"{self.server.colors.INFO} {old_username} is now known as {new_username}.", sender_socket=client_socket)

    def _ping(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /ping <username>\n" + self.server.colors.RESET).encode("utf-8"))
            return
        
        target_username = args.split(" ", 1)[0]
        found = False
        for sock, session in self.server.sessions.items():
            if session.username == target_username:
                found = True
                # Simulate latency
                import time
                start_time = time.time()
                time.sleep(0.1) # Simulate network delay
                end_time = time.time()
                latency = int((end_time - start_time) * 1000)
                client_socket.sendall((self.server.colors.OK + f"Ping to {target_username}: {latency}ms\n" + self.server.colors.RESET).encode("utf-8"))
                sock.sendall((self.server.colors.INFO + f"{user_session.username} pinged you ({latency}ms)!\n" + self.server.colors.RESET).encode("utf-8"))
                break
        if not found:
            client_socket.sendall((self.server.colors.ERROR + f"User {target_username} not found.\n" + self.server.colors.RESET).encode("utf-8"))

    def _status(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /status [online|away|dnd]\n" + self.server.colors.RESET).encode("utf-8"))
            return
        
        new_status = args.split(" ", 1)[0].lower()
        if user_session.set_status(new_status):
            client_socket.sendall((self.server.colors.OK + f"Your status has been set to {new_status}.\n" + self.server.colors.RESET).encode("utf-8"))
            self.server.broadcast_message(f"{self.server.colors.INFO} {user_session.username} is now {new_status}.", sender_socket=client_socket)
        else:
            client_socket.sendall((self.server.colors.ERROR + "Invalid status. Choose from online, away, or dnd.\n" + self.server.colors.RESET).encode("utf-8"))

    def _clear(self, client_socket, clients, user_session, args):
        # ANSI escape code to clear the terminal screen
        client_socket.sendall(b"\033[2J\033[H")

    def _exit(self, client_socket, clients, user_session, args):
        client_socket.sendall((self.server.colors.INFO + "Exiting...\n" + self.server.colors.RESET).encode("utf-8"))
        client_socket.close()

    def _kick(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /kick <username>\n" + self.server.colors.RESET).encode("utf-8"))
            return

        if user_session.username != "admin": # Simple admin check for now
            client_socket.sendall((self.server.colors.ERROR + "You don\'t have permission to use this command.\n" + self.server.colors.RESET).encode("utf-8"))
            return

        target_username = args.split(" ", 1)[0]
        found = False
        for sock, session in list(self.server.sessions.items()):
            if session.username == target_username:
                try:
                    sock.sendall((self.server.colors.INFO + "You have been kicked from the server.\n" + self.server.colors.RESET).encode("utf-8"))
                    sock.close()
                    with self.server.lock:
                        del self.server.clients[sock]
                        del self.server.sessions[sock]
                    self.server.broadcast_message(f"{self.server.colors.INFO} User {target_username} has been kicked.")
                    client_socket.sendall((self.server.colors.OK + f"User {target_username} kicked successfully.\n" + self.server.colors.RESET).encode("utf-8"))
                    found = True
                    break
                except Exception as e:
                    client_socket.sendall((self.server.colors.ERROR + f"Error kicking user {target_username}: {e}\n" + self.server.colors.RESET).encode("utf-8"))
                    found = True
                    break
        if not found:
            client_socket.sendall((self.server.colors.ERROR + f"User {target_username} not found.\n" + self.server.colors.RESET).encode("utf-8"))

    def _ban(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /ban <username>\n" + self.server.colors.RESET).encode("utf-8"))
            return

        if user_session.username != "admin": # Simple admin check for now
            client_socket.sendall((self.server.colors.ERROR + "You don\'t have permission to use this command.\n" + self.server.colors.RESET).encode("utf-8"))
            return

        target_username = args.split(" ", 1)[0]
        # In a real system, you\'d store banned users (e.g., in a file or database)
        # For now, we\'ll just kick and pretend to ban.
        found = False
        for sock, session in list(self.server.sessions.items()):
            if session.username == target_username:
                try:
                    sock.sendall((self.server.colors.INFO + "You have been banned from the server.\n" + self.server.colors.RESET).encode("utf-8"))
                    sock.close()
                    with self.server.lock:
                        del self.server.clients[sock]
                        del self.server.sessions[sock]
                    self.server.broadcast_message(f"{self.server.colors.INFO} User {target_username} has been banned.")
                    client_socket.sendall((self.server.colors.OK + f"User {target_username} banned successfully.\n" + self.server.colors.RESET).encode("utf-8"))
                    found = True
                    break
                except Exception as e:
                    client_socket.sendall((self.server.colors.ERROR + f"Error banning user {target_username}: {e}\n" + self.server.colors.RESET).encode("utf-8"))
                    found = True
                    break
        if not found:
            client_socket.sendall((self.server.colors.ERROR + f"User {target_username} not found.\n" + self.server.colors.RESET).encode("utf-8"))

    def _mute(self, client_socket, clients, user_session, args):
        if not args:
            client_socket.sendall((self.server.colors.WARNING + "Usage: /mute <username> [duration_minutes]\n" + self.server.colors.RESET).encode("utf-8"))
            return

        if user_session.username != "admin": # Simple admin check for now
            client_socket.sendall((self.server.colors.ERROR + "You don\'t have permission to use this command.\n" + self.server.colors.RESET).encode("utf-8"))
            return

        parts = args.split(" ", 1)
        target_username = parts[0]
        duration = 5 # Default mute duration in minutes
        if len(parts) > 1:
            try:
                duration = int(parts[1])
            except ValueError:
                client_socket.sendall((self.server.colors.ERROR + "Invalid duration. Must be a number.\n" + self.server.colors.RESET).encode("utf-8"))
                return

        found = False
        for sock, session in self.server.sessions.items():
            if session.username == target_username:
                session.mute(duration * 60) # Convert minutes to seconds
                client_socket.sendall((self.server.colors.OK + f"User {target_username} muted for {duration} minutes.\n" + self.server.colors.RESET).encode("utf-8"))
                self.server.broadcast_message(f"{self.server.colors.INFO} User {target_username} has been muted for {duration} minutes.")
                found = True
                break
        if not found:
            client_socket.sendall((self.server.colors.ERROR + f"User {target_username} not found.\n" + self.server.colors.RESET).encode("utf-8"))


