from decouple import config as config_environment

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from src.routes import AuthRoutes, NotificationRoutes

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = config_environment('JWT_SECRET_KEY')
jwt = JWTManager(app)

if config_environment('CORS') == 'cors':
    CORS(app, origins=['http://139.144.171.68/'], methods=['GET', 'POST'], allow_headers=['Content-Type', 'Authorization'])

# swagger configs
SWAGGER_URL = '/swagger'
#API_URL = '/static/openapi.json'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Todo Lista Endpoints"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)


def init_app(config):

    app.config.from_object(config)

    app.register_blueprint(NotificationRoutes.main_notiSelec, url_prefix='/noti_selec')
    app.register_blueprint(NotificationRoutes.main_notiRead, url_prefix='/noti_read')
    app.register_blueprint(NotificationRoutes.main_carHistory, url_prefix='/car_history')
    app.register_blueprint(NotificationRoutes.main_carSelect, url_prefix='/car_select')
    app.register_blueprint(NotificationRoutes.main_motorCut, url_prefix='/motor_cut')
    app.register_blueprint(NotificationRoutes.main_geoInsert, url_prefix='/geo_insert')
    app.register_blueprint(NotificationRoutes.main_geoSelect, url_prefix='/geo_select')
    app.register_blueprint(NotificationRoutes.main_geoDelete, url_prefix='/geo_delete')
    app.register_blueprint(NotificationRoutes.main_questionSelect, url_prefix='/question_select')
    app.register_blueprint(NotificationRoutes.main_userSelect, url_prefix='/user_select')
    app.register_blueprint(NotificationRoutes.main_userUpdate, url_prefix='/user_update')
    app.register_blueprint(NotificationRoutes.main_loginApp, url_prefix='/login_app')


    app.register_blueprint(AuthRoutes.main_loginUserJWT, url_prefix='/login')
    app.register_blueprint(AuthRoutes.main_logoutJWT, url_prefix='/logout')
    app.register_blueprint(AuthRoutes.main_refreshTokenJWT, url_prefix='/refresh_token')
    app.register_blueprint(AuthRoutes.main_funcionTestJWT, url_prefix='/function_test')

    return app