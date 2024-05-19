import sqlite3

class ToDoDatabase:
    def __init__(self, db_name='todo_list.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task TEXT NOT NULL,
                    deadline TEXT,
                    priority TEXT,
                    category TEXT
                )
            """)

    def add_task(self, task, deadline, priority, category):
        with self.connection:
            self.connection.execute("""
                INSERT INTO tasks (task, deadline, priority, category)
                VALUES (?, ?, ?, ?)
            """, (task, deadline, priority, category))

    def remove_task(self, task_id):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def update_task(self, task_id, task, deadline, priority, category):
        with self.connection:
            self.connection.execute("""
                UPDATE tasks
                SET task = ?, deadline = ?, priority = ?, category = ?
                WHERE id = ?
            """, (task, deadline, priority, category, task_id))

    def list_tasks(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM tasks").fetchall()

    def get_task(self, task_id):
        with self.connection:
            return self.connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
