from db.db import initializeConnection

try:
    conn = initializeConnection()
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")