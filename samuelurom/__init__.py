import os
from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # default secret - should be overridden by instance config
        SECRET_KEY='y$B&E)H@McQfTjWnZq4t7w!z%C*F-JaN',
        # store database in instance folder
        DATABASE=os.path.join(app.instance_path, 'samuelurom.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
