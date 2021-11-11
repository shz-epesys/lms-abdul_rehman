from handlers.DBHandler import (select, insert, select_with_join)
from flask import jsonify, request
# from helpers.enums import RolesEnum
from helpers.decorators import token_required
# from models.models import Class
from forms.ClassForm import ClassForm
from models.models import Student, Class


@token_required
def create_class(current_user):
    form = ClassForm(data=request.json)
    class_data = select(
        table='classes',
        where=f"name = '{form.name.data}'",
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
    size = request.args.get('size', 2, type=int)
    classes = select(
        table="classes",
        feilds=['id', 'name', 'no_of_students', 'image', 'created_at'],
        # limit=[f'{page}',f'{size}'],
        # where=f"teacher_id = '{teacher.get('id')}'",
        as_list=True
    )

    print(classes)
    if classes:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                'data':     [Class.serialize(x) for x in classes]
            }), 200
    return jsonify({'status': False, 'message:': "this student doesn't have any classes"}), 400


def is_class_exist(class_id):
    classes = select(
        table="classes",
        feilds=[],
        where=f"id = '{class_id}'",
        as_list=True
    )
    if classes:
        return classes[0]
    return False


@token_required
def get_students(current_user, class_id):
    page = request.args.get('page', 0, type=int)
    size = request.args.get('size', 2, type=int)
    classe = is_class_exist(class_id)
    if not classe:
        return jsonify({'status': False, 'message:': "Class doesn't Exist"}), 400

    students = select_with_join(
        tables=['users AS u', 'students AS s',
                'student_class AS sc', 'classes AS c'],
        feilds=['s.id', 'u.first_name', 'u.last_name', 'u.dob', 'u.email', 's.reg_no', 'u.contact_no',
                'c.image', 'c.created_at'],
        joins=['u.id=s.user_id', 's.id=sc.students_id', 'sc.class_id = c.id'],
        limit=[f'{page}', f'{size}'],
        where=f" c.id = '{class_id}'",
        as_list=True
    )
    print(students)
    if students:
        return jsonify(
            {
                'status': True,
                'message:': 'classes successfully found.',
                'data': [Student.serialize(student) for student in students]
            }
        ), 200
    return jsonify(
        {
            'status': False,
            'message:': "The student is not assigned this class."
        }
    ), 400
