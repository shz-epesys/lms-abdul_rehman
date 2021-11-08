from decorators.token_required import token_required
from handlers.DBHandler import (insert, select)
from flask import jsonify,  request


@token_required
def get_classes(current_user, teacher_id):
    classes = select(
        table="classes",
        feilds= ['name'],
        where=f"teacher_id = '{teacher_id}'"
    )
    classes = classes.fetchall()
    result =[i[0] for i in classes]
    if result:
        return jsonify({'status':True, 'message:':'classes found.', 'classes': result}),200
    return jsonify({'status':False, 'message:':'invalid entry'}),400



@token_required
def get_class(current_user,teacher_id,class_id):
    classes = select(
        table="classes",
        feilds= ['name'],
        where=f"teacher_id = '{teacher_id}' and id = '{class_id}'"
    )
    result = classes.fetchall()
    if result:
        return jsonify({'status':True, 'message:':'classes found.', 'classe': result[0][0]}),200
    return jsonify({'status':False, 'message:':'invalid entry'}),400