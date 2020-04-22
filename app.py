import werkzeug
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='public')

root = 'public'
default_page = 'index.html'


@app.route('/')
def hello_world():
    return send_from_directory(root, default_page)


@app.route('/<path:filename>')
def index(filename: str):
    if filename.endswith('/'):
        filename += default_page
    try:
        return send_from_directory(root, filename)
    except werkzeug.exceptions.NotFound as e:
        if filename.endswith("/"):
            return send_from_directory(root, filename + default_page)
        raise e


@app.route('/config')
def config():
    return "config page"


app.run()
