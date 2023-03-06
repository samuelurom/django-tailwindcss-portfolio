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

    # import and register the database commands
    # run ``flask --app [project_folder] init-db`` to initialize the database
    from . import db
    db.init_app(app)

    # Import and register auth blueprint to the app
    from . import auth
    app.register_blueprint(auth.blueprint)

    # import and register page blueprint to the app
    # page blueprint does not have a url_prefix. so index view will be at /
    from . import pages
    app.register_blueprint(pages.blueprint)
    app.add_url_rule('/', endpoint='index')

    return app
