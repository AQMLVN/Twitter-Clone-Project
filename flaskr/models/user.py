from flaskr import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
