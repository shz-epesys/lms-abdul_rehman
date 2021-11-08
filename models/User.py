# from datetime import datetime
# from .models import db


# class Role(db.Model):
#     __tablename__ = 'roles'

#     id = db.Column(db.Integer, primary_key=True)
#     role_name = db.Column(db.String(60), nullable=False)
#     is_hidden = db.Column(db.Boolean(), default=False)
#     users = db.relationship("User", backref='roles')


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(60), unique=True, nullable=False)
#     password = db.Column(db.String(1000),  nullable=False)
#     first_name = db.Column(db.String(60), nullable=False)
#     last_name = db.Column(db.String(60), nullable=False)
#     email = db.Column(db.String(60), unique=True)
#     dob = db.Column(db.DateTime, default=None)
#     contact_no = db.Column(db.Integer)
#     address = db.Column(db.String(100))
#     city = db.Column(db.String(60))
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#     is_hidden = db.Column(db.Boolean(), default=False)
#     created_at = db.Column(
#         db.DateTime, default=datetime.utcnow, nullable=False
#     )

#     students = db.relationship("Student", backref='users', uselist=False)
#     teachers = db.relationship("Teacher", backref='users', uselist=False)
