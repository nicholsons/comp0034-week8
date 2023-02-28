# Week 3 activities (REST API version) 3 hours

Check you can run the app before you start:
`python -m flask --app 'paralympic_app:create_app()' --debug run`

Last week you created skeleton functions for the REST API. This week you will:

1. [Map the data to SQLAlchemy classes (45 mins)](#1-map-the-data-to-sqlalchemy-classes)
2. [Serialise and deserialise the data (45 mins)](#2-serialise--deserialise-the-data)
3. [Update the routes to return the expected JSON (45 mins)](#3-update-the-routes-to-return-json)
4. [Use the API routes to generate a list of paralympic events on the homepage (30 mins)](#4-use-the-api-to-generate-a-list-of-paralympic-events-on-the-homepage)

Note: this week's activties do not gracefully handle errors. Error handling will be covered in week 10.

## 1. Map the data to SQLAlchemy classes

Install Flask-SQLAlchemy if you have not already `pip install Flask-SQLAlchemy`. This should also install SQLAlchemy.

You may want to install the VS Code extension SQLite Viewer to allow you to view the content of a database through the VS Code interface.

The logical steps for this activity are:

1. Create a sqlite database in the data folder of the paralympic_app, and load the data from csv and save to a SQLite database.
2. Modify the `paralympic_app/__init__.py` code:
    - Create a SQLAlchemy instance
    - Add configuration parameters to the Flask app instance to tell it the location of the database file and to not track modifications.
    - Modify the `create_app` function so that after the Flask app instance is created, it is registered to the SQLAlchemy instance.
    Modify the `create_app` function after the Flask app is registered to the SQLAlchemy instance to reference the tables in the database (you need this so that the app can map the tables to Python classes).

3. Define the Python classes ('models' in our Flask app) that will map to the data. Include a `repr` function for each class that provides a string representation of the class.

### Why we are using Flask-SQLAlechemy, SQLAlchemy with an SQLite database

When you install Flask-SQLAlchemy, the SQLAlchemy package will also be installed. Together they provide functionality that lets you more easily create Python classes that map to database tables; and handles the database interaction, i.e. SQL queries, using Python functions. This follows a design pattern called ORM, Object Relational Mapper. An ORM encapsulates, or wraps, data stored in a database into an object that can be used in Python (or other object-oriented language).

SQLAlchemy will not work directly with .csv files, though you may be able to find additional python libraries that provide such support. For the coursework it is assumed that you will save your csv file contents to a sqlite database and work with that instead of directly with the csv file.

If you want to work directly with .csv files for coursework 2 and not a database, then you could use pandas and read from, and save to, csv. Since most web apps work with a database then this version is not taught in the course. However, you should have sufficient pandas skills to do this if you prefer. If you do this then you will not use Flask-SQLAlchemy.

SQLite allows you to store the data in tables. If your data is a single worksheet, then you can save it to a single table in SQLAlchemy. Groups however will have designed a database structure which likely has multiple tables that are related through the use of primary and secondary keys. This tutorial will cover a data set that has multiple tables and those that have a single table. There will be some unfamiliar technical terms for those students who did not follow the database lecture and activities from COMP0035.

### 1.1 Create a SQLite database from a csv file

The code for this is given you in `csv_to_sqlite.py`. There are many ways to save csv as sqlite. The following uses libraries you should be familiar with from COMP0035, namely pandas and pathlib; and introduces some sqlalchemy code.

Sqlachemy is used to create the database engine. The engine handles the connection to the database file and operates as if a sqlite database.

The code is commented and can be found in the data directory.

`data\cvs_to_sqlite.csv` creates two tables in a database that are not related. If you have a single CSV file this would be a suitable approach for your project.

`data\cvs_to_sqlite_with_relations.csv` creates a relationship between the `event` and `region` tables using the `NOC` attribute as primary key in region and foreign key in event. Groups who designed a database with multiple tables would need this approach.

### 1.2 Modify the code to create and configure the Flask app

Refer to the [Flask-SQLAlchemy documentation for the configuration](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#configure-the-extension). T.

Modify the `create_app` function to create an instance of SQLAlchemy. There are two ways to do this in the Flask-SQLAlchemy documentation. Let's use the version that creates the global instance and then initialises it for the Flask app.

```python
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent

# Create a global SQLAlchemy object
db = SQLAlchemy()


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "YY3R4fQ5OmlmVKOSlsVHew"
    # configure the SQLite database location
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
        PROJECT_ROOT.joinpath("data", "paralympics.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    # Uses a helper function to initialise extensions
    initialize_extensions(app)

    # Include the routes from routes.py
    with app.app_context():
        from . import routes

    return app


def initialize_extensions(app):
    """Binds extensions to the Flask application instance (app)"""
    # Flask-SQLAlchemy
    db.init_app(app)
```

### 1.3 Define the model classes

Create a python file. This is often named `models.py` but doesn't have to be.

Add the following code to create two classes that represents the data in the database.

```python
from paralympic_app import db

class Region(db.Model):
    """NOC region"""

    __tablename__ = "region"
    NOC = db.Column(db.Text, primary_key=True)
    region = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    events = db.relationship("Event", back_populates="region")

    def __repr__(self):
        """
        Returns the attributes of the region as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.NOC}, {self.region}, {self.notes}>"


class Event(db.Model):
    """Paralympic event"""

    __tablename__ = "event"
    event_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Text, nullable=False)
    lat = db.Column(db.Text)
    lon = db.Column(db.Text)
    NOC = db.Column(db.Text, db.ForeignKey("region.NOC"), nullable=False)
    start = db.Column(db.Text, nullable=False)
    end = db.Column(db.Text, nullable=False)
    disabilities_included = db.Column(db.Text, nullable=False)
    events = db.Column(db.Text, nullable=False)
    sports = db.Column(db.Text, nullable=False)
    countries = db.Column(db.Integer, nullable=False)
    male = db.Column(db.Integer, nullable=False)
    female = db.Column(db.Integer, nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    highlights = db.Column(db.Text)
    region = db.relationship("Region", back_populates="events")

    def __repr__(self):
        """
        Returns the attributes of the event as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}: {self.type},{self.type}, {self.year}, {self.location}, {self.lat}, {self.lon}, {self.NOC}, {self.start}, {self.end}, {self.diabiliities}, {self.events}, {self.sports}, {self.countries}, {self.male}, {self.female}, {self.participants}, {self.highlights}>"

```

`db` you created in step 2 in the `paralympic_app/__init__.py` and is the SQLAlchemy instance.

The syntax for the table is from the [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application). The table is defined as follows:

- Define the class with an appropriate name.
- The tablename should match the tablename in the databse.
- The column names should match the column names used in the database.
- The column datatypes should match the data types used in the database.

The `relationship` between the two tables is defined used the primary and foreign keys with the db.relationship function as follows:

```python
class Region(db.Model):
    __tablename__ = "region"
    # column details ommited
    NOC = db.Column(db.Text, primary_key=True)
    events = db.relationship("Event", back_populates="region")


class Event(db.Model):
    __tablename__ = "event"
    # column details ommited
    NOC = db.Column(db.Text, db.ForeignKey("region.NOC"), nullable=False)
    region = db.relationship("Region", back_populates="events")    
```

## 2. Serialise / deserialise the data

Since this can become complex, use libraries to help you. This activity uses:

- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- marshmallow-sqlalchemy

Install both of the above into your venv (may already be installed if you used `pip install -r requirements.txt` from the week 4 repository).

### Configure the app for Flask-Marshmallow

Flask-Marshmallow will be used with Flask-SQLAlchemy so [this part of the documentation is most relevant](https://flask-marshmallow.readthedocs.io/en/latest/#optional-flask-sqlalchemy-integration). The documentation states that Flask-SQLAlchemy must be initialized before Flask-Marshmallow.

```python
from flask_marshmallow import Marshmallow

# Create a global SQLAlchemy object
db = SQLAlchemy()
# Create a global Flask-Marshmallow object
ma = Marshmallow()


def create_app():

... existing code ...

    # Flask-SQLAlchemy
    db.init_app(app)
    # Flask-Marshmallow
    ma.init_app(app) 

    with app.app_context():
        # This is required as you must instantiate the models before marshamallow schemas
        from paralympic_app.models import Event, Region

... existing code ...
```

## 3. Update the routes to return JSON

In a REST API your routes return HTTP responses in JSON rather than a web page.

The routes in this app use a combination of:

- Accessing data from the Flask request object when an HTTP request is submitted
- Flask-SQLAlchemy to query the database
- Flask-Marshmallow for the serialisation/deserialisation of the data to and from JSON
- Flask make_response to create HTTP responses where there is no other data to return

### GET routes

The first route is `/noc` which gets a list of all the region codes and returns these in an HTTP response in JSON format.

The Flask-SQLAlchemy query syntax for a 'SELECT' query is exaplained in the [Flask-SQLAlchemy 3.x documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/#select)

```python
@app.get("/noc")
def noc():
    """Returns a list of NOC region codes and their details in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_regions = db.session.execute(db.select(Region)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = regions_schema.dump(all_regions)
    # Return the data
    return result


@app.get("/event/<int:event_id>")
def event_id(event_id):
    """Returns the details for a specified event id"""
    event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).scalar_one_or_none()
    return events_schema.dump(event)
```

Now try and implement the `@app.get("/event")` and `@app.get("/event/<int:event_id>")` routes.

### DELETE routes

DELETE routes need to query the database but the HTTP JSON response that is returned is a message rather than database records. Marshmallow isn't used in this case.

Instead you can create an HTTP response using the [Flask `make_response` function](https://flask.palletsprojects.com/en/2.2.x/api/?highlight=make_response#flask.make_response).

You need to know a little about HTTP responses. You will set the [Content-Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type), and the [status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) as well as sending the body of the content.

```python
@app.delete("/noc/<code>")
def noc_delete(code):
    """Removes a NOC record from the dataset."""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    region = db.session.execute(
        db.select(Region).filter_by(NOC=code)
    ).scalar_one_or_none()
    # Delete the record you found
    db.session.delete(region)
    db.session.commit()
    # Return a JSON HTTP response to let the person know it was deleted
    text = jsonify({"Successfully deleted": region.NOC})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response
```

### POST and PATCH routes

Use the [Flask-SQLAlechemy documentation for INSERT and UPDATE](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/#insert-update-delete)

For these requests you need to access more than just the variable passed to the route, you need to access JSON data passed with the request. You can do this using:

1. Flask.request.json.get for an individual property e.g. `region = request.json.get("region", "")` gets the value for "region" and if it isn't in the requests sets it to an empty string instead.

2. Flask request.get_json() which converts the JSON object into Python data.

Flask translates JSON data into Python data structures:

- Anything that is an object gets converted to a Python dict. `{"key" : "value"}` in JSON corresponds to `somedict['key']`, which returns a value in Python.
- An array in JSON gets converted to a list in Python. The syntax is the same, e.g.: `[1,2,3,4,5]`
- The values inside of quotes in the JSON object become strings in Python.
- Boolean true and false become True and False in Python.
- Numbers without quotes around them become numbers in Python.

An example of using request.get_json():

```python
request_data = request.get_json()
NOC = request_data['NOC']
notes = request_data['notes']
```

The following shows how a new NOC could be added:

```python
@app.post("/noc")
def noc_add():
    """Adds a new NOC record to the dataset."""
    # Get the values of the JSON sent in the request
    NOC = request.json.get("NOC", "")
    region = request.json.get("region", "")
    notes = request.json.get("notes", "")
    # Create a new Region object using the values
    region = Region(NOC=NOC, region=region, notes=notes)
    # Save the new region to the database
    db.session.add(region)
    db.session.commit()
    # Return a reponse to the user with the newly added region in JSON format
    result = region_schema.jsonify(region)
    return result
```

To update a request you need to first find the record in the database and then update the relevant fields:

```python
@app.patch("/noc/<code>")
def noc_update(code):
    """Updates changed fields for the NOC record"""
    # Find the current region in the database
    existing_region = db.session.execute(
        db.select(Region).filter_by(NOC=code)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    region_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    region_schema.load(region_json, instance=existing_region, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(Region).filter_by(NOC=code)
    ).scalar_one_or_none()
    result = region_schema.jsonify(updated_region)
    return result
```

Try and implement routes for `@app.post("/event")` and `@app.patch("/event/<event_id>")`

### Check the routes work using Postman

- GET for single region: `GET http://127.0.0.1:5000/noc/GBR`
- GET for all regions: `GET http://127.0.0.1:5000/noc`
- POST for new region: `POST http://127.0.0.1:5000/noc` In the body select 'raw' and 'JSON' and enter

```json
{
    "NOC": "ZZZ",
    "region": "ZedZedZed"
}
```

= PATCH to update the 'ZZZ' region adding notes: `PATCH http://127.0.0.1:5000/noc/ZZZ` In the body select 'raw' and 'JSON' and enter

```json
{
    "notes" : "some new notes again again again"
}
```

- DELET the 'ZZZ" region: `DELETE http://127.0.0.1:5000/noc/ZZZ`
- GET a single event:  `GET`<http://127.0.0.1:5000/event/1>`
- GET all events: `GET http://127.0.0.1:5000/event`
- POST a new event: `POST http://127.0.0.1:5000/event` In the body select 'raw' and 'JSON' and enter

```json
{
    "NOC": "GBR",
    "countries": 17,
    "disabilities_included": "Spinal injury",
    "end": "25-Sep-60",
    "events": "113",
    "female": null,
    "location": "London",
    "male": null,
    "participants": 209,
    "region": "ITA",
    "sports": "8",
    "start": "18-Sep-60",
    "type": "Summer",
    "year": 2022
}
```

- PATCH to update the new event: `POST http://127.0.0.1:5000/event/28` In the body select 'raw' and 'JSON' and enter

```json
{
    "countries": 21,
    "end": "25-Sep-22",
    "start": "18-Sep-22",
    "year": 2022
}
```

##  4. Use the API to generate a list of paralympic events on the homepage

This is a simple illustration of querying data from an API to generate a page in an application.

Modify the homepage route to make a call the API routes and return

The route will:

- Make an HTTP request to the relevant URL.
- Receive the JSON that is returned from the URL
- Pass the JSON to a page template
- Use Jinja in the page template to generate HTML from the JSON

If you are using an external API, or your own API that is being run as a separate web app, you could use the requests library e.g.

```python
import requests

response_json = requests.get('https://myapi.com/event').json()
```

The localhost URL for the events page when the app is run on port 5000 will be: <http://127.0.0.1:5000/event>

You could of course just query the database but the purpose of this is to show you how to use JSON results to generate a page.

The index route could look like this:

```python
import requests

@app.route("/")
def index():
    """Returns the home page"""
    url = "http://127.0.0.1:5000/event"
    response = requests.get(url).json()
    return render_template("index.html", event_list=response)
```

The 'index.html' template could look like this:

```jinja
{% extends 'layout.html' %}
{% set title = 'Paralympics Home' %}
{% block content %}

<h1>Paralympic events</h1>
<p>We have data for the following events</p>
<ul>
    {% for event in event_list %}
    <li>{{ event['location'] }} {{ event['year'] }} ({{ event['type'] }})</li>
    {% endfor %}
</ul>

{% endblock %}
```

## Further

Investigate [APIFairy](https://testdriven.io/blog/flask-apifairy/) from Miguel Grinberg. [Example app code](https://github.com/miguelgrinberg/microblog-api).

[Tutorial explaining how to create a database using Flask-SQLAlchemy with relationships between the tables](https://www.digitalocean.com/community/tutorials/how-to-use-one-to-many-database-relationships-with-flask-sqlalchemy)

Flask-SQLAlchemy

<https://akashsenta.com/blog/flask-rest-api-with-sqlalchemy-and-marshmallow/>

<https://medium.com/craftsmenltd/flask-with-sqlalchemy-marshmallow-2ec34ecfd9d4>
