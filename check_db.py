import sqlite3

try:
    conn = sqlite3.connect('churn_app.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Rows in {table_name}: {count}")

    conn.close()

except Exception as e:
    print("Error:", e)
