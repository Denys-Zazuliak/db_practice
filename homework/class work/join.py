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

with sqlite3.connect('..\..\sm_app.sqlite') as conn:
    cursor = conn.cursor()

    select_users_posts = """
    SELECT users.id, users.name, posts.description
    FROM posts
    INNER JOIN users ON users.id = posts.user_id
    """

    users_posts=execute_read_query(conn, select_users_posts)

for post in users_posts:
    print(post)

select_user_comment = """
SELECT posts.description as post, comment, name
FROM posts
INNER JOIN comments ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id
"""

with sqlite3.connect('..\..\sm_app.sqlite') as conn:
    comments= execute_read_query(conn, select_user_comment)

for user_comment in comments:
    print(user_comment)