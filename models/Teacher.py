# from .models import db
# from datetime import datetime

# class Teacher(db.Model):
#     __tablename__ = 'teachers'

#     id = db.Column(db.Integer, primary_key=True)
#     reg_no = db.Column(db.Integer, unique=True, nullable=False)
#     degree = db.Column(db.String(60),  nullable=False)
#     experience = db.Column(db.String(60), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     is_hidden = db.Column(db.Boolean(), default=False)
#     teacher_class = db.relationship("TeacherClass", backref='teachers')
#     created_at = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False
#     )
