from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
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
        msg = Message("Login info",
                      sender="noreply@localhost",
                      recipients=["giovanni.herdigein@gmail.com"])
        mail.send(msg)
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
