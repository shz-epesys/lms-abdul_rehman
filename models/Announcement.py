# from .models import db
# from datetime import datetime

# class Announcement(db.Model):
#     __tablename__ = 'announcements'

#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
#     title = db.Column(db.String(60), nullable=False)
#     description = db.Column(db.String(1000))
#     created_at = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False
#     )
#     is_hidden = db.Column(db.Boolean(), default=False)
