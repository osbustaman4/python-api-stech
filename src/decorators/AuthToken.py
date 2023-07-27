from functools import wraps
from flask import request, jsonify
from src.utils.Logger import Logger

from decouple import config

import jwt
import traceback


def verify_token(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        secret = config('JWT_KEY')

        try:
            if  'Authorization' in (request.headers).keys():
                authorization = request.headers['Authorization']
                encoded_token = authorization.split(" ")[1]

                if ((len(encoded_token) > 0) and (encoded_token.count('.') <= 3)):
                    try:
                        payload = jwt.decode(encoded_token, secret, algorithms=["HS256"])
                        roles = list(payload['roles'])

                        if 'Administrator' in roles:
                            return func(*args, **kwargs)
                        return False
                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                        response = jsonify({'message': 'Unauthorized'})
                        return response, 401

            response = jsonify({'message': 'Unauthorized'})
            return response, 401
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

            response = jsonify({'message': 'Unauthorized'})
            return response, 401

    return decorador