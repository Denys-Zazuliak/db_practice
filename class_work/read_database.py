import sqlite3

with sqlite3.connect('../database.db') as conn:
    cursor=conn.cursor()

    select_students="""
    SELECT id, firstname, lastname
    FROM students
    WHERE age>=15
    """

    cursor.execute(select_students)
    first_student = cursor.fetchone()
    more_student = cursor.fetchmany(10)
    other_students=cursor.fetchall()
    print(first_student)

    average_query="""
    SELECT avg(age)
    FROM students
    WHERE gender=?
    """
    average_age=cursor.execute(average_query, ('F',)).fetchone()[0]
    print(average_age)

    group_by_query="""
    SELECT gender, avg(age)
    FROM students
    GROUP BY gender
    """
    average_age_by_gender=cursor.execute(group_by_query).fetchall()
    print(average_age_by_gender)