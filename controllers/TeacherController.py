from decorators.token_required import token_required
from handlers.DBHandler import (insert, select)
from flask import jsonify,  request


# @token_required
def get_classes(teacher_id):
    classes = select(
        table="classes",
        feilds= ['name'],
        where=f"teacher_id = '{teacher_id}'"
    )
    output = classes.fetchall()
    print(output)
    # for user in classes:
    #     output.append({
    #         'public_id': user.public_id,
    #         'name': user.username,
    #         'email': user.email
    #     })
    return jsonify({'classes': output})


def get_class(current_user,teacher_id,class_id):
        # user_schema = UserSchema()
    classes = select(
        table="classes",
        feilds= ['name'],
        where=f"teacher_id = '{teacher_id}' and id = '{class_id}'"
    )
    result = classes.fetchone()[0][0]
    return jsonify(result)