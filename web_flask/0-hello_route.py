#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask
app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_world():
    ''' <TODO> add documentation '''
    return 'Hello HBNB'
