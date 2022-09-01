from flask import Blueprint, render_template, make_response, request, session, redirect, url_for
from flask_login import login_required, current_user
root = Blueprint('root', __name__,
                 template_folder='templates')


# Eerste route van onze app
@root.route('/', methods=['GET'])
# @login_required
def index():
    check_user_in_session()
    cookie_name = request.cookies.get('User_Name')
    resp = make_response(render_template('index.html', name=cookie_name))
    return resp


@root.route('/over', methods=['GET'])
def over():
    return render_template('over.html')


@root.route('/services', methods=['GET'])
def services():
    return render_template('services.html')


@root.route('/werkgever')
@login_required
def werkgever():
    check_user_in_session()
    resp = make_response(render_template('werkgever.html'))
    resp.set_cookie("User_Name", current_user.username, 30)
    return resp


def check_user_in_session():
    if not 'uid' in session:
        return redirect(url_for('auth.login'))
