from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, unique=False, nullable=True)
    refresh_token = db.Column(db.String, unique=False, nullable=True)
    expiry = db.Column(db.String, unique=False, nullable=True)
    access_token = db.Column(db.String, unique=False, nullable=True)
    github_oauth_token = db.Column(db.String, unique=False, nullable=True)