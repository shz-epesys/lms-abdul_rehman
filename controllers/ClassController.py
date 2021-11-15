from handlers.DBHandler import (
    insert_many, select, insert, select_with_join, update)
from flask import jsonify, request
from helpers.enums import RolesEnum, RolesMappingEnum
from helpers.decorators import token_required
# from models.models import Class
from forms.ClassForm import ClassForm
from forms.AnnouncForm import AnnouncForm
from models.models import ReadingMaterial, Student, Class, Announcement, Teacher
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import uuid
import os
from werkzeug.utils import secure_filename
from datetime import datetime


@token_required
def create_class(current_user):
    if current_user.get('role_id') != RolesMappingEnum.Teacher.value:
        return jsonify({'status': False, 'message:': "User not Autherized"}), 401
    form = ClassForm(data=request.json)
    class_data = select(
        table='classes',
        where=f"name = '{form.name.data}' and is_hidden=0",
        as_list=True
    )
    if form.validate():
        if class_data:
            return jsonify({'status': False, 'message': 'Class already exists!!'}), 401
        insert(
            table='classes',
            feilds=['name', 'no_of_students', 'image'],
            values=[form.name.data, form.no_of_students.data, form.image.data]
        )
    else:
        return jsonify({"status": False, "message": "Entries not valid"}), 406
    return jsonify({"status": True, "message": "Class created."}), 201


@token_required
def get_classes(current_user):
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 5, type=int)
    classes = select(
        table="classes",
        feilds=['id', 'name', 'no_of_students', 'image', 'created_at'],
        limit=[f'{page}', f'{size}'],
        # where=f"teacher_id = '{teacher.get('id')}'",
        where=f" and is_hidden=0",
        as_list=True
    )

    # print(classes)
    if classes:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                'data':     [Class.serialize(x, many=True) for x in classes]
            }), 200
    return jsonify({'status': False, 'message:': "this student doesn't have any classes"}), 400


def is_class_exist(class_id):
    classes = select(
        table="classes",
        feilds=[],
        where=f"id = '{class_id}' and is_hidden=0",
        as_list=True
    )
    if classes:
        return classes[0]
    return False


def is_student_exist(st_id):
    student = select(
        table="students",
        feilds=['id'],
        where=f"id = '{st_id}' and is_hidden = 0",
        as_list=True
    )
    if student:
        return True
    return False


@token_required
def get_student(current_user, class_id, st_id):
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 5, type=int)
    clss = is_class_exist(class_id)
    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400
    std = is_student_exist(st_id)
    if not std:
        return jsonify({'status': False, 'message:': "Student doesn't Exist"}), 400

    students = select_with_join(
        tables=['users AS u', 'students AS s',
                'student_class AS sc', 'classes AS c'],
        feilds=['s.id', 'u.first_name', 'u.last_name', 'u.dob', 'u.email', 's.reg_no', 'u.contact_no',
                'c.image', 'c.created_at'],
        joins=['u.id=s.user_id', 's.id=sc.students_id', 'sc.class_id = c.id'],
        limit=[f'{page}', f'{size}'],
        where=f" c.id = '{class_id}' and s.id='{st_id}' and s.is_hidden= 0",
        as_list=True
    )[0]
    print(students)
    if students:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                'data': Student.serialize(students)
            }
        ), 200
    return jsonify(
        {
            'status': False,
            'message:': "The student is not assigned this class."
        }
    ), 400


@token_required
def get_students(current_user, class_id):
    if current_user.get('role_id') != RolesMappingEnum.Teacher.value:
        return jsonify({'status': False, 'message:': "User not Autherized"}), 401
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 5, type=int)
    clss = is_class_exist(class_id)
    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400

    students = select_with_join(
        tables=['users AS u', 'students AS s',
                'student_class AS sc', 'classes AS c'],
        feilds=['s.id', 'u.first_name', 'u.last_name', 'u.dob', 'u.email', 's.reg_no', 'u.contact_no',
                'c.image', 'c.created_at'],
        joins=['u.id=s.user_id', 's.id=sc.students_id', 'sc.class_id = c.id'],
        limit=[f'{page}', f'{size}'],
        where=f" c.id = '{class_id}' and is_hidden=0",
        as_list=True
    )
    # print(students)
    if students:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                # [Student.serialize(student) for student in students]
                'data': Student.serialize(students, True)
            }
        ), 200
    return jsonify(
        {
            'status': False,
            'message:': "The student is not assigned this class."
        }
    ), 400


@token_required
def create_announcements(current_user, class_id):
    form = AnnouncForm(data=request.json)
    clss = is_class_exist(class_id)
    if current_user.get('role_id') != RolesMappingEnum.Teacher.value:
        return jsonify({'status': False, 'message:': "User not Autherized"}), 401

    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400

    if form.validate():
        insert(
            table='announcements',
            feilds=['title', 'description', 'class_id'],
            values=[form.title.data, form.description.data, class_id]

        )
    else:
        return jsonify({"status": False, "message": "Entries not valid"}), 406
    return jsonify({"status": True, "message": "Announcement created."}), 201


@token_required
def get_announcements(current_user, class_id):
    clss = is_class_exist(class_id)
    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400

    announcements = is_announcement_exist(class_id)

    if announcements:
        return jsonify(
            {
                'status': True,
                'message:': 'Announcements successfully found.',
                'data': Announcement.serialize(announcements, True)
            }), 200
    return jsonify({'status': False, 'message:': "this student doesn't have any classes"}), 400


