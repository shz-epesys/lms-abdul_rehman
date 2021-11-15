from controllers.ClassController import is_class_exist
from handlers.DBHandler import (select, select_with_join)
from flask import jsonify
from helpers.enums import RolesEnum
from helpers.decorators import token_required
from models.models import Class


def is_student(current_user):
    role = select(
        table="roles",
        feilds=['role_name'],
        where=f"id='{current_user.get('role_id')}' and is_hidden=0",
        as_list=True
    )
    if len(role) and role[0].get('role_name') == RolesEnum.Student.value:
        return True
    return False


def is_student_exist(current_user):
    student = select(
        table="students",
        feilds=[],
        where=f"user_id = '{current_user.get('id')}' and is_hidden=0",
        as_list=True
    )
    if student:
        return student
    return False


@token_required
def get_classes(current_user):
    if not is_student(current_user):
        return jsonify({'status': False, 'message:': "Bad Request"}), 400

    student = is_student_exist(current_user)
    if not student:
        return jsonify({'status': False, 'message:': "Student doesn't Exist"}), 400

    classes = select_with_join(
        tables=['students AS s', 'student_class AS sc', 'classes AS c'],
        feilds=['c.id', 'c.name', 'c.no_of_students',
                'c.image', 'c.created_at'],
        joins=['s.id=sc.students_id', 'sc.class_id = c.id'],
        where=f"s.id = '{student[0].get('id')}' and is_hidden=0",
        as_list=True
    )

    if classes:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                'data': [Class.serialize(x) for x in classes]
            }), 200
    return jsonify({'status': False, 'message:': "this student doesn't have any classes"}), 400


@ token_required
def get_class(current_user, class_id):

    if not is_student(current_user):
        return jsonify({'status': False, 'message:': "Bad Request"}), 400

    student = is_student_exist(current_user)
    if not student:
        return jsonify({'status': False, 'message:': "Student doesn't Exist"}), 404

    classes = select_with_join(
        tables=['students AS s', 'student_class AS sc', 'classes AS c'],
        feilds=['c.id', 'c.name', 'c.no_of_students',
                'c.image', 'c.created_at'],
        joins=['s.id=sc.students_id', 'sc.class_id = c.id'],
        where=f"s.id = '{student.get('id')}' and c.id = '{class_id}' and is_hidden=0",
        as_list=True
    )

    if classes:
        return jsonify({'status': True, 'message:': 'classes successfully found.',
                        'data': Class.serialize(classes[0])}), 200
    return jsonify({'status': False, 'message:': "The student is not assigned this class."}), 400


