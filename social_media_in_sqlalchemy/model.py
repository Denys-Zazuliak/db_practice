from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

class Base(so.DeclarativeBase):
    pass

likes = sa.Table("likes",
                             Base.metadata,
                             sa.Column("id", sa.Integer,primary_key=True,autoincrement=True),
                             sa.Column("post_id",sa.ForeignKey("posts.id",)),
                             sa.Column("user_id",sa.ForeignKey("users.id"),),
                             sa.UniqueConstraint("post_id","user_id")
                             )

class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(unique=True)
    age: so.Mapped[int]
    gender: so.Mapped[str|None]
    nationality: so.Mapped[str|None]
    posts: so.Mapped[list['Post']] = so.relationship(back_populates='user')
    liked_posts: so.Mapped[list['Post']] = so.relationship(secondary=likes, back_populates='liked_by_users')
    comments_made: so.Mapped[list['Comment']] = so.relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"User(name='{self.name}')"

class Post(Base):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str]
    description: so.Mapped[str]
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    user: so.Mapped["User"] = so.relationship(back_populates='posts')
    liked_by_users: so.Mapped[list["User"]] = so.relationship(secondary=likes, back_populates='liked_posts')
    comments: so.Mapped[list["Comment"]] = so.relationship(back_populates='post')

    def __repr__(self) -> str:
        return f"Post(title='{self.title}')"

class Comment(Base):
    __tablename__ = 'comments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('posts.id'))
    comment: so.Mapped[str]
    post: so.Mapped['Post'] = so.relationship(back_populates='comments')
    user: so.Mapped['User'] = so.relationship(back_populates='comments_made')

    def __repr__(self):
        return f"Comment(user_id={self.user_id}, post_id={self.post_id}, comment='{self.comment}')"