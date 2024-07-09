
from app.database.db import db

class Interactions(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    response = db.Column(db.Text, nullable=True)
    empid = db.Column(db.Text, nullable=True)
    raw_question = db.Column(db.Text, nullable=True)
    date = db.Column(db.Text, nullable=True)
    isliked = db.Column(db.Boolean, nullable=True)