def is_announcement_exist(class_id, a_id=None):
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 5, type=int)
    where = f"class_id='{class_id}' and is_hidden=0"
    if a_id:
        where += f" id='{a_id}'"
    announcements = select(
        table="announcements",
        feilds=['id', 'title', 'description', 'created_at', 'is_hidden'],
        limit=[f'{page}', f'{size}'],
        where=where,
        as_list=True
    )

    if announcements:
        return announcements
    return False


@token_required
def update_announcements(current_user, class_id, a_id):
    if current_user.get('role_id') != RolesMappingEnum.Teacher.value:
        return jsonify({'status': False, 'message:': "User not Autherized"}), 401
    form = AnnouncForm(data=request.json)
    clss = is_class_exist(class_id)
    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400
    announcements = is_announcement_exist(class_id, a_id)
    if not announcements:
        return jsonify({'status': False, 'message:': "Announcement doesn't Exist"}), 404
    update(
        table="announcements",
        feilds=['title', 'description'],
        values=[form.title.data, form.description.data],
        where=f"id='{a_id}' "
    )
    return jsonify({'status': True, 'message:': "Announcement updated"}), 200


@token_required
def delete_announcements(current_user, class_id, a_id):
    announcements = is_announcement_exist(class_id, a_id)
    if not announcements:
        return jsonify({'status': False, 'message:': "Not Found"}), 404
    update(
        table="announcements",
        feilds=['is_hidden'],
        values=['1'],
        where=f"class_id = '{class_id}' and id ='{a_id}'"
    )
    return jsonify({'status': True, 'message:': "Announcement deleted"}), 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_filename(file):
    filename = secure_filename(
        file.filename.rsplit('.', 2)[0].
        lower()+'-'+datetime.now().strftime('%d-%m-%y-%I-%M-%S')+'-' +
        str(uuid.uuid4()).rsplit('-', 5)[0]+"." +
        file.filename.rsplit('.', 1)[1].
        lower()
    )
    return filename


@token_required
def upload_files(current_user, class_id):
    if current_user.get('role_id') != RolesMappingEnum.Teacher.value:
        return jsonify({'status': False, 'message:': "User not Autherized"}), 401
    if 'files[]' not in request.files:
        return jsonify({'status': False, 'message': 'file path not found'}), 404

    files = request.files.getlist('files[]')
    rejected_files = []
    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = create_filename(file)
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
            )
            uploaded_files.append(
                {
                    'file_name': filename,
                    'file_path': os.path.join(UPLOAD_FOLDER, filename)
                }
            )

        else:
            rejected_files .append(file.filename)
    return jsonify(
        {
            'uploaded_files': uploaded_files,
            'rejected_files ': rejected_files
        }
    ), 201


@token_required
def store_files(current_user, class_id):
    if current_user.get('role_id') != RolesMappingEnum.Teacher.value:
        return jsonify({'status': False, 'message:': "User not Autherized"}), 401
    data = request.json['uploaded_files']
    try:
        clss = is_class_exist(class_id)
        if not data:
            return jsonify({'status': False, 'message': 'file path not found'}), 404
        if clss:
            def append_class(obj):
                obj['class_id'] = class_id
                return obj

            insert_many(
                table='reading_materials',
                feilds=['file_name', 'file_path', 'class_id'],
                values=list(map(append_class, data))
            )

        return jsonify({"status": True, "message": "Files succesfully stored."}), 201
    except:
        return jsonify({"status": False, "message": "Invalid data."}), 400


@token_required
def get_files(current_user, class_id):

    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 5, type=int)
    clss = is_class_exist(class_id)
    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400
    files = select(
        table='reading_materials',
        feilds=['id', 'file_name', 'file_path', 'created_at'],
        limit=[f'{page}', f'{size}'],

        where=f'class_id="{class_id}" and is_hidden=0',
        as_list=True
    )
    if files:
        return jsonify(
            {
                'status': True,
                'message:': 'files successfully found.',
                'data': ReadingMaterial.serialize(files, True)
            }), 200
    return jsonify({'status': False, 'message:': "Files not found"}), 404


@token_required
def get_teacher(current_user, class_id):

    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 5, type=int)
    clss = is_class_exist(class_id)
    if not clss:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 404

    teacher = select_with_join(
        tables=['users AS u', 'teachers AS t',
                'teacher_class AS ts', 'classes AS c'],
        feilds=[
            't.id', 'u.first_name',
            'u.last_name', 'u.dob',
            'u.email', 't.reg_no',
            't.degree', 't.experience',
            'u.contact_no',
            'c.image', 'c.created_at'
        ],
        joins=['u.id=t.user_id', 't.id=ts.teacher_id', 'ts.class_id = c.id'],
        limit=[f'{page}', f'{size}'],
        where=f" c.id = '{class_id}' and t.is_hidden= 0",
        as_list=True
    )
    if teacher:
        return jsonify({'status': True, 'message:': 'classes successfully found.',
                        'data': Teacher.serialize(teacher[0])}), 200
    return jsonify({'status': False, 'message:': "this class doesn't have teacher assigned."}), 404
