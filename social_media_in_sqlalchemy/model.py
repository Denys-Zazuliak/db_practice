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
    id: so.Mapped[int] = so.mapped_column(primary_key=True,autoincrement=True)
    name: so.Mapped[Optional[str]]
    age: so.Mapped[Optional[int]]
    gender: so.Mapped[Optional[str]]
    nationality: so.Mapped[Optional[str]]
    posts: so.Mapped[list[posts]] = so.relationship("Post", secondary=likes)
    liked_posts: so.Mapped[list[posts]] = so.relationship("Liked_Post", secondary=likes)

    def __repr__(self) -> str:
        return f"User(name='{self.name}')"

class Post(Base):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str]
    description: so.Mapped[str]
    user: so.Mapped[list[User]] = so.relationship("User", secondary=User)
    liked_by_users: so.Mapped[list[User]] = so.relationship("User", secondary=likes, order_by="User.id")
    #comments: so.Mapped[str]

    def __repr__(self) -> str:
        return f"Post(title='{self.title}')"