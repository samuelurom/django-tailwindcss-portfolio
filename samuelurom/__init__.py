import os
from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # load the configuration settings for secrete key and mail server
    from . import config
    app.config.from_mapping(config.config)

    # store database in instance folder
    app.config['DATABASE'] = os.path.join(
        app.instance_path, 'samuelurom.sqlite')

    # configure upload folder
    path = os.getcwd()
    app.config['UPLOAD_FOLDER'] = os.path.join(path, 'uploads')

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
    # bind CKEditor instance to app
    pages.ckeditor.init_app(app)
    app.register_blueprint(pages.blueprint)
    app.add_url_rule('/', endpoint='index')

    # bind Mail instance to app
    pages.mail.init_app(app)

    return app
