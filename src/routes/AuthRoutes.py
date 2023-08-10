import traceback

from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from src.models.error.HTTP404Error import HTTP404Error
from src.services.auth.AuthServices import AuthServices
from src.utils.Logger import Logger

main_loginUserJWT = Blueprint('main_loginUserJWT', __name__)
main_refreshTokenJWT = Blueprint('main_refreshTokenJWT', __name__)
main_logoutJWT = Blueprint('main_logoutJWT', __name__)


main_funcionTestJWT = Blueprint('main_funcionTestJWT', __name__)

@main_loginUserJWT.route('/', methods=['POST'])
def loginApp():

    data = request.get_json()

    try:
        user = AuthServices.loginUser(data)

        if user:
            access_token = create_access_token(identity=user.id)
            response = jsonify({
                                    'token': access_token, 
                                    'success': True
                            })
            return response, 404
        else:
            raise HTTP404Error("Usuario no existe, credenciales no coinciden")

    except HTTP404Error as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': f"{ str(ex) }", 'success': False})
        return response, 404

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500
    

@main_logoutJWT.route('/', methods=['POST'])
@main_refreshTokenJWT.route('/', methods=['POST'])
def refreshToken():

    data = request.get_json()

    try:
        user = AuthServices.getUserById(data)

        if user:
            access_token = create_refresh_token(identity=user.id)
            response = jsonify({
                                    'token': access_token,
                                    'refresh': True,
                                    'success': True
                            })
            return response, 404
        else:
            raise HTTP404Error("Usuario no existe, credenciales no coinciden")

    except HTTP404Error as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': f"{ str(ex) }", 'success': False})
        return response, 404

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500
    


@main_funcionTestJWT.route('/', methods=['GET'])
@jwt_required()
def refreshToken():

    response = jsonify(
            {'message': "entra a la app", 'success': True})
    return response, 500