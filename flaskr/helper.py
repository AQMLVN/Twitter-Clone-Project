from flask import redirect, url_for, flash, session
from flaskr import db
from flaskr.models.user import User
from flaskr.models.tweet import Tweet
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort


def register_helper(params):
    error = None

    if not params['username']:
        error = 'Username is required.'
    elif not params['password']:
        error = 'Password is required.'
    elif get_user_by_username(params['username']):
        error = 'User {} is already registered.'.format(params['username'])
    else:
        create_user(params)

    if not error:
        return redirect(url_for('login'))

    flash(error)
    return redirect(url_for('register'))


def login_helper(params):
    error = None
    user = get_user_by_username(params['username'])

    if not user:
        error = 'Incorrect username.'
    elif not check_password_hash(user.password, params['password']):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['currentUser'] = params['username']
        return redirect(url_for('index'))    # Function name in route.py (endpoints)

    flash(error)
    return redirect(url_for('login'))


def create_helper(params):
    error = None
    title = params['title']
    body = params['body']

    if not title:
        error = 'Title is required.'
    elif not body:
        error = 'Body is required.'

    if error is None:
        tweet = Tweet(title=title, body=body, user_id=get_user_by_username(session['currentUser']).id)
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('index'))

    flash(error)
    return redirect(url_for('create'))


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_id(username):
    return User.query.filter_by(username=username)


def create_user(params):
    user = User(username=params['username'], password=generate_password_hash(params['password']))
    db.session.add(user)
    db.session.commit()
    return user


def get_post(id, check_author=True):
    post = Tweet.query.filter_by(id=id).first()

    if not post:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and (post['user_id'] != get_user_by_username(session['currentUser']).id):
        abort(403)

    return post


def get_posts(author_id):
    posts = Tweet.query.filter_by(user_id=author_id).all()
    return posts


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['currentUser'] is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
