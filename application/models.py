from application.app import app, db

from werkzeug.security import generate_password_hash, check_password_hash
import logging


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))

shared_with = db.Table('shared_with',
    db.Column('work_item_id', db.Integer, db.ForeignKey('work_item.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class WorkItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    estimated_time = db.Column(db.Integer, default=0)
    is_done = db.Column(db.Boolean, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with = db.relationship('User', secondary=shared_with, lazy='subquery', backref=db.backref('user', lazy=True))

# user - WorkItem
# 1       1
# 2       1
# 3       2
# 3       1

class SubTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_item.id'), nullable=False)


db.create_all()
db.init_app(app)