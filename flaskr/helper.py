from flask import redirect, url_for, flash, session
from flaskr import db
from flaskr.models.hashtag import Hashtag
from flaskr.models.hashtagtype import HashtagType
from flaskr.models.user import User
from flaskr.models.tweet import Tweet
import functools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
import re


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
        hashtags = re.findall(r'#\w+', body)
        for ht in hashtags:
            hashtag = get_hashtag(ht)
            if not hashtag:
                hashtag = Hashtag(value=ht)
                db.session.add(hashtag)
                db.session.commit()
            hashtag_type = HashtagType(hashtag_id=hashtag.id, tweet_id=tweet.id)
            db.session.add(hashtag_type)
            db.session.commit()

        tweet.body = link_hashtag(tweet.body, hashtags)

        db.session.commit()

        return redirect(url_for('index'))

    flash(error)
    return redirect(url_for('create'))


def update_helper(post, params):
    error = None
    title = params['title']
    body = params['body']

    if not title:
        error = 'Title is required.'
    elif not body:
        error = 'Body is required.'

    if error is None:
        hashtags = re.findall(r'#\w+', body)
        for ht in hashtags:
            hashtag = get_hashtag(ht)
            if not hashtag:
                hashtag = Hashtag(value=ht)
                db.session.add(hashtag)
                db.session.commit()
            hashtag_type = HashtagType(hashtag_id=hashtag.id, tweet_id=post.id)
            db.session.add(hashtag_type)
            db.session.commit()
        post.title = title
        post.body = body
        post.body = link_hashtag(post.body, hashtags)
        db.session.commit()
        return redirect(url_for('index'))

    flash(error)
    return redirect(url_for('update'))


def delete_helper(id):
    post = get_post(id)
    remove_hashtag(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))


def remove_hashtag(post_id):
    hashtag = db.session.query(
        Hashtag, HashtagType
    ).join(
        HashtagType
    ).filter(
        HashtagType.tweet_id == post_id
    ).filter(
        Hashtag.id == HashtagType.hashtag_id
    ).all()

    for ht, htt in hashtag:
        db.session.delete(ht)
        db.session.delete(htt)
        db.session.commit()


def link_hashtag(body, hashtags):
    for ht in hashtags:
        hashtag_id = Hashtag.query.filter_by(value=ht).first()
        ht_redirect = '<a href= \"/hashtag/'+str(hashtag_id.id)+'\">' + ht + '</a>'
        body = body.replace(ht, ht_redirect)
    return body


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


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

    if check_author and (post.user_id != get_user_by_username(session['currentUser']).id):
        abort(403)

    return post


def get_posts(author_id):
    posts = db.session.query(
        Tweet, User
    ).join(
        User
    ).filter(
        Tweet.user_id == User.id
    ).all()

    return posts


def get_posts_by_hashtag(hashtag_id):
    test = db.session.query(
        Tweet, User
    ).join(
        HashtagType
    ).join(
        User
    ).filter(
        Tweet.id == HashtagType.tweet_id
    ).filter(
        HashtagType.hashtag_id == hashtag_id
    ).all()

    return test


def get_hashtag(hashtag):
    return Hashtag.query.filter_by(value=hashtag).first()


def get_hashtag_type(id):
    return HashtagType.query.filter_by(hashtag_id=id).all()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['currentUser'] is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
