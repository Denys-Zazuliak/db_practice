from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Person, Activity, Location

people = [
    Person(first_name="Andrew", last_name="Dales"),
    Person(first_name='Eleanore', last_name='Shiner'),
    Person(first_name='Adam', last_name='Reeves'),
    Person(first_name="Chris", last_name="Brolin"),
    Person(first_name='Vera', last_name="Malcova"),
    ]

location_chess = Location(room='7')
location_fives = Location(room='Fives court')
location_outdoor_ed = Location(room='Fives court')
location_drawing = Location(room='7')

chess = Activity(name="Chess", location=location_chess)
fives = Activity(name="Fives", location=location_fives)
outdoor_ed = Activity(name="Outdoor Ed", location=location_outdoor_ed)
drawing = Activity(name="Drawing", location=location_drawing)

people[0].activities.append(chess)
people[0].activities.append(fives)
people[1].activities.append(outdoor_ed)
people[1].activities.append(drawing)

engine = create_engine('sqlite:///activities.sqlite', echo=True)

with Session(engine) as sess:
    sess.add_all(people)
    sess.commit()
