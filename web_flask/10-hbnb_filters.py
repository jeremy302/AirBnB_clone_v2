#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
''' <TODO> add documentation '''
    states = sorted((storage.all(State).values()), key=lambda x: x.name)
    for state in states:
        state.cities.sort(key=lambda x: x.name)
    amenities = sorted(list(storage.all(Amenity).values()), key=lambda x: x.name)

    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(ctx):
    ''' <TODO> add documentation '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
