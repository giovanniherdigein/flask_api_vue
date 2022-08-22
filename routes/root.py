from flask import Blueprint, render_template
from flask_login import login_required, current_user
root = Blueprint('root', __name__,
                 template_folder='templates')


# Eerste route van onze app
@root.route('/', methods=['GET'])
# @login_required
def index():
    return render_template('index.html')


@root.route('/over', methods=['GET'])
def over():
    return render_template('over.html')


@root.route('/services', methods=['GET'])
def services():
    return render_template('services.html')


@root.route('/werkgever')
@login_required
def werkgever():
    return 'Werkgever %s ingelogt' % current_user.username
