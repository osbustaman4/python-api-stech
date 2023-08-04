from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from src.routes import ObjectDataRoutes, NotificationRoutes

app = Flask(__name__)

# swagger configs
SWAGGER_URL = '/swagger'
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

    app.register_blueprint(ObjectDataRoutes.main_get_data, url_prefix='/')
    app.register_blueprint(ObjectDataRoutes.main_getObjectData, url_prefix='/object-data/base64')
    app.register_blueprint(ObjectDataRoutes.main_getObjectDataJson, url_prefix='/object-data/json')

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

    

    return app