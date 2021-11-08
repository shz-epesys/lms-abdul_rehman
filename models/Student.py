# from .models import db
# from datetime import datetime

# class Student(db.Model):
#     __tablename__ = 'students'
    
#     id = db.Column(db.Integer, primary_key=True)
#     reg_no = db.Column(db.Integer, unique=True, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     is_hidden = db.Column(db.Boolean(), default=False)
#     student_class = db.relationship("StudentClass", backref='students')
#     created_at = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False
#     )
