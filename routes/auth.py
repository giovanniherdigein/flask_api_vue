from os import environ
from itsdangerous import URLSafeTimedSerializer
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
import uuid
from models import User, db

auth = Blueprint('auth', __name__,
                 template_folder='../auth')

login_manager = LoginManager()
mail = Mail()


@auth.route('/auth', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _email = request.form.get('email')
        user = User.query.filter_by(email=_email).first()
        check_password_hash(user.password, request.form.get('password'))
        login_user(user)
        # session['username'] = user.username
        session['uid'] = uuid.uuid4()
        print("%s,%s" % (user.id, session['uid']))
        flash("Hallo, Welcome terug")
        return redirect(url_for('root.werkgever'))
    return render_template('login.html')


@ auth.route('/aanmelden', methods=['GET', 'POST'])
def aanmelden():
    if request.method == 'POST':
        _username = request.form.get('username')
        _email = request.form.get('email')
        _password = generate_password_hash(
            request.form.get('password'), method='sha256')
        _repeat = request.form.get('repeat_password')
        user = User(username=_username, email=_email, password=_password)
        db.session.add(user)
        db.session.commit()
        print(user)
        return redirect(url_for('auth.login'))
    return render_template('aanmelden.html')


@ auth.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    return 'authenticate your account'


@ auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    return "Change Password"


@ auth.route('/remove-account', methods=['GET', 'POST'])
def remove_account():
    return "Remove account"


@ auth.route('/update-account', methods=['GET', 'POST'])
def update_account():
    return "Update account"


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('root.index'))


def generate_email_token(email):
    s = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
    salt = environ.get('SECURITY_PASSWORD_SALT')
    return s.dumps(email, salt=salt)


def confirm_email_token(token, expiration=360):
    s = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
    salt = environ.get('SECURITY_PASSWORD_SALT')
    try:
        email = s.load(token, salt=salt)
    except:
        return False
    return email


def add_user(user, request):
    '''
    Adding users to the _active_users_list
    '''
    user = user.id
    sid = request.sid

    pass


def remove_user(user):
    '''
    Removing users from the active_users_list
    '''
    pass
