from flask import Flask,render_template
from flask.ext.restful import reqparse, abort, Api, Resource,fields, marshal_with
from flask import make_response
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
from flask.ext import restful
import pymongo
import json

app = Flask(__name__, static_url_path='')

def output_json(obj, code, headers=None):
    """
    This is needed because we need to use a custom JSON converter
    that knows how to translate MongoDB types to JSON.
    """
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})

    return resp

def get_db():

    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client['dashboard-info']

    return db

def get_projects(db):
    return db.projects

db = get_db()
projectsO = get_projects(db)
projects = output_json(projectsO.find())

print projects
api = Api(app)




@app.route('/')
def home_page():
    return app.send_static_file('index.html')









TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}



def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

post_parser = reqparse.RequestParser()
post_parser.add_argument('task', type=str, required=True,
help="task cannot be blank!")
post_parser.add_argument('task', type=str, action='append')








# Todo
#   show a single todo item and lets you delete them
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


def tojson(obs):
    output =[]
    for ob in obs.find():
         output.append(ob)
    return output


# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class Projects(Resource):
    def get(self):
        return projects
##
## Actually setup the Api resource routing here
##
class MongoEncoder(JSONEncoder):
    def mongo_dumps(obj):
        # convert all iterables to lists
        if hasattr(obj, '__iter__'):
            return list(obj)
        # convert cursors to lists
        elif isinstance(obj, pymongo.cursor.Cursor):
            return list(obj)
        # convert ObjectId to string
        elif isinstance(obj, bson.objectid.ObjectId):
            return unicode(obj)
        # dereference DBRef
        elif isinstance(obj, bson.dbref.DBRef):
            return db.dereference(obj) # db is the incetance database
        # convert dates to strings
        elif isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)

app = app()
app.autojson = False
m_encoder = MongoEncoder()
app.install(JSONPlugin(json_dumps=lambda s: dumps(s, default=m_encoder.mongo_dumps)))




api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')

api.add_resource(Projects, '/api/projects')







if __name__ == '__main__':
    app.run(debug=True)