import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from model import Base, User, Post, Comment, likes
from sqlalchemy.exc import IntegrityError

from social_media_in_sqlalchemy.write_to_social_media import session

test_db_location='sqlite:///test.db'

def test_test():
    assert 3**2==9

class TestDataBase:
    @pytest.fixture(scope='class')

    def db_session(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        session = so.Session(engine)
        yield session
        session.close()
        Base.metadata.drop_all(engine)

    def test_valid_user(self, db_session):
        user=User(name='Rayhan', age=16, gender='male')
        db_session.add(user)
        db_session.commit()
        qry=sa.select([User]).where(User.name=='Rayhan')
        rayhan=db_session.scalar(qry)
        assert rayhan is not None
        assert rayhan.name == 'Rayhan'
        assert rayhan.age == 16
        assert rayhan.gender == 'male'
        assert rayhan.nationality is None



