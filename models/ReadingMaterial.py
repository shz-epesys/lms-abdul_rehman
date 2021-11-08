# from .models import db
# from datetime import datetime

# class ReadingMaterial(db.Model):
#     __tablename__ = 'reading_materials'

#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
#     file_name = db.Column(db.String(60), nullable=False)
#     file_path = db.Column(db.String(600), nullable=False)
#     file_type = db.Column(db.String(60), nullable=False)
#     created_at = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False)

#     is_hidden = db.Column(db.Boolean(), default=False)
