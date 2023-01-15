#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    ''' <TODO> add documentation '''
    return 'Hello HBNB'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    ''' <TODO> add documentation '''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_fun(text):
    ''' <TODO> add documentation '''
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', defaults={'text': 'is cool'},  strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def py_cool(text='is cool'):
    ''' <TODO> add documentation '''
    return 'Python {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
