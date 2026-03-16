import sqlite3
class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, user_input, agent_response):
        self.history.append({"user": user_input, "agent": agent_response})

    def get_history(self):
        return "\n".join(
            [
                f"User: {entry['user']}\nAgent: {entry['agent']}"
                for entry in self.history
                if "user" in entry and "agent" in entry
            ]
        )
    
def save_to_database(memory, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            agent_response TEXT
        )
    ''')
    for entry in memory.history:
        c.execute('''
            INSERT INTO conversations (user_input, agent_response)
            VALUES (?, ?)
        ''', (entry['user'], entry['agent']))
    conn.commit()
    conn.close()