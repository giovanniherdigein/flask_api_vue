from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from routes.root import root as root_blueprint
from routes.auth import auth as auth_blueprint
from routes.api import api as api_blueprint
from routes.auth import login_manager
from dotenv import load_dotenv
from os import environ
from models import *

# building the app
app = Flask(__name__)
# configuration files
load_dotenv('.env')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    "SQLALCHEMY_DATABASE_URI")  # 'sqlite:///flask_vue_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['FLASK_SERVER_PORT'] = 8943
# app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config.from_pyfile('Flask_App.cfg')
# creating the database app, origins=[“http://localhost:8000”, “https://example.com”])
# db = SQLAlchemy()
# ma = Marshmallow()
db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)

login_manager.login_message = "U dient in te loggen voor u verder gaat"
login_manager.login_view = 'auth.login'
CORS(app, origins=["http://localhost:5000"])
# creating the model from here


@login_manager.user_loader
def user_loader(id):
    user = User.query.get(int(id))
    return user


# registering the routes
app.register_blueprint(root_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Todo': Todo,
        'Werkgever': Werkgever,
        'Werknemer': Werknemer,
        'Vacature': Vacature
    }


# starting the app
if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
