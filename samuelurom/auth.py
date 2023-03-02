import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from samuelurom.db import get_db

# create a blueprint named auth.
# the ``url_prefix`` will be prepended to all the urls associated with the blueprint.
blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register/', methods=('GET', 'POST'))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """

    if request.method == 'POST':
        # get the submitted username and password data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # connect to database
        db = get_db()

        # initialize variable to grab the error message
        error = None

        # check if fields are empty and grab the error
        if not username:
            error = 'Username is required!'
        elif not email:
            error = 'Email is required!'
        elif not password:
            error = 'Password is required!'

        # insert new user to database
        if error is None:
            try:
                # insert user with hashed password
                db.execute(
                    'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                    (username, email, generate_password_hash(password),)
                )

                # commit changes to database
                db.commit()
            except db.IntegrityError as e:
                # check the error message to determine which field caused the error
                if 'username' in str(e):
                    error = f'User {username} already exists!'
                elif 'email' in str(e):
                    error = f'Email {email} is already in use!'
                else:
                    error = 'An error occured. Please contact the administrator.'
            else:
                # redirect to login page
                return redirect(url_for('auth.login'))

        # flash stores the error message
        flash(error)

    return render_template('auth/register.html')


@blueprint.route('/login/', methods=('GET', 'POST'))
def login():
    """Login the user.
    Validates that the user exists in the database"""

    if request.method == 'POST':
        # get submitted username and password data
        username = request.form['username']
        password = request.form['password']

        # connect to database
        db = get_db()

        # initialize the error messages
        error = None

        # query the database for the user and store the `user` object
        user = db.execute(
            'SELECT id, username, password FROM user WHERE username = ?', (
                username,)
        ).fetchone()

        # validate username and securely compare `check_password_hash`
        if user is None:
            error = 'Username not found!'
        elif not check_password_hash(user['password'], password):
            error = 'Wrong password entered!'

        # add user to session if `error` is none
        if error is None:
            # store the user id in a new session and redirect to the `index` view
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        # flash stores the error message
        flash(error)

    return render_template('auth/login.html')


@blueprint.before_app_request
def load_logged_in_user():
    """This function runs before the view function, no matter what URL is requested.
    If a user id is stored in the session, load the user object from the database into ``g.user``.
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # connect to database and query database for user
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@blueprint.route('/logout/')
def logout():
    """Remove the ``user_id`` from session. ``load_logged_in_user`` will not load a user on subsequent requests.
    """
    session.clear()
    return redirect(url_for('index'))


def login_requried(view):
    """View decorator that redirects anonymous users to the login page.
    It returns a new view function that wraps the original view it is applied to.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
