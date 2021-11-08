from re import T
from sqlalchemy.sql.expression import null
from forms.AuthForm import StudentForm, TeacherForm, StudentForm, AdminForm,  LoginForm, UserForm
from handlers.DBHandler import (insert, select)
from flask import jsonify,  request
from datetime import datetime, timedelta
import uuid

import jwt
from config import SECRET_KEY


def create_user(form):
    role_id = select(
        table='roles',
        feilds=['id'],
        where=f'role_name = "{form.role.data}"'

    )
    role_id = role_id.fetchall()[0][0]
    user_data = select(
        table='users',
        feilds=[],
        where=f'username  = "{form.username.data.lower()}" or email = "{form.email.data}"'
    )
    data = user_data.fetchall()
    if not data:
        insert(
            table='users',
            feilds=[
                'username', 'email',
                'password', 'first_name',
                'last_name', 'contact_no',
                'address', 'city',
                'dob',
                'role_id'
            ],
            values=[
                form.username.data.lower(), form.email.data.lower(),
                form.password.data, form.first_name.data,
                form.last_name.data, form.contact_no.data,
                form.address.data, form.city.data,
                form.dob.data,
                role_id
            ]
        )
        user_id = select(
            table='users',
            feilds=['id'],
            where=f'username  = "{form.username.data.lower()}"'
        )
        return user_id.fetchall()[0][0]
    return null


def create_student(data):
    form = StudentForm(data=data)
    if form.validate():
        user_id = create_user(form)
        if user_id is not null:
            reg_no = str(uuid.uuid4()).split('-')[0]+str(user_id)
            insert(
                table='students',
                feilds=[
                    'reg_no', 'user_id',
                ],
                values=[
                    reg_no, user_id
                ]
            )

            return {"status": True, "message": 'Student created.', 'status_code': 201}
        return {"status": False, "message": 'Duplicate entries!', 'status_code': 401}
    return {"status": False, "message": 'Entries not valid!', 'status_code': 400}


def create_teacher(data):
    form = TeacherForm(data=data)
    if form.validate():
        user_id = create_user(form)
        if user_id is not null:
            reg_no = str(uuid.uuid4()).split('-')[0]+str(user_id)
            insert(
                table='teachers',
                feilds=[
                    'reg_no', 'user_id',
                    'degree', 'experience'
                ],
                values=[
                    reg_no, user_id,
                    form.degree.data, form.exp.data
                ]
            )
            return {"status": True, "message": 'teacher created.', 'status_code': 201}
        return {"status": False, "message": 'Duplicate entries!', 'status_code': 401}
    return {"status": False, "message": 'Entries not valid!', 'status_code': 400}


def create_admin(data):
    form = AdminForm(data=data)
    if form.validate():
        create_user(form)
    else:
        return jsonify({'status': False, 'message': 'Entries not valid!'}), 406


def is_role_exist(role):
    role = select(
        table="roles",
        feilds=['role_name'],
        where=f'role_name="{role}" '
    )
    role = role.fetchall()
    print(role)
    if role:
        return {"status": True, "message": 'Role exists!', 'status_code': 200}
    return {"status": False, "message": 'Invalid Role!', 'status_code': 406}


def signup():
    data = request.json
    user = UserForm(data=data)
    if user.validate():

        role = data['role'].lower()

        role_exist = is_role_exist(role)
        if not role_exist['status']:
            return jsonify({"status": role_exist['status'], 'message': role_exist['message']}), role_exist['status_code']
        else:
            create = {
                'student': create_student,
                'teacher': create_teacher,
                'admin': create_admin

            }
            result = create[role](data)
            if result["status"]:
                return jsonify({"status": result["status"], 'message': result["message"]}), result["status_code"]
            return jsonify({"status": result["status"], 'message': result["message"]}), result["status_code"]
    return jsonify(
        {"status": False,
            'message': 'Invalid Entries or Fields missing!!!'
         }
    ), 400


def login():
    form = LoginForm(data=request.json)
    if form.validate():
        user_data = select(
            table="users",
            feilds=[],
            where=f'(username="{form.username.data}" or email="{form.username.data}") and password="{form.password.data}"'
        )
        data = user_data.fetchall()
        if data:
            data = data[0]
            role = select(
                table="roles",
                feilds=['role_name'],
                where=f'id="{data[10]}"'
            )
            print(data)
            token = jwt.encode(
                {
                    'username': data[1],
                    'exp': datetime.utcnow() + timedelta(minutes=60*24)
                },
                SECRET_KEY
            )
            login_data = {
                'username': data[1],
                'first_name': data[3],
                'last_name': data[4],
                'role': role.fetchall()[0][0],
                'token': token.decode('UTF-8')
            }
            return jsonify(
                {
                    "status": True,
                    'message': 'Login Successful',
                    'data': login_data

                }
            ), 201

        else:
            return jsonify(
                {
                    "status": False,
                    'message': 'User doesnt exist or incorrect Input !'
                }
            ), 401
    return jsonify(
        {
            "status": False,
            'message': 'Invalid Entries or Fields missing!!!!'
        }
    ), 400
