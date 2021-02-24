from flaskr import app, db
from flask import jsonify
from flaskr import helper

from flask import (
    redirect, render_template, request, session, url_for
)


@app.route('/')
def test():
    return render_template('base.html')


@app.route('/users', methods=['POST'])
def create_user():
    arg = request.form
    return jsonify(helper.create_user(arg).serialize()), 201


@app.before_first_request
def init():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('hi')
        return helper.register_helper(request.form)
    print('bye')
    return render_template('auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        return helper.login_helper(request.form)
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required():
    if session.get('currentUser') is None:
        return redirect(url_for('auth.login'))

