import sqlite3

# Connect to your database file (it will create if not exists)
conn = sqlite3.connect('churn_app.db')

# Open and read your schema.sql file
with open('schema.sql', 'r') as f:
    sql_script = f.read()

# Run all SQL commands in schema.sql (this will create tables)
conn.executescript(sql_script)

conn.commit()
conn.close()

print("Database tables created successfully!")
