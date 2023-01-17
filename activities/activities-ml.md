# Week 3 activities (ML version)

Check you can run the app before you start:
`python -m flask --app 'iris_app:create_app()' --debug run`

The activities include:

- [Add an iris prediction form to the index.html template](#add-a-form-to-the-indexhtml-template)

## Add an iris prediction form to the index.html template

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

Having defined the form class, you next need to generate the form in the index.html template using a combination of HTML and Jinja. You can also add a Jinja variable that can be used to show the result of the prediction.

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

If you get stuck have a look at the completed code in week 4.

If the form works, try the following sets of values to see what the prediction is:

- 5.0,3.3,1.4,0.2 (setosa)

- 7.0,3.2,4.7,1.4 (versicolor)

- 5.9,3.0,5.1,1.8 (virginica)

You no longer need the "/predict" route so you could delete this if you wish.

## Going further

If you want to extend your skills consider:

- Add [Boostrap form classes](https://getbootstrap.com/docs/5.2/forms/overview/) to modify the style of the form.

- Rather than adding each of the form field to index.html and each of the error message fields, you can add a macro that will autogenerate all the fields for a form using a helper function `_formhelpers.html` as [suggested here](https://flask.palletsprojects.com/en/2.2.x/patterns/wtforms/#forms-in-templates).

- Try and create a 'contact us' form with fields for the person's email address and their request text; and a submit button. On submit, if it passes validation return something like "thank you for your message". You will need to create a form class, a template and a route.

Third-party examples:

- <https://carolinacamassa.tech/blog/posts/flask-ml-app/>
