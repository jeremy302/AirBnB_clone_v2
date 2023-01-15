#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask, render_template
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
def py_cool(text):
    ''' <TODO> add documentation '''
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    ''' <TODO> add documentation '''
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    ''' <TODO> add documentation '''
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_even(n):
    ''' <TODO> add documentation '''
    return render_template('6-number_odd_or_even.html', n=n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
