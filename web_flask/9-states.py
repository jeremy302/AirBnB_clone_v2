#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
''' <TODO> add documentation '''
    states = list(storage.all(State).values())
    value = None
    if id is None:
        states.sort(key=lambda x: x.name)
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        value = states
        status = 0
    else:
        state = next((s for s in states if s.id == id), None)
        if state:
            state.cities.sort(key=lambda x: x.name)
            value = state
            status = 1
        else:
            status = -1

    return render_template('9-states.html', status=status, value=value)

@app.route('/cities_by_states', strict_slashes=False)
def get_states():
    ''' <TODO> add documentation '''
    states = sorted(storage.all(State).values(), key=lambda k: k.name)
    for state in states:
        state.cities.sort(key=lambda k: k.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(ctx):
    ''' <TODO> add documentation '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
