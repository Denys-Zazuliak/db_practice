from sqlalchemy import create_engine
from model import Base

engine = create_engine('sqlite:///social_media.sqlite', echo=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)