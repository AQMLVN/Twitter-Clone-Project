from flaskr import db


class HashtagType(db.Model):
    __tablename__ = 'HashtagType'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('Hashtag.id'), nullable=False)
    hashtag = db.Relationship('Hashtag', foreign_keys=['hashtag_id'])
    tweet_id = db.Column(db.Integer, db.ForeignKey('Tweet.id'), nullable=True)
    tweet = db.Relationship('Tweet', foreign_keys=['tweet_id'])
    comment_id = db.Column(db.Integer, db.ForeignKey('Comment.id'), nullable=True)
    comment = db.Relationship('Comment', foreign_keys=['comment_id'])

    def serialize(self):
        return {
            'id': self.id,
            'hashtag_id': self.hashtag_id,
            'tweet_id': self.tweet_id,
            'comment_id': self.comment_id
        }
