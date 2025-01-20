import sqlite3

from faker import Faker
import random

fake = Faker('en_GB')

#conn=sqlite3.connect('student.sqlite')

with sqlite3.connect('database.db') as conn:
    cursor=conn.cursor()

#    create_students_table="""
#    CREATE TABLE IF NOT EXISTS students(
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        firstname TEXT NOT NULL,
#        lastname TEXT NOT NULL,
#        age INTEGER,
#        gender TEXT);
#    """
#    cursor.execute(create_students_table)

#    insert_query="""
#    INSERT INTO students(firstname, lastname, age, gender)
#    VALUES ('Milan','Gal',17,'M'),
#    ('Rayhan','Chowdhury',16,'M'),
#    ('Eleanore','Shiner',16,'F'),
#    ('Adam','Reeves',16,'M'),
#    ('Sami','Hafezjee',16,'M');
#    """
#    cursor.execute(insert_query)

#    parameterised_insert_query="""
#    INSERT INTO students (firstname, lastname, age, gender)
#    VALUES (?, ?, ?, ?);
#    """
    #cursor.execute(parameterised_insert_query, ('Ethan','Levy', 16, 'M'))

#    fake.random.seed(6082008)
#    random.seed(6082008)
#    for _ in range(10):
#        f_name=fake.first_name()
#        l_name=fake.last_name()
#        age=random.randint(16,17)
#        gender=random.choice(('M','F'))
#        cursor.execute(parameterised_insert_query,(f_name,l_name,age,gender))

#    data=[(fake.first_name(),
#           fake.last_name(),
#           random.randint(16,17),
#           random.choice(('M','F')))
#          for _ in range(5)]
#    cursor.executemany(parameterised_insert_query, data)

#    update_query="""
#    UPDATE students
#    SET lastname = ?
#    WHERE id = 4;
#    """
#    cursor.execute(update_query, ('Smith',))

    increment_age_query="""
    UPDATE students
    SET age=age+1;
    """
    cursor.execute(increment_age_query)



    conn.commit()

#conn.close()