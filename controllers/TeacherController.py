from decorators.token_required import token_required
from handlers.DBHandler import (select)
from flask import jsonify


@token_required
def is_teacher(current_user, teacher_id):
    print(current_user)
    # role = select(
    #     table="roles",
    #     feilds=['role_name'],
    #     where=f"id='{}'",
    #     as_list=True
    # )
    return jsonify({}), 200


def is_teacher_exist(teacher_id):
    teacher = select(
        table="teachers",
        feilds=[],
        where=f"id = '{teacher_id}'"
    )
    teacher = teacher.fetchall()
    print(teacher)
    if teacher:
        return {"status": True, "message": "Teacher exists!", 'status_code': 200}
    return {"status": False, "message": "Teacher doesn't exists!", 'status_code': 406}


@token_required
def get_classes(current_user, teacher_id):
    teacher = is_teacher_exist(teacher_id)
    if not teacher['status']:
        return jsonify({'status': teacher['status'], 'message:': teacher['message']}), teacher['status_code']

    classes = select(
        table="classes",
        feilds=['name'],
        where=f"teacher_id = '{teacher_id}'"
    )
    classes = classes.fetchall()
    result = [i[0] for i in classes]
    if result:
        return jsonify({'status': True, 'message:': 'classes successfully found.', 'classes': result}), 200
    return jsonify({'status': False, 'message:': "this teacher doesn't have any classes"}), 400


@token_required
def get_class(current_user, teacher_id, class_id):
    teacher = is_teacher_exist(teacher_id)
    if not teacher['status']:
        return jsonify({'status': teacher['status'], 'message:': teacher['message']}), teacher['status_code']

    classes = select(
        table="classes",
        feilds=['name'],
        where=f"teacher_id = '{teacher_id}' and id = '{class_id}'"
    )
    result = classes.fetchall()
    if result:
        return jsonify({'status': True, 'message:': 'classes found.', 'classe': result[0][0]}), 200
    return jsonify({'status': False, 'message:': 'invalid class id'}), 400
