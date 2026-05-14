from database import db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(255))

    role = db.Column(db.String(20))

    bio = db.Column(db.Text, nullable=True)

    avatar_url = db.Column(db.String(255), nullable=True)


class RefreshToken(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(db.String(500))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )