import sqlite3

DATABASE = 'churn_app.db'

def create_activity_logs_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')
    
    conn.commit()
    conn.close()
    print("activity_logs table created successfully!")

if __name__ == "__main__":
    create_activity_logs_table()
