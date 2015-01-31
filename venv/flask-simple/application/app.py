# encoding=utf-8
from flask import Flask, make_response, request, g, send_from_directory
from flask import url_for, render_template
from werkzeug.routing import BaseConverter
import random
import os.path

class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split(',')
    def to_url(self, values):
        return ','.join(BaseConverter.to_url(value)
                        for value in values)


app = Flask(__name__,static_url_path="/test")
app.url_map.converters['list'] = ListConverter





@app.route("/task/")
def task_list():
    return "List of all task"

@app.route("/task/<int:task_id>/")
def task_detail(task_id):
    return "Detail of task#{}.".format(task_id)

@app.route("/task/<int:task_id>/edit/",methods=['GET','POST'])
def task_edit(task_id):
    return 'From to edit task#{}.'.format(task_id)

@app.route("/task/create/",methods=['GET','POST'])
def task_create():
    return "Create New Task"

@app.route("/task/<int:task_id>/delete/",methods=['DELETE'])
def task_delete(task_id):
    raise NotImplementedError('DELETE')

@app.route("/list/<list:data>/")
def test_list(data):
    return ''.join(data)
@app.route("/string/")
def return_string():
    return "Hello,world"

@app.route("/object/")
def return_object():
    headers={'Content-Type':'text/plain'}
    return make_response('Hello,world',200,headers)

@app.route("/tuple/")
def return_tuple():
    return "hello,world",304,{'Content-Type':'text/plain'}

def dump_request_detail(request):
    request_detail="""
request.endpoint:{request.endpoint}
request.method:{request.method}
request.view_args:{request.view_args}
request.args:{request.args}
request.form:{request.form}
request.user_agent:{request.user_agent}
request.files:{request.files}
request.is_xhr:{request.is_xhr}
{request.headers}""".format(request=request).strip()
    return request_detail

@app.before_request
def set_on_g_object():
    x = random.randint(0,9)
    app.logger.debug('before request g.x is {x}'.format(x=x))
    g.x = x

@app.route("/g")
def test():
    g.x=1000
    return str(g.x)

@app.after_request
def get_on_g_object(response):
    app.logger.debug('after request g.x is{g.x}'.format(g=g))
    return response



@app.route("/css")
def static_create():
    return url_for('static',filename='style.css')


dirpath = os.path.join(app.root_path,'upload')
@app.route("/download/<path:filename>")
def downloader(filename):
    return send_from_directory(dirpath,filename,as_attachment=True)

