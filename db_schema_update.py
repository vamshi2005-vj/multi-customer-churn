# db_schema_update.py
import sqlite3

conn = sqlite3.connect('churn_app.db')
cursor = conn.cursor()

# Create activity_logs table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_type TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("activity_logs table created/verified.")
