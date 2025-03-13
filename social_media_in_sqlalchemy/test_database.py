from os import write

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from social_media_in_sqlalchemy.write_to_social_media import write_initial_data
from social_media_in_sqlalchemy.controller import Controller
from social_media_in_sqlalchemy.model import Base, User, Post, Comment, likes


test_db_location='sqlite:///test_database.db'

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
        print(rayhan.id)
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
        db_session.rollback()

    def test_comment(self, db_session):
        comment=Comment(user_id=1, post_id=6, comment='among us')
        db_session.add(comment)
        db_session.commit()
        qry=sa.select(Comment).where(Comment.user_id == 1)
        among_us= db_session.scalar(qry)
        assert among_us.comment == 'among us'
        assert among_us.user_id == 1
        assert among_us.post_id == 6
        db_session.rollback()

    def test_likes(self, db_session):
        pass

class TestController:
    @pytest.fixture(scope='class', autouse=True)
    def test_db(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        write_initial_data(engine)
        yield
        # After the fixture is used drop the data from the database
        Base.metadata.drop_all(engine)

    @pytest.fixture(scope='class')
    def controller(self):
        control = Controller(db_location=test_db_location)
        return control

    def test_set_current_user_from_name(self, controller):
        controller.set_current_user_from_name('Alice')
        assert controller.current_user.name == 'Alice'
        assert controller.current_user.id == 1
        assert controller.current_user.age == 30

    def test_get_user_names(self):
        mylist=controller.get_user_names()
        assert mylist[0] == 'Alice'
        assert len(mylist) == 4

    def test_create_user(self):
        user=controller.create_user(name='KSI', age=100, gender='male', nationality='British')
        assert user.name == 'KSI'
        assert user.age == 100
        assert user.gender == 'male'
        assert user.nationality == 'British'

    def test_get_posts(self):
        posts=controller.get_posts()
        assert posts[0]['title'] == 'Exploring the Rocky Mountains'
        assert posts[1]['description'] == 'Sharing some of my favorite recipes, including a delicious chocolate cake and a savory lasagna.'


    def test_create_post(self):
        assert False

    def test_choose_post(self):
        assert False

    def test_get_comments(self):
        assert False