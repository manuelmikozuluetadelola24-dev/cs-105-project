from db.connection import get_connection

try:
    conn = get_connection()
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")