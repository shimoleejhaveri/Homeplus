"""Models and database functions for Hackbright Capstone project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of dashboard."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    home_add = db.Column(db.String, nullable=True, unique=False)
    work_add = db.Column(db.String, nullable=True, unique=False)
    timezone = db.Column(db.String(100), nullable=True, unique=False)
    clock_opt = db.Column(db.String(2), nullable=True, unique=False)
    weather_opt = db.Column(db.String(1), nullable=True, unique=False)

    to_do_lists = db.relationship('ToDoList', backref='user')
    shared_lists = db.relationship('ToDoList',
                                   backref='shared_users',
                                   secondary='shared_users_lists')

    def __repr__(self):
        """Returns a human-readable representation of a user."""

        return f'<User user_id={self.user_id} name={self.name} email={self.email}>'


class ToDoList(db.Model):
    """Lists created by each user."""

    __tablename__ = 'to_do_lists'

    # Defining columns and relationships of To-Do Lists
    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_title = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=False)

    to_do_items = db.relationship('ToDoItem', backref='to_do_list')

    def __repr__(self):
        """Returns a human-readable representation of a to-do list."""

        return (f'<List list_id={self.list_id} list_title={self.list_title} ' +
                f'user_id={self.user_id}>')


class ToDoItem(db.Model):
    """Items and item-descriptions corresponding to each individual list."""

    __tablename__ = 'to_do_items'

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_title = db.Column(db.String, nullable=False, unique=False)
    item_description = db.Column(db.String, nullable=True, unique=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer,
                        db.ForeignKey('to_do_lists.list_id'),
                        unique=False)

    def __repr__(self):
        """Returns a human-readable representation of a to-do item."""

        return (f'<Item item_id={self.item_id} item_title={self.item_title} ' +
                f'list_id={self.list_id}>')


class SharedUsersLists(db.Model):
    """Different users sharing the same lists."""

    __tablename__ = 'shared_users_lists'
    __table_args__ = (db.UniqueConstraint('shared_user_id', 'shared_list_id'),)

    shared_users_list_id = db.Column(db.Integer,
                                     autoincrement=True,
                                     primary_key=True)
    shared_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.user_id'))
    shared_list_id = db.Column(db.Integer,
                               db.ForeignKey('to_do_lists.list_id'))

    def __repr__(self):
        """Returns a human-readable representation of a shared to-do list."""

        return (f'<SharedUsersLists shared_users_list_id={self.shared_users_list_id}' +
                f'shared_list_id={self.shared_list_id} ' +
                f'shared_user_id={self.shared_user_id}>')


def create_test_data():
    """Test data."""

    user1 = User(name='John Doe', email='johndoe@test.com', password='jdoe123', 
    home_add='1, Home Street, San Francisco', work_add='10, Google Way, San Francisco',
    timezone='Pacific', clock_opt='12', weather_opt='F') 
    
    user2 = User(name='Jane Doe', email='janedoe@test.com', password='doej123', 
    home_add='5, Home Address, San Francisco', work_add='200, Facebook Street, San Francisco',
    timezone='Eastern', clock_opt='24', weather_opt='C')


    user1_list = ToDoList(list_title='work tasks')
    user1.to_do_lists.append(user1_list)
    user1_list.to_do_items.append(ToDoItem(item_title='debug flask',
                                            item_description='flask debug toolbar doesn\'t work any more'))

    user2_list = ToDoList(list_title='assignment work')
    user2.to_do_lists.append(user2_list)
    user2_list.to_do_items.append(ToDoItem(item_title='create routes', 
                                            item_description='connect database to server using flask routes'))


    user1_shared_list = ToDoList(list_title='shared chores')
    user1.to_do_lists.append(user1_shared_list)
    user1_shared_list.to_do_items.append(ToDoItem(item_title='laundry', 
                                                item_description='launder all white clothes'))
    user2.shared_lists.append(user1_shared_list)

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
