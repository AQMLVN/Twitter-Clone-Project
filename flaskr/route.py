from flaskr import app, db
from flask import jsonify
from flaskr import helper
from flaskr.helper import login_required, remove_html_tags
from flask import (
    redirect, render_template, request, session, url_for
)


@app.route('/')
def index():
    posts = []
    if session.get('currentUser', None):
        posts = helper.get_posts(helper.get_user_by_username(session['currentUser']).id)
    return render_template('feed/index.html', posts=posts)


@app.route('/hashtag/<int:id>')
def hashtag(id):
    posts = helper.get_posts_by_hashtag(id)
    return render_template('feed/hashtag.html', posts=posts)


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


@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = helper.get_post(id)
    post.body = remove_html_tags(post.body)

    if request.method == 'POST':
        helper.remove_hashtag(id)
        return helper.update_helper(post, request.form)

    return render_template('feed/update.html', post=post)


@app.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    helper.delete_helper(id)
    return redirect(url_for('index'))
