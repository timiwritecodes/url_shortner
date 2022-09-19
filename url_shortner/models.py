from url_shortner import db
from datetime import datetime


class ShortUrls(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    long_url = db.Column(db.String(), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

