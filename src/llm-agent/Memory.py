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
                if 'user' in entry and 'agent' in entry
            ]
        )

def save_to_database(memory, db_path):
    """
    対話履歴と使用したツールをSQLiteデータベースに保存
    :param memory: ConversationMemoryオブジェクト
    :param db_path: 保存するSQLiteデータベースのパス
    """
    # データベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        agent_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # データを挿入
    for entry in memory.history:
        cursor.execute("""
        INSERT INTO conversation_history (user_input, agent_response)
        VALUES (?, ?)
        """, (entry["user"], entry["agent"]))

    # コミットして接続を閉じる
    conn.commit()
    conn.close()
