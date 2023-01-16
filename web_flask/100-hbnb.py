#!/usr/bin/python3
''' <TODO> add documentation '''
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


@app.route('/hbnb')
def hbnb():
''' <TODO> add documentation '''
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    amenities = list(storage.all(Amenity).values(), key=lambda x: x.name)
    places = list(storage.all(Place).values(), key=lambda x: x.name)

    for state in states:
        state.cities.sort(key=lambda x: x.name)
    for place in places:
        place.description = Markup(place.description)

    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)



@app.teardown_appcontext
def teardown(ctx):
    ''' <TODO> add documentation '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
