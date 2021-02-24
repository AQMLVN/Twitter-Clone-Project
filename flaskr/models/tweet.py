from flaskr import db


class Tweet(db.Model):
    __tablename__ = 'Tweet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id
        }
