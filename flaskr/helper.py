from flask import redirect, url_for, flash, session
from flaskr import db
from flaskr.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash


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
        return redirect(url_for('test'))    # Function name in route.py (endpoints)

    flash(error)
    return redirect(url_for('login'))


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def create_user(params):
    user = User(username=params['username'], password=generate_password_hash(params['password']))
    db.session.add(user)
    db.session.commit()
    return user
