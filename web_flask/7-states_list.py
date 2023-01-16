#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def get_states():
    ''' <TODO> add documentation '''
    states = sorted(storage.all().values(), key=lambda k: k.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    ''' <TODO> add documentation '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
