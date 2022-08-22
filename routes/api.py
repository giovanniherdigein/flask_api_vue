from datetime import datetime
from flask import Blueprint, jsonify, request
from models import Todo, todo_schema, todos_schema, db

api = Blueprint('/api', __name__)


@api.route('/api/todos', methods=['GET'])
def all_todos():
    ''' Haalt alle Todos uit de database'''
    todos = Todo.query.all()
    return jsonify(todos_schema.dump(todos))


@api.route('/api/todo', methods=['POST'])
def post_todo():
    '''Verstuurt een nieuwe post naar de database'''
    data = request.get_data()
    todo = Todo(title=data)
    db.session.add(todo)
    db.session.commit()
    # print(todo)
    return jsonify(message='Succesvol verstuurd')


@api.route('/api/todo/<int:_id>', methods=['PATCH'])
def update_todo(_id):
    '''Pas de desbetreffende todo aan. Maakt 'm completed'''
    if request.method == 'PATCH':
        try:
            todo = Todo.query.filter_by(id=_id).first()
            todo.completed = not todo.completed
            todo.date_created = datetime.utcnow()
            db.session.commit()
            return jsonify(message='Gelukt de record aan te passen')
        except Exception as e:
            print(e)
            return jsonify(message="Er ging iets fout %s" % e)


@api.route('/api/todo/<int:_id>', methods=['DELETE'])
def delete_todo(_id):
    '''Deze verwijdert de todo'''
    todo = Todo.query.filter_by(id=_id).first()
    db.session.delete(todo)
    db.session.commit()
    return jsonify(message="Gelukt de record te verwijderen")


@api.route('/api/todo/<int:_id>', methods=['GET'])
def get_todo(_id):
    '''Haalt 1 todo uit de database'''
    todo = Todo.query.filter_by(id=_id).first()
    return jsonify(todo_schema.dump(todo))


@api.route('/api/todo/<int:_id>', methods=['PUT'])
def complete_update_todo(_id):
    try:
        todo = Todo.query.get(_id)
        todo.title = request.form['title']
        todo.date_created = datetime.utcnow()
        db.session.commit()
        return jsonify(message="Gelukt, De record is aangepast")
    except:
        return jsonify(message="Oops, Er ging is mis")
