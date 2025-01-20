import sqlite3

with sqlite3.connect('database.db') as conn:
    cursor=conn.cursor()

    #7
    j_firstname="""
    SELECT firstname
    FROM students
    WHERE firstname LIKE 'J%'
    """
    names=cursor.execute(j_firstname).fetchmany(5)
    print(names)

    #8
    gender_group="""
    SELECT gender
    FROM students
    """
    student_gender=cursor.execute(gender_group).fetchall()
    print(f'Male: {student_gender.count(('M',))}, Female: {student_gender.count(('F',))}')

    #9
    age_sum="""
    SELECT substring(firstname, 1,1), SUM(age)
    FROM students
    GROUP BY substring(firstname, 1,1) 
    """
    sum_age=cursor.execute(age_sum).fetchall()
    print(sum_age)