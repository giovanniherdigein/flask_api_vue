from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_babelex import Babel
from routes.root import root as root_blueprint
from routes.auth import auth as auth_blueprint
from routes.api import api as api_blueprint
from routes.auth import login_manager, current_user, mail
from models import *

# building the app
app = Flask(__name__)
# configuration files
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_vue_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config.from_pyfile('mail_config.cfg')
# creating the database app, origins=[“http://localhost:8000”, “https://example.com”])
# db = SQLAlchemy()
# ma = Marshmallow()
db.init_app(app)
ma.init_app(app)
babel = Babel(app)
login_manager.init_app(app)
mail.init_app(app)

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

# starting the app
if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
