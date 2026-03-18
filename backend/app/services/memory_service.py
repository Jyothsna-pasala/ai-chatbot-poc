class MemoryService:

    def __init__(self):
        self.sessions = {}

    def add_message(self, session_id, message):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(message)

    def get_history(self, session_id):
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]