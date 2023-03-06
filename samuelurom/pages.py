from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from samuelurom.auth import login_requried
from samuelurom.db import get_db

# create blueprint named `page`
blueprint = Blueprint('page_bp', __name__)


@blueprint.route('/')
def index():
    db = get_db()
    recent_posts = db.execute(
        '''SELECT post.id, post_title, post_description, post_url, created_date, author_id, full_name
            FROM post JOIN user ON post.author_id = user.id
            ORDER BY created_date DESC
        '''
    ).fetchmany(5)
    return render_template('pages/index.html', recent_posts=recent_posts)


@blueprint.route('/blog/')
def blog():
    db = get_db()
    posts = db.execute(
        '''SELECT post.id, post_title, post_description, post_url, created_date, author_id, full_name
            FROM post JOIN user ON post.author_id = user.id
            ORDER BY created_date DESC
        '''
    ).fetchall()
    return render_template('pages/blog.html', posts=posts)


@blueprint.route('/create/', methods=('GET', 'POST'))
@login_requried
def create():
    '''Create a new post for the current user.
    '''
    if request.method == 'POST':
        # get submitted form data
        post_title = request.form['post_title']
        post_description = request.form['post_description']
        post_content = request.form['post_content']
        post_url = request.form['post_url']

        # initialize the error variable
        error = None

        # check that empty fields are not submitted for `title` and `body`
        if not post_title:
            error = 'Title is required'
        elif not post_description:
            error = 'Meta description is required'
        elif not post_content:
            error = 'Post content cannot be empty'
        elif not post_url:
            error = 'Post URL is required'

        if error is not None:
            flash(error)
        else:
            # connect to database and insert record to post table
            db = get_db()
            db.execute(
                '''INSERT INTO post (post_title, post_description, post_content, post_url, author_id)
                    VALUES (?, ?, ?, ?, ?)
                ''',
                (post_title, post_description,
                 post_content, post_url, g.user['id'],)
            )
            db.commit()
            return redirect(url_for('blog'))

    return render_template('pages/create.html')
