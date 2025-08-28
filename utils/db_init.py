import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('../churn_app.db')

employees = [
    (1201, 'raghu', 'raghu@gmail.com', generate_password_hash('raghu')),
    (1202, 'shiva', 'shiva@gmail.com', generate_password_hash('shiva')),
    (1205, 'harsha', 'harsha@gmail.com', generate_password_hash('harsha')),
    (1213, 'arunchand', 'arunchand@gmail.com', generate_password_hash('arunchand')),
    (1220, 'lucky', 'lucky@gmail.com', generate_password_hash('lucky')),
]

admins = [
    (1224, 'vamshi', 'vamshijakkali2005@gmail.com', generate_password_hash('vamshi')),
    (1236, 'pranay', 'pranay@gmail.com', generate_password_hash('pranay')),
]

conn.execute("DELETE FROM employees")
conn.execute("DELETE FROM admins")

conn.executemany("INSERT INTO employees (id, name, email, password) VALUES (?, ?, ?, ?)", employees)
conn.executemany("INSERT INTO admins (id, name, email, password) VALUES (?, ?, ?, ?)", admins)

conn.commit()
conn.close()
print("Inserted employee and admin records successfully.")
