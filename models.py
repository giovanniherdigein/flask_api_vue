from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(256), nullable=False)
    registered_on = db.Column(db.Date, default=datetime.utcnow())
    todos = db.relationship('Todo', backref='todos')
    # is_authenticated = db.Column(db.Boolean, default=False)
    # is_active = db.Column(db.Boolean, default=False)
    # is_anonumous = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<USER: {self.id} {self.email}>'

    def get_id(self):
        return super().get_id()


class Todo(db.Model):
    '''Declaring the Todo model'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<TODO> {self.id} {self.title}"


class Sessions(db.Model):
    '''Sessions are stored'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    key = db.Column(db.String(255))

    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __repr__(self):
        return f"<SESSION> {self.name} : {self.key}"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo


user_schema = UserSchema()
users_schema = UserSchema(many=True)

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
