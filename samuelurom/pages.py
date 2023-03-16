from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_from_directory
)
from werkzeug.exceptions import abort

from flask_ckeditor import CKEditor
from wtforms import TextAreaField

from werkzeug.utils import secure_filename
import os

from flask_mail import Mail, Message

from samuelurom.auth import login_requried
from samuelurom.db import get_db

# create blueprint named `page`
blueprint = Blueprint('page', __name__)

# Initialize new CKEditor instance
ckeditor = CKEditor()

# initialie new Mail instance
mail = Mail()
admin_email = 'hello@samuelurom.com'

# set upload folder and allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


# check if a file extension is valid
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/')
def index():
    db = get_db()
    recent_posts = db.execute(
        '''SELECT post.id, post_title, post_description, post_url, created_date, author_id, full_name
            FROM post JOIN user ON post.author_id = user.id
            ORDER BY created_date DESC
        '''
    ).fetchmany(2)
    return render_template('pages/index.html', recent_posts=recent_posts)


@blueprint.route('/blog/')
def blog():
    db = get_db()
    posts = db.execute(
        '''SELECT post.id, post_title, post_description, post_url, created_date, featured_image, author_id, full_name
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
        post_url = request.form['post_url']
        post_description = request.form['post_description']
        post_content = request.form['ckeditor']
        featured_image = request.files['featured_image']
        published_status = request.form['published_status']

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

        # check if featured image is added to form and if UPLOAD_FOLDER directory eists
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        if featured_image and allowed_file(featured_image.filename):
            featured_image_name = secure_filename(
                featured_image.filename).lower()
            featured_image.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], featured_image_name))

        if error is not None:
            flash(error)
        else:
            # connect to database and insert record to post table
            db = get_db()
            db.execute(
                '''INSERT INTO post (post_title, post_url, post_description, post_content, published_status, featured_image, author_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (post_title, post_url, post_description,
                 post_content, published_status, featured_image_name, g.user['id'],)
            )
            db.commit()
            return redirect(url_for('page.blog'))

    return render_template('pages/create.html')


@blueprint.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


def get_post(id=None, url=None, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.

    :param ``id``: id of post to get
    :param ``check_author``: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    # connect to db
    db = get_db()

    if id:
        post = db.execute(
            """SELECT post.id, post_title, post_url, post_description, post_content, created_date, featured_image, author_id, full_name
                FROM post JOIN user ON post.author_id = user.id
                WHERE post.id = ?
            """, (id,)
        ).fetchone()

        if check_author and post['author_id'] != g.user['id']:
            abort(403)

    elif url:
        post = db.execute(
            """SELECT post.id, post_title, post_url, post_description, post_content, created_date, featured_image, author_id, full_name
                FROM post JOIN user ON post.author_id = user.id
                WHERE post.post_url = ?
            """, (url,)
        ).fetchone()

    if post is None:
        abort(404, f"Oops! That page doesn't exist.")

    return post


@blueprint.route('/<post_url>/')
def single_post(post_url):
    post = get_post(url=post_url)
    return render_template('pages/single_post.html', post=post)


@blueprint.route('/<int:id>/edit/', methods=('GET', 'POST'))
@login_requried
def edit(id):
    """Update a post if the current user is the author."""

    # get the post by id
    post = get_post(id=id)

    if request.method == 'POST':
        # get submitted form data
        post_title = request.form['post_title']
        post_url = request.form['post_url']
        post_description = request.form['post_description']
        post_content = request.form['ckeditor']
        featured_image = request.files['featured_image']
        published_status = request.form['published_status']

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

        # check if featured image is added to form and if UPLOAD_FOLDER directory eists
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        if featured_image and allowed_file(featured_image.filename):
            featured_image_name = secure_filename(
                featured_image.filename).lower()
            featured_image.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], featured_image_name))

        if error is not None:
            flash(error)
        else:
            # connect to database and insert record to post table
            db = get_db()
            db.execute(
                '''UPDATE post
                    SET post_title = ?, post_url = ?, post_description = ?, post_content = ?, featured_image =?, published_status = ?
                    WHERE id = ?
                ''',
                (post_title, post_url, post_description,
                 post_content, featured_image_name, published_status, id,)
            )
            db.commit()
            return redirect(url_for('page.blog'))

    return render_template('pages/edit.html', post=post)


@blueprint.route('/<int:id>/delete', methods=('POST',))
@login_requried
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id=id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('page.blog'))


@blueprint.route('/contact/', methods=('GET', 'POST'))
def contact():
    """Send contact form by email.
    """
    sender_name = None

    if request.method == 'POST':
        sender_name = request.form['name']
        sender_email = request.form['email']
        contact_subject = request.form['subject']
        contact_message = request.form['message']

        # initialize error
        error = None

        if not sender_name:
            error = 'Sender name required.'
        elif not sender_email:
            error = 'Sender email required.'
        elif not contact_subject:
            error = 'Subject required.'
        elif not contact_message:
            error = 'Message can not be empty.'

        if error is not None:
            flash(error)
        else:
            new_message = Message(contact_subject, recipients=[
                admin_email], sender=sender_name)
            new_message.body = f'''
From: {sender_name}<{sender_email}>

{contact_message}'''
            mail.send(new_message)
            current_url = request.path

    return render_template('pages/contact.html', sender_name=sender_name)
