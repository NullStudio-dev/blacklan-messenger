import time

class UserSession:
    def __init__(self, username, client_socket):
        self.username = username
        self.client_socket = client_socket
        self.status = "online"
        self.join_time = time.time()
        self.is_muted = False
        self.mute_until = 0

    def mute(self, duration):
        self.is_muted = True
        self.mute_until = time.time() + duration

    def unmute(self):
        if self.is_muted and time.time() > self.mute_until:
            self.is_muted = False
            self.mute_until = 0

    def is_currently_muted(self):
        if self.is_muted and time.time() > self.mute_until:
            self.unmute()
        return self.is_muted

    def set_status(self, status):
        valid_statuses = ["online", "away", "dnd"]
        if status in valid_statuses:
            self.status = status
            return True
        return False

