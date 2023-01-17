from flask import render_template, current_app as app


@app.route("/")
def index():
    """Creates a homepage for the paralympic app"""
    return render_template("index.html")
