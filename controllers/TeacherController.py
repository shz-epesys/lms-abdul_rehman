from handlers.DBHandler import (select)
from flask import jsonify
from helpers.enums import RolesEnum
from helpers.decorators import token_required
from models.models import Class, Teacher


def is_teacher(current_user):
    role = select(
        table="roles",
        feilds=['role_name'],
        where=f"id='{current_user.get('role_id')}' and is_hidden=0",
        as_list=True
    )
    if len(role) and role[0].get('role_name') == RolesEnum.Teacher.value:
        return True
    return False


def is_teacher_exist(current_user):
    teacher = select(
        table="teachers",
        feilds=[],
        where=f"user_id = '{current_user.get('id')}'  and is_hidden=0",
        as_list=True
    )
    if teacher:
        return teacher[0]
    return False


@token_required
def get_classes(current_user):
    if not is_teacher(current_user):
        return jsonify({'status': False, 'message:': "Bad Request"}), 400

    teacher = is_teacher_exist(current_user)
    if not teacher:
        return jsonify({'status': False, 'message:': "Teacher doesn't Exist"}), 400

    classes = select(
        table="classes",
        feilds=['id', 'name', 'no_of_students', 'image', 'created_at'],
        where=f"teacher_id = '{teacher.get('id')}'  and is_hidden=0",
        as_list=True
    )

    if classes:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                'data': [Class.serialize(x) for x in classes]
            }), 200
    return jsonify({'status': False, 'message:': "this teacher doesn't have any classes"}), 400


@ token_required
def get_class(current_user, class_id):

    if not is_teacher(current_user):
        return jsonify({'status': False, 'message:': "Bad Request"}), 400

    teacher = is_teacher_exist(current_user)
    if not teacher:
        return jsonify({'status': False, 'message:': "Teacher doesn't Exist"}), 400

    classes = select(
        table="classes",
        where=f"teacher_id = '{teacher.get('id')}' and id = '{class_id}' and is_hidden=0",
        as_list=True
    )
    if classes:
        return jsonify({'status': True, 'message:': 'classes successfully found.',
                        'data': Class.serialize(classes[0])}), 200
    return jsonify({'status': False, 'message:': "this teacher doesn't have any classes"}), 400


