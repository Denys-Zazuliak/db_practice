import sqlalchemy as sa
import sqlalchemy.orm as so
import pyinputplus as pyip

from social_media_in_sqlalchemy.model import User, Post, Comment, likes

class Controller:
    def __init__(self, db_location='sqlite:///social_media.db'):
        self.current_user = None
        self.engine = sa.create_engine(db_location)

    def set_current_user_from_name(self, name):
        with so.Session(bind=self.engine) as session:
            self.current_user = session.scalars(sa.select(User).where(User.name == name)).one_or_none()

    def get_user_names(self) -> list[str]:
        with so.Session(bind=self.engine) as session:
            user_names = session.scalars(sa.select(User.name).order_by(User.name)).all()
        return list(user_names)

    def create_user(self, name: str, age: int, gender: str, nationality: str) -> User:
        with so.Session(bind=self.engine) as session:
            user = User(name=name, age=age, gender=gender, nationality=nationality)
            session.add(user)
            session.commit()
            self.current_user = user
        return user

    def get_posts(self, user_name: str) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            user = session.scalars(sa.select(User).where(User.name == user_name)).one_or_none()
            posts_info = [{'id': post.id,
                           'title': post.title,
                           'description': post.description,
                           'number_likes': len(post.liked_by_users),
                           }
                          for post in user.posts]
        return posts_info

    def create_post(self, title: str, description: str, ) -> Post:
        with so.Session(bind=self.engine) as session:
            post = Post(title=title, description=description, user_id=self.current_user.id)
            session.add(post)
            session.commit()
        return post

    def choose_post(self):
        users = self.get_user_names()

        user_name = pyip.inputMenu(users,
                                   prompt="Select a user:\n",
                                   numbered=True,
                                   )

        print(f"{user_name}'s Posts")

        posts = self.get_posts(user_name)

        post_options = [f"{post['title']} (Likes: {post['number_likes']})" for post in posts]
        post_ids = [post["id"] for post in posts]


        post_index = pyip.inputMenu(post_options,
                                    prompt="Select a post:\n",
                                    numbered=True,
                                    )
        post_id = post_ids[post_options.index(post_index)]

        return post_id

    def get_comments(self, post_id: str) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            post = session.scalars(sa.select(Post).where(Post.id == post_id)).one_or_none()
            comments_info = [{'id': comment.id,
                           'user_id': comment.user_id,
                           'post_id': comment.post_id,
                           'comment': comment.comment,
                           }
                           for comment in post.comments]
        return comments_info

    def create_comment(self, post_id, comment):
        with so.Session(bind=self.engine) as session:
            comment = Comment(user_id=self.current_user.id, post_id=post_id, comment=comment)
            session.add(comment)
            session.commit()
        return comment

    def like(self, post_id):
        with so.Session(bind=self.engine) as session:
            post = session.scalars(sa.select(Post).where(Post.id == post_id)).one_or_none()
            user=self.current_user
            if post and user not in post.liked_by_users:
                post.liked_by_users.append(user)
                session.commit()
            else:
                post.liked_by_users.remove(user)
                session.commit()


class CLI:
    def __init__(self):
        self.controller = Controller()
        self.login()

    @staticmethod
    def show_title(title):
        print('\n' + title)
        print('-' * len(title) + '\n')

    def login(self):
        self.show_title('Login Screen')
        users = self.controller.get_user_names()
        menu_items = users + ['Create a new account',
                              'Exit',
                              ]
        menu_choice = pyip.inputMenu(menu_items,
                                     prompt='Select user or create a new account\n',
                                     numbered=True,
                                     )
        if menu_choice.lower() == 'create a new account':
            self.create_account()
        elif menu_choice.lower() == 'exit':
            print('Goodbye')
        else:
            user_name = menu_choice
            self.controller.set_current_user_from_name(user_name)
            self.user_home()

    def create_account(self, existing_users=None):
        self.show_title('Create Account Screen')
        print('Enter Account Details')
        user_name = pyip.inputStr('Username: ', blockRegexes=existing_users, strip=None)
        age = pyip.inputInt('Age: ', min=0, max=150, blank=True)
        gender = pyip.inputMenu(['male', 'female', 'other'], prompt='Gender: ', blank=True)
        nationality = pyip.inputStr('Nationality: ')
        self.controller.create_user(user_name, age, gender, nationality)
        self.login()

    def user_home(self):
        self.show_title(f'{self.controller.current_user.name} Home Screen')
        print(f'Name: {self.controller.current_user.name}')
        print(f'Age: {self.controller.current_user.age}')
        print(f'Nationality: {self.controller.current_user.nationality}')
        self.show_posts(self.controller.current_user.name)

        menu_items = {'Show posts from another user': self.show_posts,
                      'Create a post': self.create_post,
                      'Create a comment': self.create_comments,
                      #'Like the post': self.likes,
                      'Logout': self.login,
                      }

        menu_choice = pyip.inputMenu(list(menu_items.keys()),
                                     prompt='Select an action\n',
                                     numbered=True,
                                     )
        menu_items[menu_choice]()
        if menu_choice != 'Logout':
            self.user_home()

    def show_posts(self, user_name: [str] = None):
        if user_name is None:
            users = self.controller.get_user_names()
            menu_choice = pyip.inputMenu(users,
                                         prompt='Select a user\n',
                                         numbered=True,
                                         )
            user_name = menu_choice

        self.show_title(f"{user_name}'s Posts")
        posts = self.controller.get_posts(user_name)
        for post in posts:
            print(f'Title: {post["title"]}')
            print(f'Content: {post["description"]}')
            print(f'Likes: {post["number_likes"]}')

            self.show_comments(post)

        if not posts:
            print('No Posts')

    def create_post(self):
        user_name = self.controller.current_user.name

        title = pyip.inputStr('Title: ')
        description = pyip.inputStr('Description: ')

        self.controller.create_post(user_name, title, description)


    def show_comments(self, post):
        comments=self.controller.get_comments(post['id'])
        for comment in comments:
            print(f'Comment: {comment["comment"]}')

    def create_comments(self):
        post_id = self.controller.choose_post()
        comment = input("Enter your comment: ").strip()

        self.controller.create_comment(post_id, comment)

    def likes(self):
        post_id=self.controller.choose_post()
        self.controller.like(post_id)

if __name__ == '__main__':
    cli = CLI()
    controller = Controller()
