from flaskr import app, db
from flask import jsonify
from flaskr import helper
from flaskr.helper import login_required
from flask import (
    redirect, render_template, request, session, url_for
)


@app.route('/')
def index():
    posts = []
    if session.get('currentUser', None):
        posts = helper.get_posts(helper.get_user_by_username(session['currentUser']).id)
    return render_template('feed/index.html', posts=posts)


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
        return helper.register_helper(request.form)
    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return helper.login_helper(request.form)
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        return helper.create_helper(request.form)
    return render_template('feed/create.html')


