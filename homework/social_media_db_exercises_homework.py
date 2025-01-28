import sqlite3


with sqlite3.connect('..\sm_app.sqlite') as conn:
    cursor=conn.cursor()

    questions="""
    SELECT comment
    FROM comments
    WHERE comment LIKE '%?';
    """

    print(cursor.execute(questions).fetchall())

    update="""
    UPDATE users
    SET name='Lizzy'
    WHERE name='Elizabeth';
    """

    cursor.execute(update)

    post_count="""
    SELECT users.name, COUNT(posts.user_id)
    FROM users, posts
    WHERE users.id=posts.user_id
    GROUP BY users.name
    """

    print(cursor.execute(post_count).fetchall())

    user_comments="""
    SELECT users.name, comments.comment
    FROM users, comments
    WHERE users.id=comments.user_id
    GROUP BY users.name
    """

    print(cursor.execute(user_comments).fetchall())

    conn.commit()