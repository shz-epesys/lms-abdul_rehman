
import jwt
from handlers.DBHandler import (select)
from functools import wraps
from flask import request, jsonify
from config import SECRET_KEY


#  decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'token' in request.headers:
            token = request.headers['token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'status': False, 'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY)
            print(data)
            current_user = select(
                table='users',
                feilds=[],
                where=f"username='{data['username']}';"
            )
        except:
            return jsonify({
                'status': False,
                'message': 'Token is invalid !!'
            }), 401
        return f(current_user, *args, **kwargs)
    return decorated
