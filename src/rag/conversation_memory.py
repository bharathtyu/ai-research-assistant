from datetime import datetime


class ConversationMemory:

    def __init__(self):
        self.history = []

    def add_message(self, question, answer):
        self.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "answer": answer
        })

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history.clear()


memory = ConversationMemory()