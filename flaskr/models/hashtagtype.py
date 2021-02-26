from flaskr import db


class HashtagType(db.Model):
    __tablename__ = 'HashtagType'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('Hashtag.id'), nullable=False)
    hashtag = db.relationship('Hashtag', foreign_keys=[hashtag_id])
    tweet_id = db.Column(db.Integer, db.ForeignKey('Tweet.id'), nullable=False)
    tweet = db.relationship('Tweet', foreign_keys=[tweet_id])

    def serialize(self):
        return {
            'id': self.id,
            'hashtag_id': self.hashtag_id,
            'tweet_id': self.tweet_id
        }
