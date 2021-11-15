from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(60), nullable=False)
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )
    users = db.relationship("User", backref='roles')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(1000),  nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True)
    dob = db.Column(db.Date, default=None)
    contact_no = db.Column(db.Integer)
    address = db.Column(db.String(100))
    city = db.Column(db.String(60))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=expression.text('NOW()')
    )

    students = db.relationship("Student", backref='users', uselist=False)
    teachers = db.relationship("Teacher", backref='users', uselist=False)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )
    student_class = db.relationship("StudentClass", backref='students')
    created_at = db.Column(
        db.DateTime, server_default=expression.text('NOW()'), nullable=False
    )

    @staticmethod
    def serialize(query,many=False):
        if many:
            return [Student.serialize(x, many=True) for x in query]
        return {
            'studet_id': int(query['id']),
            'first_name': query['first_name'],
            'last_name': query['last_name'],
            'dob': query['dob'],
            'image': query['image'],
            'contact_no': query['contact_no'],
            'created_at': query['created_at'],
        }


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(100), unique=True, nullable=False)
    degree = db.Column(db.String(60),  nullable=False)
    experience = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )
    teacher_class = db.relationship("TeacherClass", backref='teachers')
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=expression.text('NOW()')
    )
    
    @staticmethod
    def serialize(query,many=False):
        if many:
            return [Teacher.serialize(x, many=True) for x in query]
        return {
            'id': int(query['id']),
            'first_name': query['first_name'],
            'last_name': query['last_name'],
            'dob': query['dob'],
            'reg_no': query['reg_no'],
            'experience': query['experience'],
            'image': query['image'],
            'contact_no': query['contact_no'],
            'created_at': query['created_at'],
        }



class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    name = db.Column(db.String(60), nullable=False)
    no_of_students = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(60))
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )
    reading_material = db.relationship("ReadingMaterial", backref='classes')
    announcement = db.relationship("Announcement", backref='classes')
    created_at = db.Column(
        db.DateTime, server_default=expression.text('NOW()'), nullable=False
    )

    # @staticmethod
    # def serialize_list(query, many=True):
    #     return [Class.serialize(x) for x in query]

    @staticmethod
    def serialize(query, many=False):
        if many:
            return [Class.serialize(x) for x in query]
        return {
            'class_id': int(query['id']),
            'name': query['name'],
            'teacher_name': query['first_name']+" "+query['last_name'],
            # 'last_name': query['last_name'],/
            'no_of_students': query['no_of_students'],
            'image': query['image'],
            'created_at': query['created_at'],
        }


class TeacherClass(db.Model):
    __tablename__ = 'teacher_class'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )


class StudentClass(db.Model):
    __tablename__ = 'student_class'

    id = db.Column(db.Integer, primary_key=True)
    students_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )


class ReadingMaterial(db.Model):
    __tablename__ = 'reading_materials'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    file_name = db.Column(db.String(60), nullable=False)
    file_path = db.Column(db.String(600), nullable=False)
    # file_type = db.Column(db.String(60), nullable=False,
    #                       server_default=expression.text('file'))
    created_at = db.Column(
        db.DateTime, server_default=expression.text('NOW()'), nullable=False
    )

    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )
    @staticmethod
    def serialize(query, many=False):
        if many:
            return [ReadingMaterial.serialize(x) for x in query]
        return {
            'id': int(query['id']),
            'file_name': query['file_name'],
            'file_path': query['file_path'],
            'created_at': query['created_at'],
        }


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(1000))
    created_at = db.Column(
        db.DateTime, server_default=expression.text('NOW()'), nullable=False
    )
    is_hidden = db.Column(
        db.Boolean(), nullable=False,
        server_default=expression.false()
    )

    # @staticmethod
    # def serialize_list(query, many=True):
    #     return [Announcement.serialize(x) for x in query]

    @staticmethod
    def serialize(query, many=False):
        if many:
            return [Announcement.serialize(x) for x in query]
        return {
            'a_id': int(query['id']),
            'title': query['title'],
            'description': query['description'],
            'created_at': query['created_at'],
        }
