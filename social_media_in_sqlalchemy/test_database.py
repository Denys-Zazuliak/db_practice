import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from model import Base, User, Post, Comment, likes
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

test_db_location='sqlite:///test_database_new.db'

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
        qry=sa.select(User).where(User.name == 'Rayhan')
        rayhan=db_session.scalar(qry)
        assert rayhan is not None
        assert rayhan.name == 'Rayhan'
        assert rayhan.age == 16
        assert rayhan.gender == 'male'
        assert rayhan.nationality is None

    def test_invalid_user(self, db_session):
        user=User(age=-12, gender='the game')
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_add_post(self, db_session):
        post=Post(title='Pycharm disaster', description='raycho0809, FuzzyGhost551', user_id=1)
        db_session.add(post)
        db_session.commit()
        qry=sa.select(Post).where(Post.title == 'Pycharm disaster')
        pycharm_disaster=db_session.scalar(qry)
        assert pycharm_disaster.title == 'Pycharm disaster'
        assert pycharm_disaster.description == 'raycho0809, FuzzyGhost551'