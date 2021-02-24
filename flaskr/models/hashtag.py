from flaskr import db


class Hashtag(db.Model):
    __tablename__ = 'Hashtag'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'value': self.value
        }
