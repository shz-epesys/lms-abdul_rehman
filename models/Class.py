# from .models import db
# from datetime import datetime

# class Class(db.Model):
#     __tablename__ = 'classes'

#     id = db.Column(db.Integer, primary_key=True)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
#     name = db.Column(db.String(60), nullable=False)
#     no_of_students = db.Column(db.Integer, nullable=False)
#     image = db.Column(db.String(60))
#     is_hidden = db.Column(db.Boolean(), default=False)
#     reading_material = db.relationship("ReadingMaterial", backref='classes')
#     announcement = db.relationship("Announcement", backref='classes')
#     created_at = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False
#     )
