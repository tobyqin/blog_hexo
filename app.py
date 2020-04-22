import flask
import werkzeug
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='public')

root = 'public'


@app.route('/')
def hello_world():
    return send_from_directory(root, 'index.html')


@app.route('/<path:filename>')
def index(filename: str):
    if filename.endswith('/'):
        filename += 'index.html'
    try:
        return flask.send_from_directory(root, filename)
    except werkzeug.exceptions.NotFound as e:
        if filename.endswith("/"):
            return flask.send_from_directory(root, filename + "index.html")
        raise e


@app.route('/config')
def config():
    return "config page"


app.run()
