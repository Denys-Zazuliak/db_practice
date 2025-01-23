import sqlite3

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"The error {e} occurred")
    return result


select_users = "SELECT * from users"
with sqlite3.connect("../../sm_app.sqlite") as conn:
    users = execute_read_query(conn, select_users)

for user in users:
    print(user)
