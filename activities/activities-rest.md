TODO: This is incomplete.

# Week 3 activities (REST API version) 3 hours

Check you can run the app before you start:
`python -m flask --app 'paralympic_app:create_app()' --debug run`

Last week you created skeleton functions for the REST API. This week you will:

1. Map the data to SQLAlchemy classes
2. Serialise and deserialise the data
3. Update the routes to return the expected JSON

Note: this week's activties do not gracefully handle errors, this will be covered in week 5.

## 1. Map the data to SQLAlchemy classes

The logical steps for this activity are:

1. Define the Python classes ('models' in our Flask app) that will map to the data. Include a `repr` function for each class that provides a string representation of the class.
2. Create a sqlite database in the data folder of the paralympic_app, and load the data from csv and save to a SQLite database.
3. Modify the Flask code so that a SQLAlchemy instance is created.
4. Add configuration parameters to the Flask app instance to tell it the location of the database file and to not track modifications.
5. Modify the `create_app` function so that after the Flask app instance is created, it is registered to the SQLAlchemy instance.
6. Modify the `create_app` function after the Flask app is registered to the SQLAlchemy instance to reference the tables in the database (you need this so that the app can map the tables to Python classes).

Install Flask-SQLAlchemy if you have not already `pip install Flask-SQLAlchemy`. This should also install SQLAlchemy.

You may want to install the VS Code extension SQLite Viewer to allow you to view the content of a database through the VS Code interface.

### Why we are using Flask-SQLAlechemy, SQLAlchemy with an SQLite database

When you install Flask-SQLAlchemy, the SQLAlchemy package will also be installed. Together they provide functionality that lets you more easily create Python classes that map to database tables; and handles the database interaction, i.e. SQL queries, using Python functions. This follows a design pattern called ORM, Object Relational Mapper. An ORM encapsulates, or wraps, data stored in a database into an object that can be used in Python (or other object-oriented language).

[According to this article](https://www.cdata.com/kb/tech/csv-python-sqlalchemy.rst), you can configure SQLAlchemy to work with .csv files though there is very little documentation to support this. Most tutorials for Flask-SQLAlchemy and SQLAlchemy assume you are working with a database. For the coursework it is assumed you will save your csv file contents to a sqlite database and work with that instead of directly with the csv file.

SQLite allows you to store the data in tables. If your data is a single worksheet, then you can save it to a single table in SQLAlchemy. Groups however will have designed a database structure which likely has multiple tables that are related through the use of primary and secondary keys. This tutorial will cover a data set that has multiple tables and those that have a single table. There will be some unfamiliar technical terms for those students who did not follow the database lecture and activities from COMP0035.

### Define the model classes

### Option 1: Create the database from the model classes and load the data to them from CSV

### Option 1: Create a SQLite database from a csv file

The code for this is given you in `csv_to_sqlite.py`. There are many ways to save csv as sqlite. The following uses libraries you should be familiar with from COMP0035, namely pandas and pathlib; and introduces some sqlalchemy code.

Sqlachemy is used to create the database engine. The engine handles the connection to the database file and operates as if a sqlite database.

The code is commented and can be found in the data directory.

`data\cvs_to_sqlite.csv` creates two tables in a database that are not related. If you have a single CSV file this would be a suitable approach for your project.

`data\cvs_to_sqlite_with_relations.csv` creates a relationship between the `event` and `region` tables using the `NOC` attribute as primary key in region and foreign key in event. Groups who designed a database with multiple tables would need this approach.

Note that many of the Flask-SQLAlchemy tutorials assume that you do not already have data. If this is the case then you can create the models in the

### Modify the Flask code so that a SQLAlchemy instance is created

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

## 2. Serialise / deserialise the data

Since this can become complex, use libraries to help you. This activity uses:

- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
- marshmallow-sqlalchemy

Install both of the above into your venv (may already be installed if you used `pip install -r requirements.txt` from the week 4 repository).

### Configure the app for Flask

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

... existing code ...
```

## Check the routes work using Postman

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

## Further

Investigate [APIFairy](https://testdriven.io/blog/flask-apifairy/) from Miguel Grinberg. [Example app code](https://github.com/miguelgrinberg/microblog-api).

[Tutorial explaining how to create a database using Flask-SQLAlchemy with relationships between the tables](https://www.digitalocean.com/community/tutorials/how-to-use-one-to-many-database-relationships-with-flask-sqlalchemy)

Flask-SQLAlchemy

<https://akashsenta.com/blog/flask-rest-api-with-sqlalchemy-and-marshmallow/>

<https://medium.com/craftsmenltd/flask-with-sqlalchemy-marshmallow-2ec34ecfd9d4>
