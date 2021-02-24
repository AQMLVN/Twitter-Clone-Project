from flaskr import db


class Like(db.Model):
    __tablename__ = 'Like'
    id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('User', foreign_keys=['user_id'])
    tweet_id = db.Column(db.Integer, db.ForeignKey('Tweet.id'), nullable=False)
    tweet = db.relationship('Tweet', foreign_keys=['tweet_id'])

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tweet_id': self.tweet_id
        }
