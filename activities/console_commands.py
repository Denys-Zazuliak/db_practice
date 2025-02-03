from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sqlalchemy as sa
from models import Person, Activity

engine = create_engine('sqlite:///activities.sqlite', echo=True)
sess = Session(engine)