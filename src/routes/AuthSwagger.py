import traceback

from flask import Flask, request, jsonify, Blueprint, redirect, url_for
from flask import Blueprint
from flask_login import login_user, login_required
from src.auth import load_user
from flask_swagger_ui import get_swaggerui_blueprint
from src.services.AuthSwaggerServices import AuthSwaggerServices

from src.utils.Logger import Logger

app = Flask(__name__)

main_mainSwaggerOauth = Blueprint('main_mainSwaggerOauth', __name__)
swagger_blueprint = Blueprint('swagger_blueprint', __name__)

SWAGGER_URL = '/swagger' 
API_URL = '/static/swagger.json'

SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Todo Lista Endpoints"
    }
)

swagger_blueprint.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


@main_mainSwaggerOauth.route('/', methods=['POST'])
def swagger_oauth():
    try:
        data = request.get_json()
        is_authenticated = AuthSwaggerServices.loginSwagger(data)
        if is_authenticated:
            login_user(is_authenticated)
            return redirect(url_for('main_mainSwaggerOauth.swagger_page'))
        else:
            return redirect(url_for('main_mainSwaggerOauth.login_page'))

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {
                'message': "Internal Server Error", 
                'success': False,
                'error': str(ex)
            })
        return response, 500


@main_mainSwaggerOauth.route('/', methods=['GET'])
@login_required
def swagger_page():
    return redirect(url_for('swagger_blueprint.swagger_ui.show'))

@main_mainSwaggerOauth.route('/login', methods=['POST'])
def login_page():
    username = request.form['username']
    password = request.form['password']
    user = load_user(username)  # Implementa esta función para cargar el usuario

    if user and user.password == password:
        login_user(user)
        return redirect(url_for('swagger_blueprint.swagger_page'))
    else:
        return "Credenciales inválidas", 401