from application.app import app, db

from werkzeug.security import generate_password_hash, check_password_hash
import logging


class WorkItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    estimated_time = db.Column(db.Integer, default=0)
    is_done = db.Column(db.Boolean, default=0)

class SubTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_item.id'), nullable=False)

