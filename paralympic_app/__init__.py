from flask import Flask

from . import api_routes


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "YY3R4fQ5OmlmVKOSlsVHew"

    # Register the api blueprint for the routes in api_routes.py
    from .api_routes import bp

    app.register_blueprint(bp)

    # Register the routes in paralypic_routes.py
    with app.app_context():
        from . import paralympic_routes

    return app
