from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model import User, Post

people = [
    User(name="Andrew", age=10, gender="male", nationality="yes"),
    User(name="Denys", age=100, gender="male", nationality="no"),
    ]

post1=Post(title='SQL Project', description='TOI', )

people[1].posts.append(post1)
people[1].liked_posts.append(post1)

engine = create_engine('sqlite:///social_media.sqlite', echo=True)

with Session(engine) as sess:
    sess.add_all(people)
    sess.commit()