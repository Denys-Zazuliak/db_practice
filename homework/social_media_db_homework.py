import sqlite3


with sqlite3.connect('..\sm_app.sqlite') as conn:
    cursor=conn.cursor()

    # select
    retrieving_fields1="""
    SELECT title, description
    FROM posts;
    """

    cursor.execute(retrieving_fields1)
    print(cursor.fetchall())

    retrieving_fields2 = """
    SELECT title, description
    FROM posts
    WHERE title LIKE 'H%';
    """

    cursor.execute(retrieving_fields2)
    print(cursor.fetchall())

    retrieving_fields3 = """
    SELECT comment, user_id
    FROM comments
    ORDER BY user_id;
    """

    cursor.execute(retrieving_fields3)
    print(cursor.fetchall())



    #update
    update="""
    UPDATE posts
    SET description = "The weather has become pleasant now"
    WHERE id = 2
    """

    cursor.execute(update)


    #group by
    group_by="""
    SELECT description as Post, COUNT(likes.id) as Likes
    FROM likes, posts
    WHERE posts.id = likes.post_id
    GROUP BY likes.post_id
    """

    cursor.execute(group_by)
    print(cursor.fetchall())


    #joins
    join1="""
    SELECT users.name, posts.description
    FROM users INNER JOIN posts ON users.id = posts.user_id
    ORDER BY users.name
    """

    cursor.execute(join1)
    print(cursor.fetchall())

    join2="""
    SELECT users.name, posts.description
    FROM users LEFT JOIN posts ON users.id = posts.user_id
    ORDER BY users.name
    """

    cursor.execute(join2)
    print(cursor.fetchall())

    conn.commit()
