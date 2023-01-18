# Week 8 activities (ML version)

Check you can run the app before you start:
`python -m flask --app 'iris_app:create_app()' --debug run`

The activities include:

- [Activity 1: Add an iris prediction form to the index.html template](#activity-1-add-an-iris-prediction-form-to-the-indexhtml-template)
- [Activity 2: Add a database to the application and use it to generate pages and capture new data from users](#activity-2-add-a-database-to-the-application)

## Activity 1: Add an iris prediction form to the index.html template

Create a form that allows someone to enter the following details and then press a button to get a prediction of the species/variety:

- sepal_length
- sepal_width
- petal_length
- petal_width

This requires 3 parts:

1. A python form class using Flask-WTForms that defines the form fields
2. An HTML form in `index.html`
3. Changes to the index route route in `routes.py`

### Part 1: Form class

To do this you can create a form class with [Flask-WTForms](https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/#creating-forms).

To separate your code, add the form functionality to a new python file (module) called forms.py

Create a class that will contain the form fields like the following:

```python
from flask_wtf import FlaskForm


class PredictionValues(FlaskForm):
    """Fields to a form to input the values required for an iris species prediction"""

```

The form fields take a decimal to 1 place. Use the [DecimalField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.DecimalField) for all the fields.

All values are required for a prediction.

Add the DecimalFields with a validator that the value is required. One field is given as an example below.

```python
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import DataRequired


class PredictionForm(FlaskForm):
    """Form fields to input the values required to predict iris variety"""

    sepal_length = DecimalField(validators=[DataRequired()])
```

Now add the remaining 3 fields.

### Part 2: HTML form

Having defined the form class, you next need to generate the form in the index.html template using a combination of HTML and Jinja.

You already have a Jinja variable that can be used to show the result of the prediction.

An HTML form is enclosed in form tags like this:

```html
<form method="POST" action="/">
    .... form fields go here ...
</form>
```

`method=` specifies the HTTP method to use when the form is submitted.

`action=` determines what action to run when the form is submitted. In this case it is going to back to the homepage route "/".

The basic syntax for a form that is generated from a Flask-WTF class is shown in the Flask-WTF documentation as follows. This defines a form with one field called 'name'. The CSRF token will be required at a later stage. If you want to learn more about CSRF [this article](https://testdriven.io/blog/csrf-flask/) explains it with specific reference to Flask apps:

```html
<form method="POST" action="/">
    {{ form.csrf_token }}
    {{ form.name.label }} {{ form.name(size=20) }}
    <input type="submit" value="Go">
</form>
```

Your form might look more like this:

```html
<form method="GET" action="/">
    {{ form.csrf_token }}
    {{ form.sepal_length.label }} {{ form.sepal_length(size=10) }}
    {{ form.sepal_width.label }} {{ form.sepal_width(size=10) }}
    {{ form.petal_length.label }} {{ form.petal_length(size=10) }}
    {{ form.petal_width.label }} {{ form.petal_width(size=10) }}
    <input type="submit" value="Predict species">
</form>
```

As you added validation to the fields, you need to have a way to display the error text if it fails validation. The code to add to each field is like the following. This introduces [Jinja control structures](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-control-structures) 'if' and 'for' :

```jinja
{{ form.sepal_length.label }}
{{ form.sepal_length }}
{% if form.sepal_length.errors %}
<ul class="text-warning">
    {% for error in form.sepal_length.errors %}
    <li>{{ error }}</li>
    {% endfor %}
</ul>
{% endif %}
```

You will need to add this for each of the 4 fields. Your form code is now quite long!

Finally, add a paragraph tag after the form that will display the text result of the prediction. Again this is a combination of HTML and Jinja variable.

`<p>{{ prediction_text }}</p>`

If you try to run the home page now you will see an error displayed. Try it.

This is because you defined variables `form.sepal_length` etc but have not yet passed anything to the template Jinja that lets it know what the 'form' object is. To this you need to edit the index route to pass a form object.

To see changes in the HTML files you will need to stop (Ctrl C in VS Code terminal) and restart the Flask app `python -m flask --app 'iris_app:create_app()' --debug run`.

### Part 3: Modify the "/" route

The "/" route in `routes.py` is currently defined as a GET method, which means the values for the variables can be added to the URL rather than in the request body. For a longer, or more secure form you would use the POST method instead.

You just created the form in HTML with a POST method so you need to change the "/" index route to acceept both the GET and POST methods like this:

```python
@app.route("/", methods=["GET", "POST"])
def index():
```

The example given in the Flask-WTF documentation for a route is:

```python
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)
```

This says when then submit route is called, create a MyForm object and pass it to the submit template so the page is generated with a new form. When the form is submitted, if it passes any validation rules defined in the form class, then go to the success route. If it does not pass the validation, return to the submit route with the form.

You want slightly different logic. The logic for the index function is now:

- When the index route is called without any other data being passed, generate a form object and pass it to the index.html template to render the page with an empty form.

- If the index route is called when a form is submitted then if the form passes the validation defined in the form class, then use the values from the fields in the form to get a prediction. Return the prediction as text and display it in the index page.

- If the form does not pass validation, return to the index page with the form and display any errors next to the fields.

You can reference the form values by using form.fieldname.data e.g.`petal_length = form.petal_length.data`

Here is a skeleton structure, try and add in the missing code described in the comments:

```python
from iris_app.forms import PredictionForm


@app.route("/")
def index():
    """Create the homepage"""
    # Create an instance of the form using your form class
    form = PredictionForm()

    if form.validate_on_submit():
        # Get the 4 values from the form fields and assign them to a list variable
        # You can access a form field value using the syntax: form_name.field_name.data e.g. form.sepal_length.data

        # Get a prediction result (which is a string) by calling the `make_prediction(flower_values)` method where `flower_values` is the list variable you created in the step above

        # Render a version of the index template that has both the form and the prediction text variable
        return render_template("index", form=form, prediction_text=prediction_result)
    
    # If the form is not submitted, or if it fails validation, render the index with just the form
    return ....
```

See if you can work out how to add the code to the route yourself.

If you get stuck have a look at the completed code in week 9.

If the form works, try the following sets of values to see what the prediction is:

- 5.0,3.3,1.4,0.2 (setosa)

- 7.0,3.2,4.7,1.4 (versicolor)

- 5.9,3.0,5.1,1.8 (virginica)

You no longer need the "/predict" route so you could delete this if you wish.

## Activity 2: Add a database to the application

If you are adding additional features to your app you may need to store data in a database.

To do this you will use the Flask-SQLAlchemy library which you can install using `pip install flask-sqlalchemy`.

SQLAlchemy allows you to work with database rows as if they were objects (classes).

The logical steps for this activity are:

1. Create a sqlite database file in the data folder of the iris_app containing the iris dataset.
2. Modify the create_app function to initialise the database:
    - Create a SQLAlchemy instance in __initi__.py before the create_app() function.
    - Add configuration parameters to the Flask app instance to tell it the location of the database file and to not track modifications.
    - Modify the `create_app` function so that after the Flask app instance is created, it is registered to the SQLAlchemy instance.
    - Modify the `create_app` function after the Flask app is registered to the SQLAlchemy instance to reference the tables in the database (you need this so that the app can map the tables to Python classes).
3. Define the Python classes ('models' in our Flask app) that will map to the data in the iris data.

### 1. Create a SQLite database from a csv file

The code for this is given you in `csv_to_sqlite.py`. There are many ways to save csv as sqlite. The following uses libraries you should be familiar with from COMP0035, namely pandas and pathlib; and introduces some sqlalchemy code.

Sqlachemy is used to create the database engine. The engine handles the connection to the database file and operates as if a sqlite database.

```python
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

# Define the database file name and location
db_file = Path(__file__).parent.joinpath("iris.db")

# Create a connection to file as a SQLite database (this automatically creates the file if it doesn't exist)
engine = create_engine("sqlite:///" + str(db_file), echo=False)

# Read the iris data to a pandas dataframe
iris_file = Path(__file__).parent.joinpath("iris.csv")
iris = pd.read_csv(iris_file)

# Write the data to a table in the sqlite database (data/iris.db)
iris.to_sql("iris", engine, if_exists="append", index=False)
```

The iris dataset has a single table with no relationships between the tables. The REST version of this activity includes a dataset with multiple tables and relationships if you wish to see an example of this.

### 2. Modify the create_app function to initialise the database

Refer to the [Flask-SQLAlchemy documentation for the configuration](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#configure-the-extension).

Modify the `create_app` function to create an instance of SQLAlchemy. There are two ways to do this in the Flask-SQLAlchemy documentation. Let's use the version that creates the global instance and then initialises it for the Flask app.

The following is the code needed in `iris_app/__init__.py`

```python
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Iris_app folder
PROJECT_ROOT = Path(__file__).parent

# Create a global SQLAlchemy object
db = SQLAlchemy()


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "YY3R4fQ5OmlmVKOSlsVHew"
    # configure the SQLite database location
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
        PROJECT_ROOT.joinpath("data", "iris.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    # Initialise SQLAlchemy extension for the Flask app
    db.init_app(app)
    
    with app.app_context():
        from . import routes

        # Create tables in the database (if not already existing)
        from .models import Iris, User
        db.create_all()

    return app
```

You will see warnings as at this point you have not created `Iris` and `User` nor the models python file.

### 3. Define the Python classes ('models')

Create a python file. This is often named `models.py` but doesn't have to be.

Add the following code to create a class that represents the data in the database.

```python
from iris_app import db


class Iris(db.Model):
    """Iris class"""

    __tablename__ = "iris"
    rowid = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    species = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """
        Returns the attributes of an iris as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.sepal_length}, {self.sepal_width}, {self.petal_length}, {self.petal_width}, {self.species}>"
```

`db` you created in step 2 in the `iris_app/__init__.py` and is the SQLAlchemy database

The syntax for the table is from the [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application). The table is defined as follows:

- Define the class with an appropriate name.
- The tablename should match the tablename in the databse.
- The column names should match the column names used in the database.
- The column datatypes should match the data types used in the database.

If you want to create another table, e.g. if you want to start allowing people to register accounts, then you can
define a new table in `models.py`. The following is simplistic and you would not in practice store passwords as plain text.

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text(), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
```

Stop and re-run the app. As you set `app.config["SQLALCHEMY_ECHO"] = True` this prints to the Terminal all the SQL statements that are generated. You should see the create user table SQL printed, and if you open the iris.db file in the iris_app/data folder you should see the table has been added.

## Activity 3: Use the database contents in pages of your app

### Part 1: Query the data to generate a page

There are two steps:

1. Define a route that use Flask-SQLAlchemy queries to find data from the database.
2. Display the results by passing the data to a template that uses Jinja to add the data to the HTML page.

Let's generate a new page, `iris.html`, and print all the rows from the database to it.

1. Create a new route in iris_app/routes.py

This is a GET route.

When the route is called:

- query the iris table in the database. [Query syntax shown here](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#query-the-data) and we will use a query as for the first example that lists all users.
- pass the results to a page template, "iris.html" that will render all the rows in an HTML table

The code will look like this:

```python
from iris_app import db
from iris_app.models import Iris

@app.route("/iris")
def iris_list():
    iris = db.session.execute(db.select(Iris).scalars())
    return render_template("iris.html", iris_list=iris)
```

2. Create a page template to display the irises as a table

Create a new template called "iris.html" that extends the base layout.

Use HTML to define a table and a heading row.

Use Jinja code to iterate the `iris_list` variable that you passed to the `render_template` function, and add a row to the table for each iris in the list. This uses Jinja for loop `{% for iris in iris_list %} some code {% endfor %}`.

```jinja
{% extends 'layout.html' %}
{% set title = 'Iris Dataset' %}
{% block content %}

<table>
    <tr>
        <th>Species</th>
        <th>Sepal length</th>
        <th>Sepal width</th>
        <th>Petal length</th>
        <th>Petal width</th>
    </tr>
    {% for iris in iris_list %}
    <tr>
        <td>{{iris.species}}</td>
        <td>{{iris.sepal_length}}</td>
        <td>{{iris.sepal_width}}</td>
        <td>{{iris.petal_length}}</td>
        <td>{{iris.petal_width}}</td>
    </tr>
    {% endfor %}
</table>

{% endblock %}
```

You can experiment with Bootstrap classes if you want to make the table look nicer.

Now run the app and go to <http://127.0.0.1:5000/iris>

###  Part 2: Add a new user to the database

To capture new data, or update existing data in your app:

1. Define the form as python classes using FlaskWTF. You already did this for the prediction form.
2. Create a form in an HTML `template` using Flask-WTF forms. You already did this for the prediction form.
3. Add a GET & POST route the uses the details from the form in the request, creates a new object, and saves the object to the database.

Add a simple user registration form.

Add code to create a new form to `forms.py` using [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/#creating-forms):

```python
class UserForm(FlaskForm):
    """Fields to a form to input the values required for adding a new user account"""

    email = StringField("email", validators=[DataRequired()])
    password = StringField("name", validators=[DataRequired()])

```

Create a template page for adding a new user e.g. `register.html`:

```jinja
{% extends 'layout.html' %}
{% set title = 'Register' %}
{% block content %}

<form method="POST" class="form">
    {{ form.csrf_token }}
    <div class="form-group">
        {{ form.email.label }}
        {{ form.email(class="form-control") }}
        {% if form.email.errors %}
        <ul class="text-warning">
            {% for error in form.email.errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
    <div class="form-group">
        {{ form.password.label }}
        {{ form.password(class="form-control") }}
        {% if form.password.errors %}
        <ul class="text-warning">
            {% for error in form.password.errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
    <input type="submit" value="Register">
</form>

{% endblock %}
```

3. Add a route to save the new user detail to the database

Create a new GET & POST route that:

- checks if the form was submited, if not present a page with an empty form
- if the form was submitted, then check it passes the validation
- if it does then create a new user by accessing the form field values in the request and create a new object using these
- save the new object to the database
- return basic HTML message showing the details of the created user

```python
from iris_app.forms import UserForm
from iris_app.models import User

@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        text = f"<p>You are registered! {repr(new_user)}</p>"
        return text
    return render_template("register.html", form=form)
```

Run the app, go to <http://127.0.0.1:5000/register> and complete and submit the form.

## Going further

If you want to extend your skills consider:

- Add [Boostrap form classes](https://getbootstrap.com/docs/5.2/forms/overview/) to modify the style of the form.

- Rather than adding each of the form field to index.html and each of the error message fields, you can add a macro that will autogenerate all the fields for a form using a helper function `_formhelpers.html` as [suggested here](https://flask.palletsprojects.com/en/2.2.x/patterns/wtforms/#forms-in-templates).

- Try and create a 'contact us' form with fields for the person's email address and their request text; and a submit button. On submit, if it passes validation return something like "thank you for your message". You will need to create a form class, a template and a route.

Third-party examples:

- <https://carolinacamassa.tech/blog/posts/flask-ml-app/>
