from datetime import datetime
from enum import unique

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression
db = SQLAlchemy()



class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(60), nullable=False)
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
    users = db.relationship("User", backref='roles')


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(1000),  nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True)
    dob = db.Column(db.DateTime, default=None)
    contact_no = db.Column(db.Integer)
    address = db.Column(db.String(100))
    city = db.Column(db.String(60))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
    created_at = db.Column(
        db.DateTime, nullable=False,server_default =expression.text('NOW()')
    )

    students = db.relationship("Student", backref='users', uselist=False)
    teachers = db.relationship("Teacher", backref='users', uselist=False)


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
    student_class = db.relationship("StudentClass", backref='students')
    created_at = db.Column(
        db.DateTime,server_default = expression.text('NOW()'), nullable=False
    )


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(100), unique=True, nullable=False)
    degree = db.Column(db.String(60),  nullable=False)
    experience = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
    teacher_class = db.relationship("TeacherClass", backref='teachers')
    created_at = db.Column(
        db.DateTime, nullable=False,server_default = expression.text('NOW()')
    )


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    name = db.Column(db.String(60), nullable=False)
    no_of_students = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(60))
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
    reading_material = db.relationship("ReadingMaterial", backref='classes')
    announcement = db.relationship("Announcement", backref='classes')
    created_at = db.Column(
        db.DateTime, server_default = expression.text('NOW()'), nullable=False
    )


class TeacherClass(db.Model):
    __tablename__ = 'teacher_class'
    
    id =db.Column(db.Integer, primary_key = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
   

class StudentClass(db.Model):
    __tablename__ = 'student_class'

    id =db.Column(db.Integer, primary_key = True)
    students_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())


class ReadingMaterial(db.Model):
    __tablename__ = 'reading_materials'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    file_name = db.Column(db.String(60), nullable=False)
    file_path = db.Column(db.String(600), nullable=False)
    file_type = db.Column(db.String(60), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default = expression.text('NOW()'), nullable=False)

    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(1000))
    created_at = db.Column(
        db.DateTime, server_default = expression.text('NOW()'), nullable=False
    )
    is_hidden = db.Column(db.Boolean(),nullable=False, server_default=expression.false())
