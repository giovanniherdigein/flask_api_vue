from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
from datetime import datetime
import uuid
db = SQLAlchemy()
ma = Marshmallow()

Base = declarative_base()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(256), nullable=False)
    registered_on = db.Column(db.Date, default=datetime.utcnow())
    # todos = db.relationship('Todo', backref='todos')
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
    # userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<TODO> {self.id} {self.title}"


opdrachten_tabel = db.Table(
    "opdrachten",
    Base.metadata,
    db.Column('werknemerid', db.ForeignKey('user.id')),
    db.Column('vacature', db.ForeignKey('vacature.id'))
)


class Vacature(db.Model):
    __tablename__ = 'vacature'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.Text)
    opdrachten = db.relationship('Werknemer', backref='opdrachten')
    werkgeverid = db.Column(db.Integer, db.ForeignKey('user.id'))


class Werknemer(User):
    __tablename__ = 'werknemer'
    werknemerid = db.Column(db.String(256))
    # vacature_list = db.Column(db.Integer, db.ForeignKey('vacature.id'))
    # vacatureid = db.Column(db.Integer, db.ForeignKey('vacature.id'))
    # vacaturid = db.relationship("Vacature", secondary=opdrachten_tabel, primaryjoin=(
    # opdrachten_tabel.c.werknemerid == 'id'), backref='opdachten_tabel', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.werknemerid = uuid.uuid4().hex

    def add_to_list(self, vacatureid):
        opdracht = opdracht(self.id, vacatureid)

    def __repr__(self):
        return f'<WERKNEMER: {self.username} {self.werknemerid} id= {self.id}>'


class Werkgever(User):
    werkgeverid = db.Column(db.String(256))
    vacatures = db.relationship('Vacature', backref='vacatures')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.werkgeverid = uuid.uuid4().hex

    def __repr__(self):
        return f'<WERKGEVER:{self.username} {self.werkgeverid} id= {self.id}>'


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
