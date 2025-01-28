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

with sqlite3.connect('..\..\sm_app.sqlite') as connection:

    select_post_likes = """
    SELECT description as Post, COUNT(likes.id) as Likes
    FROM likes, posts
    WHERE posts.id = likes.post_id
    GROUP BY likes.post_id
    """

    post_likes = execute_read_query(connection, select_post_likes)

for post_like in post_likes:
    print(post_like)