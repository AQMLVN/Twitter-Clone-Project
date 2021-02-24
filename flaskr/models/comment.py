from flaskr import db


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    tweet_id = db.Column(db.Integer, db.ForeignKey('Tweet.id'), nullable=False)
    tweet = db.relationship('Tweet', foreign_keys=['tweet_id'])
    p_comment = db.Column(db.Integer, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tweet_id': self.tweet_id,
            'p_comment': self.p_comment
        }
